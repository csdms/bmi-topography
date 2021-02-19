"""Test Topography class"""
import pytest

from bmi_topography import Topography

API_URL = "https://portal.opentopography.org/API/globaldem"


def test_data_url():
    r = Topography.data_url()
    assert r == API_URL


def test_invalid_dem_type():
    with pytest.raises(ValueError):
        Topography(dem_type="foo", output_format=Topography.DEFAULT["output_format"])


def test_invalid_output_format():
    with pytest.raises(ValueError):
        Topography(dem_type=Topography.DEFAULT["dem_type"], output_format="foo")


def test_valid_bbox():
    topo = Topography(
        dem_type=Topography.DEFAULT["dem_type"],
        output_format=Topography.DEFAULT["output_format"],
        south=Topography.DEFAULT["south"],
        west=Topography.DEFAULT["west"],
        north=Topography.DEFAULT["north"],
        east=Topography.DEFAULT["east"],
   )
    assert topo.bbox.south == Topography.DEFAULT["south"]
    assert topo.bbox.west == Topography.DEFAULT["west"]
    assert topo.bbox.north == Topography.DEFAULT["north"]
    assert topo.bbox.east == Topography.DEFAULT["east"]
    assert topo.bbox.south < topo.bbox.north
    assert topo.bbox.west < topo.bbox.east
