"""Base class to access SRTM elevation data"""
import urllib


class Topography:

    SCHEME = "https"
    NETLOC = "portal.opentopography.org"
    PATH = "/API/globaldem"

    VALID_DEM_TYPES = ("SRTMGL3", "SRTMGL1", "SRTMGL1_E")
    VALID_OUTPUT_FORMATS = ("GTiff", "AAIGrid", "HFA")
    DEFAULT = {
        "south": 36.738884,
        "north": 38.091337,
        "west": -120.168457,
        "east": -118.465576,
    }

    def __init__(
        self,
        dem_type=None,
        south=None,
        north=None,
        west=None,
        east=None,
        output_format=None,
    ):

        if dem_type in Topography.VALID_DEM_TYPES:
            self._dem_type = dem_type
        else:
            raise ValueError(
                "dem_type must be one of %s." % (Topography.VALID_DEM_TYPES,)
            )

        if dem_type in Topography.VALID_OUTPUT_FORMATS:
            self._output_format = output_format
        else:
            raise ValueError(
                "output_format must be one of %s." % (Topography.VALID_OUTPUT_FORMATS,)
            )

        self._south = south or Topography.DEFAULT["south"]
        self._north = north or Topography.DEFAULT["north"]

        if self._south > 90 or self._south < -90:
            raise ValueError(
                "south coordinate ({0}) must be in [-90,90]".format(self.south)
            )

        if self._north > 90 or self._north < -90:
            raise ValueError(
                "north coordinate ({0}) must be in [-90,90]".format(self.north)
            )

        if self._south > self._north:
            raise ValueError(
                "south coordinate ({0}) must be less than north ({1})".format(
                    self.south, self.north
                )
            )

        self._west = west or Topography.DEFAULT["west"]
        self._east = east or Topography.DEFAULT["east"]

        if self._west > 180 or self._west < -180:
            raise ValueError(
                "west coordinate ({0}) must be in [-180,180]".format(self.west)
            )

        if self._east > 180 or self._east < -180:
            raise ValueError(
                "east coordinate ({0}) must be in [-180,180]".format(self.east)
            )

        if self._west > self._east:
            raise ValueError(
                "west coordinate ({0}) must be less than east ({1})".format(
                    self.west, self.east
                )
            )

    @property
    def dem_type(self):
        return str(self._dem_type)

    @property
    def output_format(self):
        return str(self._output_format)

    @property
    def south(self):
        return self._south

    @property
    def north(self):
        return self._north

    @property
    def west(self):
        return self._west

    @property
    def east(self):
        return self._east

    @staticmethod
    def get(dem_type, south, north, west, east, output_format):
        print("This is bmi-topography!")

    @staticmethod
    def data_url():
        return urllib.parse.urlunparse(
            (Topography.SCHEME, Topography.NETLOC, Topography.PATH, "", "", "")
        )
