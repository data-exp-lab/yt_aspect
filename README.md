# yt_aspect

This package is a plugin for [yt](https://yt-project.org) that adds a frontend for [ASPECT](https://aspect.geodynamics.org/) unstructured mesh output. Currently in initial testing...

## Installation

Use pip to install:

```
pip install yt-aspect
```

To install a development version,  clone this repository, `cd` into the clone and then install locally with

```
pip install -e .
```

A number of dependencies will be installed for you, including `yt` if you don't already have it. 

## Usage

To load a single timestep:

```python
import yt
import yt_aspect

ds = yt.load('output_convection_box_3d/solution/solution-00000.pvtu')
```

From there, you can work with the dataset as a normal yt dataset (though not all functionality will work -- open an issue [here](https://github.com/chrishavlin/yt_aspect/issues) if something you need doesn't work!). Until there are ASPECT specific examples in this repository, check out the [main yt documentation](https://yt-project.org/doc/) for examples.

## Bugs and Requests
This is still in an experimental stage, so you will likely find bugs and missing features! Feel free to [open an issue](https://github.com/chrishavlin/yt_aspect/issues), contact me via [slack](https://yt-project.slack.com/) or submit pull requests (development guidelines will emerge and will likely mirror yt, but nothing is set yet). 
