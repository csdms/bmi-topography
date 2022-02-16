"""Test bmi-topography command-line interface"""
import pathlib

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


def test_defaults():
    runner = CliRunner()
    result = runner.invoke(main, ["--quiet"])
    assert pathlib.Path(result.output.strip()).is_file()
    assert result.exit_code == 0


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
