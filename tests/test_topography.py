"""Test Topography class"""
import numpy
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


@pytest.mark.parametrize("cache_dir", (".", "./cache"))
def test_cache_dir(tmpdir, cache_dir):
    with tmpdir.as_cwd():
        topo = Topography(
            dem_type=Topography.DEFAULT["dem_type"],
            output_format=Topography.DEFAULT["output_format"],
            south=Topography.DEFAULT["south"],
            west=Topography.DEFAULT["west"],
            north=Topography.DEFAULT["north"],
            east=Topography.DEFAULT["east"],
            cache_dir=cache_dir,
        )
        assert topo.cache_dir.is_absolute()
        assert list(topo.cache_dir.glob("*.tif")) == []


def test_cached_data(tmpdir, shared_datadir):
    with tmpdir.as_cwd():
        Topography(
            dem_type=Topography.DEFAULT["dem_type"],
            output_format=Topography.DEFAULT["output_format"],
            south=Topography.DEFAULT["south"],
            west=Topography.DEFAULT["west"],
            north=Topography.DEFAULT["north"],
            east=Topography.DEFAULT["east"],
            cache_dir=shared_datadir,
        )
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".tif")) == 0


def test_fetch(tmpdir):
    new_south = numpy.mean([Topography.DEFAULT["south"], Topography.DEFAULT["north"]])
    new_west = numpy.mean([Topography.DEFAULT["west"], Topography.DEFAULT["east"]])
    with tmpdir.as_cwd():
        topo = Topography(
            dem_type=Topography.DEFAULT["dem_type"],
            output_format=Topography.DEFAULT["output_format"],
            south=new_south,
            west=new_west,
            north=Topography.DEFAULT["north"],
            east=Topography.DEFAULT["east"],
            cache_dir=".",
        )
        topo.fetch()
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".tif")) == 1


def test_load(tmpdir, shared_datadir):
    with tmpdir.as_cwd():
        topo = Topography(
            dem_type=Topography.DEFAULT["dem_type"],
            output_format=Topography.DEFAULT["output_format"],
            south=Topography.DEFAULT["south"],
            west=Topography.DEFAULT["west"],
            north=Topography.DEFAULT["north"],
            east=Topography.DEFAULT["east"],
            cache_dir=shared_datadir,
        )
        topo.load()
        assert topo.dataarray is not None
