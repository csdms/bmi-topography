"""Base class to access elevation data"""
import os
import urllib
from pathlib import Path

import requests
import xarray as xr

from .bbox import BoundingBox


def find_api_key():
    """Search for an API key."""
    if "OPENTOPOGRAPHY_API_KEY" in os.environ:
        api_key = os.environ["OPENTOPOGRAPHY_API_KEY"]
    else:
        api_key = read_first_of(
            [".opentopography.txt", "~/.opentopography.txt"]
        ).strip()

    return api_key


def read_first_of(files):
    """Read the contents of the first file encountered."""
    contents = ""
    for path in files:
        try:
            contents = open(path, "r").read()
        except OSError:
            pass
        else:
            break
    return contents


class Topography:

    """Fetch and cache NASA SRTM land elevation data."""

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

    VALID_DEM_TYPES = ("SRTMGL3", "SRTMGL1", "SRTMGL1_E", "AW3D30", "AW3D30_E")
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
        if api_key is None:
            self._api_key = find_api_key()
        else:
            self._api_key = api_key

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
                params["API_Key"] = self._api_key

            response = requests.get(Topography.data_url(), params=params, stream=True)
            if response.status_code == 401:
                response.reason = "This dataset requires an API Key for access"
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
            self._da = xr.open_rasterio(self.fetch())
            self._da.name = self.dem_type
            self._da.attrs["units"] = "meters"
            self._da.attrs["location"] = "node"

        return self._da
