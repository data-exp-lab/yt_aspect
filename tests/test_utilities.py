import numpy as np
import pytest
from packaging.version import Version

from yt_aspect._utilities import yt_is, yt_version, yt_version_string
from yt_aspect.util import _valid_element_mask


@pytest.mark.parametrize("compare_str", (">", ">=", "!="))
def test_yt_version_comparison_gt(compare_str):
    assert yt_is(compare_str, "1.0.0")
    assert yt_is(compare_str, Version("1.0.0"))


@pytest.mark.parametrize("compare_str", ("<", "<="))
def test_yt_version_comparison_lt(compare_str):
    assert yt_is(compare_str, "10000.0.0")
    assert yt_is(compare_str, Version("10000.0.0"))


def test_yt_version_eq():
    assert yt_is("==", yt_version)
    assert yt_is("==", yt_version_string)


def test_yt_version_bad():
    with pytest.raises(ValueError, match="comparison string must be one of:"):
        _ = yt_is("~", Version("1.0.0"))


@pytest.mark.parametrize(
    "n_elements,nodes_per_element,n_invalid", [(5, 3, 2), (5, 8, 2), (5, 8, 0)]
)
def test_valid_element_mask(n_elements, nodes_per_element, n_invalid):
    one_element = np.arange(nodes_per_element)
    test_conn = np.repeat(one_element[:, np.newaxis], n_elements, axis=1).transpose()

    if n_invalid > 0:
        test_conn[-n_invalid:, :] = 1

    valid_elements, n_actual = _valid_element_mask(test_conn)
    assert valid_elements.sum() == n_elements - n_invalid
    assert n_actual == n_invalid
