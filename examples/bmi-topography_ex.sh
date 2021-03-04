#! /usr/bin/env bash
# Example of downloading data through the bmi-topography CLI.

DEM_TYPE=SRTMGL3
SOUTH=36.738884
NORTH=38.091337
WEST=-120.168457
EAST=-118.465576
OUTPUT_FORMAT=GTiff

bmi-topography --version
bmi-topography --help

bmi-topography \
    --dem_type=$DEM_TYPE \
    --south=$SOUTH \
    --north=$NORTH \
    --west=$WEST \
    --east=$EAST \
    --output_format=$OUTPUT_FORMAT
