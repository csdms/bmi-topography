"""Command-line interface for bmi-topography """
import click

from .topography import Topography


@click.command()
@click.version_option()
@click.option(
    "--dem_type",
    type=click.Choice(["SRTMGL3", "SRTMGL1", "SRTMGL1_E"], case_sensitive=False),
    default="SRTMGL3",
    help="The global raster dataset.",
    show_default="SRTMGL3",
)
@click.option(
    "--south",
    type=click.FloatRange(-90, 90),
    default=36.738884,
    help="WGS 84 bounding box south coordinate, in degrees, on [-90,90].",
    show_default=36.738884,
)
@click.option(
    "--north",
    type=click.FloatRange(-90, 90),
    default=38.091337,
    help="WGS 84 bounding box north coordinate, in degrees, on [-90,90].",
    show_default=38.091337,
)
@click.option(
    "--west",
    type=click.FloatRange(-180, 180),
    default=-120.168457,
    help="WGS 84 bounding box west coordinate, in degrees, on [-180,180].",
    show_default=-120.168457,
)
@click.option(
    "--east",
    type=click.FloatRange(-180, 180),
    default=-118.465576,
    help="WGS 84 bounding box east coordinate, in degrees, on [-180,180].",
    show_default=-118.465576,
)
@click.option(
    "--output_format",
    type=click.Choice(["GeoTiff", "AAIGrid", "HFA"], case_sensitive=False),
    default="GeoTiff",
    help="Output file format.",
    show_default="GeoTiff",
)
def main(dem_type, south, north, west, east, output_format):
    """Fetch and cache Shuttle Radar Topography Mission (SRTM) elevation data"""
    Topography.run()
    print(dem_type)
    print(south)
    print(north)
    print(west)
    print(east)
    print(output_format)
