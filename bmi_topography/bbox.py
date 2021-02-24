from collections.abc import Iterable
from typing import Tuple


class BoundingBox:

    """Represent a simple latitude-longiture bounding box.

    Attributes
    ----------
    lower_left : tuple
        The southwest corner of the box, given by (south, west)
    upper_right : tuple
        The northeast corner of the box, given by (north, east)

    Examples
    --------
    Create a bounding box:

    >>> from bmi_topography import BoundingBox
    >>> bbox = BoundingBox((33, 111), (44, 122))
    >>> print(bbox)
    [(33, 111), (44, 122)]

    """

    def __init__(self, lower_left: Tuple[float], upper_right: Tuple[float]) -> None:
        self._lower_left = lower_left
        self._upper_right = upper_right

        if not isinstance(self.lower_left, Iterable) or len(self.lower_left) != 2:
            raise ValueError(
                "lower left coordinate ({0}) must have two elements".format(
                    self.lower_left
                )
            )

        if not isinstance(self.upper_right, Iterable) or len(self.upper_right) != 2:
            raise ValueError(
                "upper right coordinate ({0}) must have two elements".format(
                    self.upper_right
                )
            )

        if self.south > 90 or self.south < -90:
            raise ValueError(
                "south coordinate ({0}) must be in [-90,90]".format(self.south)
            )

        if self.north > 90 or self.north < -90:
            raise ValueError(
                "north coordinate ({0}) must be in [-90,90]".format(self.north)
            )

        if self.south > self.north:
            raise ValueError(
                "south coordinate ({0}) must be less than north ({1})".format(
                    self.south, self.north
                )
            )

        if self.west > 180 or self.west < -180:
            raise ValueError(
                "west coordinate ({0}) must be in [-180,180]".format(self.west)
            )

        if self.east > 180 or self.east < -180:
            raise ValueError(
                "east coordinate ({0}) must be in [-180,180]".format(self.east)
            )

        if self.west > self.east:
            raise ValueError(
                "west coordinate ({0}) must be less than east ({1})".format(
                    self.west, self.east
                )
            )

    @property
    def lower_left(self):
        return self._lower_left

    @property
    def upper_right(self):
        return self._upper_right

    @property
    def south(self):
        return self.lower_left[0]

    @property
    def west(self):
        return self.lower_left[1]

    @property
    def north(self):
        return self.upper_right[0]

    @property
    def east(self):
        return self.upper_right[1]

    def __str__(self):
        s = "[{0}, {1}]".format(self.lower_left, self.upper_right)
        return s
