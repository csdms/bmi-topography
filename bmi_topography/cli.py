"""Command-line interface for bmi-topography"""

import click

from .config import load_config
from .topography import Topography

# Names of options that are mutually exclusive with --config-file
_CONFIG_FILE_EXCLUSIVE = {
    "dem_type",
    "south",
    "north",
    "west",
    "east",
    "output_format",
    "cache_dir",
    "api_key",
}


# Based on https://stackoverflow.com/a/37491504/1563298.
class MutuallyExclusiveOption(click.Option):
    """A Click option that is mutually exclusive with --config-file."""

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive_with = kwargs.pop("mutually_exclusive_with", [])
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current = self.name in opts and opts[self.name] is not None
        for mutex_opt in self.mutually_exclusive_with:
            if mutex_opt in opts and opts[mutex_opt] is not None:
                if current:
                    raise click.UsageError(
                        f"'--{self.name.replace('_', '-')}' cannot be used together "
                        f"with '--{mutex_opt.replace('_', '-')}'."
                    )
        return super().handle_parse_result(ctx, opts, args)


@click.command()
@click.version_option()
@click.option("-q", "--quiet", is_flag=True, help="Enables quiet mode.")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    default=None,
    help=(
        "Path to a YAML configuration file. "
        "Mutually exclusive with --dem-type, --south, --north, --west, --east, "
        "--output-format, --cache-dir, and --api-key."
    ),
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=list(_CONFIG_FILE_EXCLUSIVE),
)
@click.option(
    "--dem-type",
    type=click.Choice(Topography.VALID_DEM_TYPES, case_sensitive=True),
    default=None,
    help="The global raster dataset.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--south",
    type=click.FloatRange(-90, 90),
    default=None,
    help="WGS 84 bounding box south coordinate, in degrees.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--north",
    type=click.FloatRange(-90, 90),
    default=None,
    help="WGS 84 bounding box north coordinate, in degrees.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--west",
    type=click.FloatRange(-180, 180),
    default=None,
    help="WGS 84 bounding box west coordinate, in degrees.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--east",
    type=click.FloatRange(-180, 180),
    default=None,
    help="WGS 84 bounding box east coordinate, in degrees.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--output-format",
    type=click.Choice(Topography.VALID_OUTPUT_FORMATS.keys(), case_sensitive=True),
    default=None,
    help="Output file format.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--cache-dir",
    type=click.Path(
        exists=False, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
    default=None,
    help="Directory to store data files downloaded from OpenTopography.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="OpenTopography API key.",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive_with=["config_file"],
)
@click.option("--no-fetch", is_flag=True, help="Do not fetch data from server.")
def main(
    quiet,
    config_file,
    dem_type,
    south,
    north,
    west,
    east,
    output_format,
    cache_dir,
    api_key,
    no_fetch,
):
    """Fetch and cache land elevation data from OpenTopography

    Some datasets require an OpenTopography API key. You can find instructions
    on how to obtain one from the OpenTopography website:

        https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets

    Once you have a key, you can pass it to the `bmi-topography`
    command in one of three ways: 1) through the environment variable
    OPENTOPOGRAPHY_API_KEY, or 2) as the contents of the file
    ".opentopography.txt" located either in your current directory or your home
    directory, or 3) through the `--api-key` option.
    """
    if config_file is not None:
        params = load_config(config_file)
    else:
        defaults = Topography.DEFAULT
        params = {
            "dem_type": dem_type if dem_type is not None else defaults["dem_type"],
            "south": south if south is not None else defaults["south"],
            "north": north if north is not None else defaults["north"],
            "west": west if west is not None else defaults["west"],
            "east": east if east is not None else defaults["east"],
            "output_format": (
                output_format
                if output_format is not None
                else defaults["output_format"]
            ),
            "cache_dir": cache_dir if cache_dir is not None else defaults["cache_dir"],
            "api_key": api_key,
        }

    topo = Topography(**params)

    if not no_fetch:
        if not quiet:
            click.secho("Fetching data...", fg="yellow", err=True)
        path_to_dem = topo.fetch()
        if not quiet:
            click.secho(
                f"File downloaded to {getattr(topo, 'cache_dir')}",
                fg="green",
                err=True,
            )
        print(path_to_dem)
