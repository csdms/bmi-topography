"""Base class to access elevation data"""
import os
import urllib
from pathlib import Path

import requests
import rioxarray
from rasterio.crs import CRS

from .api_key import ApiKey
from .bbox import BoundingBox


class Topography:

    """Fetch and cache land elevation data from OpenTopography."""

    SCHEME = "https"
    NETLOC = "portal.opentopography.org"
    PATH = "/API/globaldem"

    DEFAULT = {
        "dem_type": "SRTMGL3",
        "south": 36.738884,
        "north": 38.091337,
        "west": -120.168457,
        "east": -118.465576,
        "output_format": "GTiff",
        "cache_dir": "~/.bmi_topography",
    }

    VALID_DEM_TYPES = (
        "SRTMGL3",
        "SRTMGL1",
        "SRTMGL1_E",
        "AW3D30",
        "AW3D30_E",
        "SRTM15Plus",
        "NASADEM",
        "COP30",
        "COP90",
    )
    VALID_OUTPUT_FORMATS = {"GTiff": "tif", "AAIGrid": "asc", "HFA": "img"}

    def __init__(
        self,
        dem_type=None,
        south=None,
        north=None,
        west=None,
        east=None,
        output_format=None,
        cache_dir=None,
        api_key=None,
    ):
        self._api_key = ApiKey.from_sources(api_key)
        # if api_key is None:
        #     self._api_key = find_user_api_key() or use_demo_key()
        # else:
        #     self._api_key = api_key

        if dem_type in Topography.VALID_DEM_TYPES:
            self._dem_type = dem_type
        else:
            raise ValueError(
                "dem_type must be one of %s." % (Topography.VALID_DEM_TYPES,)
            )

        if output_format in Topography.VALID_OUTPUT_FORMATS.keys():
            self._output_format = output_format
            self._file_extension = Topography.VALID_OUTPUT_FORMATS[output_format]
        else:
            raise ValueError(
                "output_format must be one of %s."
                % [k for k in Topography.VALID_OUTPUT_FORMATS.keys()]
            )

        self._bbox = BoundingBox((south, west), (north, east))

        self._da = None

        if cache_dir is None:
            cache_dir = Path(Topography.DEFAULT["cache_dir"])
        self._cache_dir = Path(cache_dir).expanduser().resolve().absolute()

    @property
    def dem_type(self):
        return str(self._dem_type)

    @property
    def output_format(self):
        return str(self._output_format)

    @property
    def file_extension(self):
        return str(self._file_extension)

    @property
    def bbox(self):
        return self._bbox

    @property
    def cache_dir(self):
        return self._cache_dir

    @staticmethod
    def data_url():
        return urllib.parse.urlunparse(
            (Topography.SCHEME, Topography.NETLOC, Topography.PATH, "", "", "")
        )

    def fetch(self):
        """Download and locally store topography data.

        Returns:
            pathlib.Path: The path to the downloaded file
        """
        fname = Path(
            self.cache_dir
        ) / "{dem_type}_{south}_{west}_{north}_{east}.{ext}".format(
            dem_type=self.dem_type,
            south=self.bbox.south,
            north=self.bbox.north,
            west=self.bbox.west,
            east=self.bbox.east,
            ext=self.file_extension,
        )

        if not fname.is_file():
            self.cache_dir.mkdir(exist_ok=True)

            params = {
                "demtype": self.dem_type,
                "south": self.bbox.south,
                "north": self.bbox.north,
                "west": self.bbox.west,
                "east": self.bbox.east,
                "outputFormat": self.output_format,
            }
            if self._api_key:
                params["API_Key"] = str(self._api_key)

            response = requests.get(Topography.data_url(), params=params, stream=True)
            if response.status_code == 401:
                if self._api_key.source == "demo":
                    msg = os.linesep.join(
                        "It looks like you are using a demo key. This error may be the result of "
                        "you reaching your maximum number of downloads."
                    )
                else:
                    msg = (
                        "It looks like you are using a user-supplied key. This error may mean "
                        "that your key is out of date or there is a typo in the supplied key. "
                        f"(source={self._api_key.source})"
                    )
                response.reason = os.linesep.join([response.reason, "", msg, ""])
            response.raise_for_status()

            with fname.open("wb") as fp:
                for chunk in response.iter_content(chunk_size=None):
                    fp.write(chunk)

        return fname.absolute()

    @property
    def da(self):
        return self._da

    def load(self):
        """Load a cached topography data file into an xarray DataArray.

        Returns:
            xarray.DataArray: A container for the data
        """
        if self._da is None:
            self._da = rioxarray.open_rasterio(self.fetch())
            self._da.name = self.dem_type

            crs = CRS.from_wkt(self._da.spatial_ref.crs_wkt)
            if crs.is_geographic:
                self._da.attrs["units"] = "degrees"
            else:
                self._da.attrs["units"] = crs.linear_units

        return self._da
