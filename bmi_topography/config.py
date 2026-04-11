"""Utility functions for loading a bmi-topography configuration from a YAML file."""

import yaml

from .errors import BadConfigFileError


def load_config(config_file):
    """Load Topography parameters from a YAML config file.

    The file is expected to have a top-level ``bmi-topography`` key whose
    value is a mapping of parameter names to values.

    Parameters
    ----------
    config_file : str or path-like
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Mapping of parameter names recognised by :class:`~bmi_topography.Topography`.

    Raises
    ------
    BadConfigFileError
        If the file cannot be read or does not contain the expected key.
    """
    with open(config_file) as fp:
        raw = yaml.safe_load(fp)

    if not isinstance(raw, dict) or "bmi-topography" not in raw:
        raise BadConfigFileError(
            f"Config file '{config_file}' must contain a top-level 'bmi-topography' key.",
        )

    return raw["bmi-topography"]
