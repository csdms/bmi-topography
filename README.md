[![Basic Model Interface](https://img.shields.io/badge/CSDMS-Basic%20Model%20Interface-green.svg)](https://bmi.readthedocs.io/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/bmi-topography.svg)](https://anaconda.org/conda-forge/bmi-topography)
[![PyPI](https://img.shields.io/pypi/v/bmi-topography)](https://pypi.org/project/bmi-topography)
[![Build/Test CI](https://github.com/csdms/bmi-topography/actions/workflows/build-test-ci.yml/badge.svg)](https://github.com/csdms/bmi-topography/actions/workflows/build-test-ci.yml)
[![Documentation Status](https://readthedocs.org/projects/bmi-topography/badge/?version=latest)](https://bmi-topography.readthedocs.io/en/latest/?badge=latest)

# bmi-topography

*bmi-topography* is a Python library for fetching and caching
land elevation data from the
NASA [Shuttle Radar Topography Mission][srtm] (SRTM)
and the
JAXA [Advanced Land Observing Satellite][alos] (ALOS)
using the [OpenTopography][ot] [REST API][ot-rest].

The *bmi-topography* library provides access to the following global raster datasets:

* SRTM GL3 (90m)
* SRTM GL1 (30m)
* SRTM GL1 (30m, Ellipsoidal)
* ALOS World 3D (30m)
* ALOS World 3D (30m, Ellipsoidal) 

The library includes an API and a CLI that accept
the dataset type,
a latitude-longitude bounding box, and
the output file format.
Data are downloaded from OpenTopography and cached locally.
The cache is checked before downloading new data.
Data from a cached file can optionally be loaded into an
[xarray][xarray] [DataArray][xarray-da]
using the experimental [open_rasterio][xarray-or] method.

The *bmi-topography* API is wrapped with a
[Basic Model Interface][bmi] (BMI),
which provides a standard set of functions for coupling with data or models
that also expose a BMI.
More information on the BMI can found in its [documentation][bmi].

## Installation

Install the latest stable release of *bmi-topography* with `pip`:
```
pip install bmi-topography
```
or with `conda`:
```
conda install -c conda-forge bmi-topography
```

The *bmi-topography* library can also be built and installed from source.
The library uses several other open source libraries,
so a convenient way of building and installing it is within a
[conda environment][conda-env].
After cloning or downloading the *bmi-topography*
[repository][bmi-topo-repo],
change into the repository directory
and set up a conda environment with the included environment file:
```
conda env create --file=environment.yml
```
Then build and install *bmi-topography* from source with
```
make install
```

## Examples

A brief example of using the *bmi-topography* API is given in the following steps.

Start a Python session and import the `Topography` class:
```python
>>> from bmi_topography import Topography
```

For convenience,
a set of default parameter values for `Topography` are included in the class definition.
Copy these and modify them with custom values:
```python
>>> params = Topography.DEFAULT.copy()
>>> params["south"] = 39.75
>>> params["north"] = 40.25
>>> params["west"] = -105.25
>>> params["east"] = -104.75
>>> params
{'dem_type': 'SRTMGL3',
 'south': 39.75,
 'north': 40.25,
 'west': -105.25,
 'east': -104.75,
 'output_format': 'GTiff',
 'cache_dir': '~/.bmi_topography'}
```
These coordinate values represent an area around Boulder, Colorado.

Make a instance of `Topography` with these parameters:
```python
>>> boulder = Topography(**params)
```
then fetch the data from OpenTopography:
```python
>>> boulder.fetch()
PosixPath('/Users/mpiper/.bmi_topography/SRTMGL3_39.75_-105.25_40.25_-104.75.tif')
```
This step might take a few moments,
and it will increase for requests of larger areas.
Note that the file has been saved to a local cache directory.

Load the data into an xarray `DataArray` for further work:
```python
>>> boulder.load()
<xarray.DataArray 'SRTMGL3' (band: 1, y: 600, x: 600)>
[360000 values with dtype=int16]
Coordinates:
  * band     (band) int64 1
  * y        (y) float64 40.25 40.25 40.25 40.25 ... 39.75 39.75 39.75 39.75
  * x        (x) float64 -105.3 -105.2 -105.2 -105.2 ... -104.8 -104.8 -104.8
Attributes:
    transform:      (0.000833333333333144, 0.0, -105.25041666668365, 0.0, -0....
    crs:            +init=epsg:4326
    res:            (0.000833333333333144, 0.000833333333333144)
    is_tiled:       1
    nodatavals:     (0.0,)
    scales:         (1.0,)
    offsets:        (0.0,)
    AREA_OR_POINT:  Area
    units:          meters
    location:       node
```

For examples with more detail,
see the two Jupyter Notebooks,
Python script, and shell script
included in the [examples][bmi-topo-examples] directory
of the *bmi-topography* repository.

User and developer documentation for *bmi-topography*
is available at https://bmi-topography.readthedocs.io.

<!-- Links (by alpha) -->

[alos]: https://www.eorc.jaxa.jp/ALOS/en/aw3d30/index.htm
[bmi]: https://bmi.readthedocs.io
[bmi-topo-examples]: https://github.com/csdms/bmi-topography/tree/main/examples
[bmi-topo-repo]: https://github.com/csdms/bmi-topography
[conda-env]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
[ot]: https://opentopography.org/
[ot-rest]: https://portal.opentopography.org/apidocs/
[srtm]: https://www2.jpl.nasa.gov/srtm/
[xarray]: http://xarray.pydata.org/en/stable/
[xarray-da]: http://xarray.pydata.org/en/stable/api.html#dataarray
[xarray-or]: http://xarray.pydata.org/en/stable/generated/xarray.open_rasterio.html#xarray.open_rasterio
