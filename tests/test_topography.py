"""Test Topography class"""
import os

import pytest

from bmi_topography import Topography

API_URL = "https://portal.opentopography.org/API/globaldem"
CENTER_LAT = 40.0
CENTER_LON = -105.0
WIDTH = 0.01


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


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
@pytest.mark.parametrize("dem_type", Topography.VALID_DEM_TYPES)
@pytest.mark.parametrize(
    "output_format,file_type", Topography.VALID_OUTPUT_FORMATS.items()
)
def test_fetch(tmpdir, dem_type, output_format, file_type):
    with tmpdir.as_cwd():
        topo = Topography(
            dem_type=dem_type,
            output_format=output_format,
            south=CENTER_LAT - WIDTH,
            west=CENTER_LON - WIDTH,
            north=CENTER_LAT + WIDTH,
            east=CENTER_LON + WIDTH,
            cache_dir=".",
        )
        topo.fetch()
        assert len(tmpdir.listdir(fil=lambda f: f.ext == "." + file_type)) == 1


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
        assert topo.da is not None
        assert topo.da.attrs["units"] == "degrees"
