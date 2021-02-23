"""Command-line interface for bmi-topography """
import click

from .topography import Topography


@click.command()
@click.version_option()
@click.option("-q", "--quiet", is_flag=True, help="Enables quiet mode.")
@click.option(
    "--dem_type",
    type=click.Choice(Topography.VALID_DEM_TYPES, case_sensitive=True),
    default=Topography.DEFAULT["dem_type"],
    help="The global raster dataset.",
    show_default=True,
)
@click.option(
    "--south",
    type=click.FloatRange(-90, 90),
    default=Topography.DEFAULT["south"],
    help="WGS 84 bounding box south coordinate, in degrees, on [-90,90].",
    show_default=True,
)
@click.option(
    "--north",
    type=click.FloatRange(-90, 90),
    default=Topography.DEFAULT["north"],
    help="WGS 84 bounding box north coordinate, in degrees, on [-90,90].",
    show_default=True,
)
@click.option(
    "--west",
    type=click.FloatRange(-180, 180),
    default=Topography.DEFAULT["west"],
    help="WGS 84 bounding box west coordinate, in degrees, on [-180,180].",
    show_default=True,
)
@click.option(
    "--east",
    type=click.FloatRange(-180, 180),
    default=Topography.DEFAULT["east"],
    help="WGS 84 bounding box east coordinate, in degrees, on [-180,180].",
    show_default=True,
)
@click.option(
    "--output_format",
    type=click.Choice(Topography.VALID_OUTPUT_FORMATS, case_sensitive=True),
    default=Topography.DEFAULT["output_format"],
    help="Output file format.",
    show_default=True,
)
@click.option("--no_fetch", is_flag=True, help="Do not fetch data from server.")
def main(quiet, dem_type, south, north, west, east, output_format, no_fetch):
    """Fetch and cache Shuttle Radar Topography Mission (SRTM) elevation data"""
    topo = Topography(dem_type, south, north, west, east, output_format)
    if not no_fetch:
        if not quiet:
            click.secho("Fetching data...", fg="yellow")
        topo.fetch()
        if not quiet:
            click.secho(
                "File downloaded to {}".format(getattr(topo, "cache_dir")), fg="green"
            )
