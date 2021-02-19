"""Test Topography class"""
import pytest

from bmi_topography import Topography, DEFAULT

API_URL = "https://portal.opentopography.org/API/globaldem"


def test_data_url():
    r = Topography.data_url()
    assert r == API_URL


def test_invalid_dem_type():
    with pytest.raises(ValueError):
        Topography(dem_type="foo", output_format=DEFAULT["output_format"])


def test_invalid_output_format():
    with pytest.raises(ValueError):
        Topography(dem_type=DEFAULT["dem_type"], output_format="foo")


def test_valid_bbox():
    topo = Topography(
        dem_type=DEFAULT["dem_type"],
        output_format=DEFAULT["output_format"],
        south=DEFAULT["south"],
        west=DEFAULT["west"],
        north=DEFAULT["north"],
        east=DEFAULT["east"],
   )
    assert topo.bbox.south == DEFAULT["south"]
    assert topo.bbox.west == DEFAULT["west"]
    assert topo.bbox.north == DEFAULT["north"]
    assert topo.bbox.east == DEFAULT["east"]
    assert topo.bbox.south < topo.bbox.north
    assert topo.bbox.west < topo.bbox.east
