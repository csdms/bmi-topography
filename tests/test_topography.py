"""Test Topography class"""
import pytest

from bmi_topography import Topography

API_URL = "https://portal.opentopography.org/API/globaldem"
DEM_TYPE = "SRTMGL3"
OUTPUT_FORMAT = "GTiff"
SOUTH = 36.738884
NORTH = 38.091337


def test_data_url():
    r = Topography.data_url()
    assert r == API_URL


def test_invalid_dem_type():
    with pytest.raises(ValueError):
        Topography(dem_type="foo", output_format=OUTPUT_FORMAT)


def test_invalid_output_format():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format="foo")


def test_south_out_of_range():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, south=400)


def test_north_out_of_range():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, north=-400)


def test_south_greater_than_north():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, south=20, north=10)


def test_west_out_of_range():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, west=-400)


def test_east_out_of_range():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, east=400)


def test_west_greater_than_east():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format=OUTPUT_FORMAT, west=50, east=-10)
