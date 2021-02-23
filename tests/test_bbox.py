"""Test BoundingBox class"""
import pytest

from bmi_topography import BoundingBox, Topography

VALID_LL = (Topography.DEFAULT["south"], Topography.DEFAULT["west"])
VALID_UR = (Topography.DEFAULT["north"], Topography.DEFAULT["east"])


def test_valid_bbox():
    BoundingBox(VALID_LL, VALID_UR)


def test_lower_left_not_iterable():
    with pytest.raises(ValueError):
        BoundingBox(0, VALID_UR)


def test_lower_left_not_coordinate_pair():
    with pytest.raises(ValueError):
        BoundingBox([0], VALID_UR)


def test_upper_right_not_iterable():
    with pytest.raises(ValueError):
        BoundingBox(VALID_LL, 0)


def test_upper_right_not_coordinate_pair():
    with pytest.raises(ValueError):
        BoundingBox(VALID_LL, [0])


def test_south_out_of_range():
    with pytest.raises(ValueError):
        BoundingBox((400, 0), VALID_UR)


def test_north_out_of_range():
    with pytest.raises(ValueError):
        BoundingBox(VALID_LL, (400, 0))


def test_south_greater_than_north():
    with pytest.raises(ValueError):
        BoundingBox((90, 0), (0, 0))


def test_west_out_of_range():
    with pytest.raises(ValueError):
        BoundingBox((0, 400), VALID_UR)


def test_east_out_of_range():
    with pytest.raises(ValueError):
        BoundingBox(VALID_LL, (0, 400))


def test_west_greater_than_east():
    with pytest.raises(ValueError):
        BoundingBox((0, 90), (0, 0))
