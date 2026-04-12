"""Test the config module"""

import pytest

from bmi_topography import Topography
from bmi_topography.config import load_config
from bmi_topography.errors import BadConfigFileError

CONFIG_FILE = "config.yaml"
DEM_TYPE = "SRTMGL3"
OUTPUT_FORMAT = "GTiff"


def test_load_config(shared_datadir):
    conf = load_config(shared_datadir / CONFIG_FILE)
    assert conf["dem_type"] == DEM_TYPE
    assert conf["output_format"] == OUTPUT_FORMAT


def test_config_file_missing_key(tmp_path):
    """Config file without 'bmi-topography' key should fail with a helpful message."""
    cfg = tmp_path / "bad.yaml"
    cfg.write_text("other_key:\n  dem_type: SRTMGL3\n")
    with pytest.raises(BadConfigFileError):
        load_config(cfg)


def test_set_default_config():
    conf = Topography.DEFAULT.copy()
    assert conf["dem_type"] == DEM_TYPE
    assert conf["output_format"] == OUTPUT_FORMAT


def test_pass_config_parameters():
    conf = Topography.DEFAULT.copy()
    topo = Topography(**conf)
    assert topo.dem_type == DEM_TYPE
    assert topo.output_format == OUTPUT_FORMAT
