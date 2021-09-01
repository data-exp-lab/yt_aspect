# yt_aspect

This package is a plugin for [yt](https://yt-project.org) that adds a frontend for [ASPECT](https://aspect.geodynamics.org/) unstructured mesh output.

## Installation

Use pip to install:

```
pip install yt_aspect
```

## Usage

To load a single timestep:

```python
import yt
import yt_aspect

ds = yt.load('output_convection_box_3d/solution/solution-00000.pvtu')
```

