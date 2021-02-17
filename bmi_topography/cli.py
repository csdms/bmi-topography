"""Command-line interface for bmi-topography """
import click

from .topography import Topography


@click.command()
@click.version_option()
def main():
    """Fetch and cache Shuttle Radar Topography Mission (SRTM) elevation data"""
    Topography.run()
