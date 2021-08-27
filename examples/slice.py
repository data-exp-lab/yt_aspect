import yt

import yt_aspect  # noqa: F401

files = [
    "aspect/output_convection_box_3d/nproc_1/solution/solution-00002.pvtu",
    "aspect/output_convection_box_3d/nproc_4/solution/solution-00001.pvtu",
    "aspect/output_shell_simple_2d/solution/solution-00004.pvtu",
]


ds = yt.load(files[2])

p = yt.SlicePlot(ds, "z", "T")
p.save("test")
