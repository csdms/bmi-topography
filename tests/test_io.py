"""Test the io module"""

from bmi_topography import Topography
from bmi_topography.io import load_config

CONFIG_FILE = "config.yaml"
DEM_TYPE = "SRTMGL3"
OUTPUT_FORMAT = "GTiff"


def test_load_config(shared_datadir):
    conf = load_config(shared_datadir / CONFIG_FILE)
    assert conf["dem_type"] == DEM_TYPE
    assert conf["output_format"] == OUTPUT_FORMAT


def test_set_default_config():
    conf = Topography.DEFAULT.copy()
    assert conf["dem_type"] == DEM_TYPE
    assert conf["output_format"] == OUTPUT_FORMAT


def test_pass_config_parameters():
    conf = Topography.DEFAULT.copy()
    topo = Topography(**conf)
    assert topo.dem_type == DEM_TYPE
    assert topo.output_format == OUTPUT_FORMAT
