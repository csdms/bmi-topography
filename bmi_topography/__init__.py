from .bbox import BoundingBox
from .bmi import BmiTopography
from .topography import Topography

__all__ = ["Topography", "BoundingBox", "BmiTopography"]

DEFAULT = {
    "dem_type": "SRTMGL3",
    "south": 36.738884,
    "north": 38.091337,
    "west": -120.168457,
    "east": -118.465576,
    "output_format": "GTiff",
}
