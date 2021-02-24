"""Test config file"""
import yaml

from bmi_topography import Topography

CONFIG_FILE = "config.yaml"
DEM_TYPE = "SRTMGL3"
OUTPUT_FORMAT = "GTiff"


def test_read_config(shared_datadir):
    with open(shared_datadir / CONFIG_FILE, "r") as fp:
        conf = yaml.safe_load(fp).get("bmi-topography", {})
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
