from collections.abc import Iterable


class BoundingBox:
    """Represent a simple latitude-longitude bounding box.

    Examples
    --------
    Create a bounding box:

    >>> from bmi_topography import BoundingBox
    >>> bbox = BoundingBox((33, 111), (44, 122))
    >>> print(bbox)
    [(33, 111), (44, 122)]

    """

    def __init__(self, lower_left: tuple[float], upper_right: tuple[float]) -> None:
        self._lower_left = lower_left
        self._upper_right = upper_right

        if not isinstance(self.lower_left, Iterable) or len(self.lower_left) != 2:
            raise ValueError(
                f"lower left coordinate ({self.lower_left}) must have two elements"
            )

        if not isinstance(self.upper_right, Iterable) or len(self.upper_right) != 2:
            raise ValueError(
                f"upper right coordinate ({self.upper_right}) must have two elements"
            )

        if self.south > 90 or self.south < -90:
            raise ValueError(f"south coordinate ({self.south}) must be in [-90,90]")

        if self.north > 90 or self.north < -90:
            raise ValueError(f"north coordinate ({self.north}) must be in [-90,90]")

        if self.south > self.north:
            raise ValueError(
                f"south coordinate ({self.south}) must be less than north ({self.north})"
            )

        if self.west > 180 or self.west < -180:
            raise ValueError(f"west coordinate ({self.west}) must be in [-180,180]")

        if self.east > 180 or self.east < -180:
            raise ValueError(f"east coordinate ({self.east}) must be in [-180,180]")

        if self.west > self.east:
            raise ValueError(
                f"west coordinate ({self.west}) must be less than east ({self.east})"
            )

    @property
    def lower_left(self):
        """The southwest corner of the box, given by tuple of *(south, west)*."""
        return self._lower_left

    @property
    def upper_right(self):
        """The northeast corner of the box, given by tuple of *(north, east)*."""
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
        s = f"[{self.lower_left}, {self.upper_right}]"
        return s
