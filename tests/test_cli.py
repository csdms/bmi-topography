"""Test bmi-topography command-line interface"""

import os
import pathlib
import stat
import sys

import pytest
from click.testing import CliRunner

from bmi_topography.cli import main


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
def test_defaults():
    runner = CliRunner()
    result = runner.invoke(main, ["--quiet"])
    assert pathlib.Path(result.output.strip()).is_file()
    assert result.exit_code == 0


@pytest.mark.skipif("NO_FETCH" in os.environ, reason="NO_FETCH is set")
def test_quiet():
    runner = CliRunner()
    quiet_lines = runner.invoke(main, ["--quiet"]).output.splitlines()
    verbose_lines = runner.invoke(main).output.splitlines()

    assert len(verbose_lines) > len(quiet_lines)


def test_demtype_valid():
    runner = CliRunner()
    result = runner.invoke(main, ["--dem-type=SRTMGL1", "--no-fetch"])
    assert result.exit_code == 0


def test_demtype_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ["--dem-type=foobar"])
    assert result.exit_code != 0


def test_demtype_is_case_sensitive():
    runner = CliRunner()
    result = runner.invoke(main, ["--dem-type=srtmgl1"])
    assert result.exit_code != 0


def test_south_inrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--south=-90.0", "--no-fetch"])
    assert result.exit_code == 0


def test_south_outrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--south=200.0"])
    assert result.exit_code != 0


def test_north_inrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--north=90.0", "--no-fetch"])
    assert result.exit_code == 0


def test_north_outrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--north=200.0"])
    assert result.exit_code != 0


def test_west_inrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--west=-180.0", "--no-fetch"])
    assert result.exit_code == 0


def test_west_outrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--west=400.0"])
    assert result.exit_code != 0


def test_east_inrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--east=180.0", "--no-fetch"])
    assert result.exit_code == 0


def test_east_outrange():
    runner = CliRunner()
    result = runner.invoke(main, ["--east=400.0"])
    assert result.exit_code != 0


def test_output_format_valid():
    runner = CliRunner()
    result = runner.invoke(main, ["--output-format=GTiff", "--no-fetch"])
    assert result.exit_code == 0


def test_output_format_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ["--output-format=foobar"])
    assert result.exit_code != 0


def test_output_format_is_case_sensitive():
    runner = CliRunner()
    result = runner.invoke(main, ["--output-format=gtiff"])
    assert result.exit_code != 0


@pytest.mark.filterwarnings("error:::bmi_topography.api_key")
def test_api_key_is_used():
    runner = CliRunner()
    result = runner.invoke(main, ["--api-key=foobar", "--no-fetch"])
    assert result.exit_code == 0


@pytest.mark.skipif(sys.platform == "win32", reason="no read-only on Windows")
def test_cache_dir_is_readonly(tmpdir):
    readonly_dir = tmpdir.mkdir("readonly")
    readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)  # r-x, no write

    try:
        runner = CliRunner()
        result = runner.invoke(main, ["--cache-dir=" + str(readonly_dir), "--no-fetch"])
        assert result.exit_code != 0
        assert "not writable" in result.output
    finally:
        readonly_dir.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)  # rwx


# ---------------------------------------------------------------------------
# --config-file tests
# ---------------------------------------------------------------------------

CONFIG_YAML = """\
bmi-topography:
  dem_type: SRTMGL3
  south: 36.738884
  north: 38.091337
  west: -120.168457
  east: -118.465576
  output_format: GTiff
  cache_dir: "."
"""


def test_config_file_no_fetch(tmp_path):
    """--config-file with --no-fetch should succeed."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(CONFIG_YAML)
    runner = CliRunner()
    result = runner.invoke(main, [f"--config-file={cfg}", "--no-fetch"])
    assert result.exit_code == 0, result.output


def test_config_file_nonexistent():
    """Passing a path that does not exist should fail."""
    runner = CliRunner()
    result = runner.invoke(main, ["--config-file=/no/such/file.yaml", "--no-fetch"])
    assert result.exit_code != 0


@pytest.mark.parametrize(
    "extra_opt",
    [
        "--dem-type=SRTMGL3",
        "--south=36.0",
        "--north=38.0",
        "--west=-120.0",
        "--east=-118.0",
        "--output-format=GTiff",
        "--cache-dir=.",
        "--api-key=foobar",
    ],
)
def test_config_file_mutually_exclusive(tmp_path, extra_opt):
    """--config-file must not be combined with any individual parameter option."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(CONFIG_YAML)
    runner = CliRunner()
    result = runner.invoke(main, [f"--config-file={cfg}", extra_opt, "--no-fetch"])
    assert result.exit_code != 0, (
        f"Expected non-zero exit when combining --config-file with {extra_opt}"
    )
