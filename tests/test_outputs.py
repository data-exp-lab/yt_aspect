import yt
import yt_aspect  # NOQA
from yt.testing import assert_array_equal, assert_equal


_node_names = ("velocity", "p", "T")
box_convect = "aspect/tests/shell_2d/solution/solution-00002.pvtu"


def test_2d_pvtu_load():
    ds = yt.load(box_convect)
    assert_equal(str(ds), "solution-00002.pvtu")
    assert_equal(ds.dimensionality, 2)
    assert_equal(len(ds.parameters["vtu_files"]), 5)
    assert_array_equal(ds.parameters["nod_names"], _node_names)
