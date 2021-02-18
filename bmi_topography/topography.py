"""Base class to access SRTM elevation data"""
import urllib
from pathlib import Path

from .bbox import BoundingBox


class Topography:

    SCHEME = "https"
    NETLOC = "portal.opentopography.org"
    PATH = "/API/globaldem"

    VALID_DEM_TYPES = ("SRTMGL3", "SRTMGL1", "SRTMGL1_E")
    VALID_OUTPUT_FORMATS = ("GTiff", "AAIGrid", "HFA")

    def __init__(
        self,
        dem_type=None,
        south=None,
        north=None,
        west=None,
        east=None,
        output_format=None,
        cache_dir=None,
    ):

        if dem_type in Topography.VALID_DEM_TYPES:
            self._dem_type = dem_type
        else:
            raise ValueError(
                "dem_type must be one of %s." % (Topography.VALID_DEM_TYPES,)
            )

        if output_format in Topography.VALID_OUTPUT_FORMATS:
            self._output_format = output_format
        else:
            raise ValueError(
                "output_format must be one of %s." % (Topography.VALID_OUTPUT_FORMATS,)
            )

        self._bbox = BoundingBox((south, west), (north, east))

        if cache_dir is None:
            cache_dir = Path("~/.bmi_topography")
        self._cache_dir = Path(cache_dir).expanduser().resolve()

    @property
    def dem_type(self):
        return str(self._dem_type)

    @property
    def output_format(self):
        return str(self._output_format)

    @property
    def bbox(self):
        return self._bbox

    @property
    def cache_dir(self):
        return self._cache_dir

    def fetch(self):
        print("This is bmi-topography!")
        print(self.dem_type)
        print(self.bbox)
        print(self.output_format)

    @staticmethod
    def data_url():
        return urllib.parse.urlunparse(
            (Topography.SCHEME, Topography.NETLOC, Topography.PATH, "", "", "")
        )
