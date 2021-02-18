"""Test Topography class"""
import pytest

from bmi_topography import Topography

from . import VALID_LL, VALID_UR

API_URL = "https://portal.opentopography.org/API/globaldem"
DEM_TYPE = "SRTMGL3"
OUTPUT_FORMAT = "GTiff"


def test_data_url():
    r = Topography.data_url()
    assert r == API_URL


def test_invalid_dem_type():
    with pytest.raises(ValueError):
        Topography(dem_type="foo", output_format=OUTPUT_FORMAT)


def test_invalid_output_format():
    with pytest.raises(ValueError):
        Topography(dem_type=DEM_TYPE, output_format="foo")


def test_valid_bbox():
    topo = Topography(
        dem_type=DEM_TYPE,
        output_format=OUTPUT_FORMAT,
        south=VALID_LL[0],
        west=VALID_LL[1],
        north=VALID_UR[0],
        east=VALID_UR[1],
    )
    assert topo.bbox.south == VALID_LL[0]
    assert topo.bbox.west == VALID_LL[1]
    assert topo.bbox.north == VALID_UR[0]
    assert topo.bbox.east == VALID_UR[1]
    assert topo.bbox.south < topo.bbox.north
    assert topo.bbox.west < topo.bbox.east
