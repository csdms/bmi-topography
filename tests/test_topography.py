"""Test Topography class"""

import os
import random
from pathlib import Path

import pytest
import requests

from bmi_topography import Topography
from bmi_topography.api_key import ApiKey
from bmi_topography.errors import BoundingBoxError

CENTER_LAT = 40.0
CENTER_LON = -105.0
WIDTH = 0.01


def test_invalid_dem_type():
    with pytest.raises(ValueError):
        Topography(dem_type="foo", output_format=Topography.DEFAULT["output_format"])


def test_default_output_format():
    params = Topography.DEFAULT.copy()
    params.pop("output_format")
    assert "output_format" not in params.keys()

    topo = Topography(**params)
    assert topo.output_format == "GTiff"


def test_invalid_output_format():
    with pytest.raises(ValueError):
        Topography(dem_type=Topography.DEFAULT["dem_type"], output_format="foo")


def test_missing_bbox():
    params = Topography.DEFAULT.copy()
    with pytest.raises(BoundingBoxError):
        Topography(params["dem_type"])


def test_incomplete_bbox():
    params = Topography.DEFAULT.copy()
    with pytest.raises(BoundingBoxError):
        Topography(params["dem_type"], south=CENTER_LAT, east=CENTER_LON)


def test_valid_bbox():
    params = Topography.DEFAULT.copy()
    topo = Topography(**params)

    assert topo.bbox.south == Topography.DEFAULT["south"]
    assert topo.bbox.west == Topography.DEFAULT["west"]
    assert topo.bbox.north == Topography.DEFAULT["north"]
    assert topo.bbox.east == Topography.DEFAULT["east"]
    assert topo.bbox.south < topo.bbox.north
    assert topo.bbox.west < topo.bbox.east


@pytest.mark.parametrize("cache_dir", (".", "./cache"))
def test_cache_dir(tmpdir, cache_dir):
    with tmpdir.as_cwd():
        params = Topography.DEFAULT.copy()
        params["cache_dir"] = cache_dir
        topo = Topography(**params)

        assert topo.cache_dir.is_absolute()
        assert list(topo.cache_dir.glob("*.tif")) == []


def test_cached_data(tmpdir, shared_datadir):
    with tmpdir.as_cwd():
        params = Topography.DEFAULT.copy()
        params["cache_dir"] = shared_datadir
        Topography(**params)

        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".tif")) == 0


def test_clear_cache(tmpdir):
    with tmpdir.as_cwd():
        dem_file = []
        for fext in Topography.VALID_OUTPUT_FORMATS.values():
            dem_file.append(Path(f"foo.{fext}"))

        for file in dem_file:
            file.touch()

        for file in dem_file:
            assert file.is_file()
        Topography.clear_cache(tmpdir)
        for file in dem_file:
            assert not file.is_file()


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
@pytest.mark.parametrize("dem_type", Topography.VALID_DEM_TYPES)
def test_fetch(dem_type):
    params = Topography.DEFAULT.copy()
    params["dem_type"] = dem_type
    params["west"] = CENTER_LON - WIDTH
    params["east"] = CENTER_LON + WIDTH
    params["north"] = CENTER_LAT + WIDTH
    params["south"] = CENTER_LAT - WIDTH
    params["api_key"] = ApiKey.INVALID_TEST_API_KEY

    topo = Topography(**params)

    with pytest.raises(requests.exceptions.HTTPError) as error:
        topo.fetch()

    assert error.value.response.status_code == 401
    assert ApiKey.INVALID_TEST_API_KEY in error.value.response.url
    assert topo._api_key.is_invalid_test_key() is True


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
def test_fetch_load_default(tmpdir):
    with tmpdir.as_cwd():
        topo = Topography(**Topography.DEFAULT)
        topo.fetch()
        topo.load()
        assert topo.da is not None
        assert topo.da.attrs["units"] == "degrees"


def _fetch_load(tmpdir, dem_type, output_format, file_type):
    scale_factor = 1.0
    lat = CENTER_LAT
    lon = CENTER_LON
    match dem_type:
        case "GEDI_L3":
            scale_factor = 100.0
        case "GEBCOIceTopo" | "GEBCOSubIceTopo":
            scale_factor = 50.0
        case "EU_DTM":
            lat = 52.0
            lon = 4.0
        case "CA_MRDEM_DSM" | "CA_MRDEM_DTM":
            lat = 44.5
            lon = -63.5
        case _:
            pass

    with tmpdir.as_cwd():
        topo = Topography(
            dem_type=dem_type,
            output_format=output_format,
            south=lat - WIDTH * scale_factor,
            west=lon - WIDTH * scale_factor,
            north=lat + WIDTH * scale_factor,
            east=lon + WIDTH * scale_factor,
            cache_dir=".",
        )
        topo.fetch()
        assert len(tmpdir.listdir(fil=lambda f: f.ext == "." + file_type)) == 1

        topo.load()
        assert topo.da is not None
        assert topo.da.name == dem_type
        assert topo.da.attrs["units"] is not None


@pytest.mark.skip(reason="too many downloads from OT server")
@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
@pytest.mark.parametrize("dem_type", Topography.VALID_DEM_TYPES)
@pytest.mark.parametrize(
    "output_format,file_type", Topography.VALID_OUTPUT_FORMATS.items()
)
def test_fetch_load(tmpdir, dem_type, output_format, file_type):
    _fetch_load(tmpdir, dem_type, output_format, file_type)


dem_types = [*Topography.VALID_DEM_TYPES]
dem_types.remove("USGS1m")  # academic use only
n_samples = 4
dem_types_sample = random.sample(dem_types, n_samples)


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
@pytest.mark.parametrize("dem_type", dem_types_sample)
def test_fetch_load_sample(tmpdir, dem_type):
    output_format, file_type = random.choice(
        list(Topography.VALID_OUTPUT_FORMATS.items())
    )
    _fetch_load(tmpdir, dem_type, output_format, file_type)
