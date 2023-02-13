from typing import Union

from packaging.version import Version
from yt import __version__ as yt_version_string

yt_version = Version(yt_version_string)


def yt_is(comparison: str, test_version: Union[Version, str]) -> bool:
    # check if yt version is less than
    if isinstance(test_version, str):
        test_version = Version(test_version)

    if comparison == "<":
        return yt_version < test_version
    elif comparison == "<=":
        return yt_version <= test_version
    if comparison == ">":
        return yt_version > test_version
    elif comparison == ">=":
        return yt_version >= test_version
    if comparison == "!=":
        return yt_version != test_version
    elif comparison == "==":
        return yt_version == test_version
    else:
        raise ValueError("comparison string must be one of: <, <=, >, >=, !=, ==")
