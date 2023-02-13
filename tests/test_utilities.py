import pytest
from packaging.version import Version

from yt_aspect._utilities import yt_is, yt_version, yt_version_string


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
