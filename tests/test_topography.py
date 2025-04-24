"""Test Topography class"""

import os

import pytest

from bmi_topography import Topography
from bmi_topography.api_key import ApiKey

CENTER_LAT = 40.0
CENTER_LON = -105.0
WIDTH = 0.01


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


@pytest.mark.parametrize("server_name", tuple(Topography.SERVER_NAME.values()))
def test_data_url(server_name):
    if "usgs" in server_name:
        dem_type = "USGS30m"
    else:
        dem_type = "NASADEM"

    params = Topography.DEFAULT.copy()
    params["dem_type"] = dem_type
    topo = Topography(**params)

    server = Topography.SERVER_BASE + server_name
    r = topo.data_url()
    assert r == Topography.base_url() + server


@pytest.mark.parametrize("dem_type", Topography.VALID_DEM_TYPES)
def test_fetch(dem_type):
    params = Topography.DEFAULT.copy()
    params["dem_type"] = dem_type
    params["api_key"] = ApiKey.INVALID_TEST_API_KEY

    topo = Topography(**params)

    with pytest.raises(requests.exceptions.HTTPError) as error:
        topo.fetch()

    assert error.value.response.status_code == 401
    assert ApiKey.INVALID_TEST_API_KEY in error.value.response.url
    assert topo._api_key.is_invalid_test_key() is True


def test_fetch_load_default(tmpdir):
    with tmpdir.as_cwd():
        topo = Topography(**Topography.DEFAULT)
        topo.fetch()
        topo.load()
        assert topo.da is not None
        assert topo.da.attrs["units"] == "degrees"


@pytest.mark.skip(reason="disabled pending resolution of #83")
@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
@pytest.mark.parametrize("dem_type", Topography.VALID_DEM_TYPES)
@pytest.mark.parametrize(
    "output_format,file_type", Topography.VALID_OUTPUT_FORMATS.items()
)
def test_fetch_load(tmpdir, dem_type, output_format, file_type):
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

        topo.load()
        assert topo.da is not None
        assert topo.da.name == dem_type
        assert topo.da.attrs["units"] is not None
