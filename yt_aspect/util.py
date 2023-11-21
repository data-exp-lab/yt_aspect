from typing import Tuple

try:
    from defusedexpat.pyexpat import ExpatError  # noqa: F401
except ImportError:
    from xml.parsers.expat import ExpatError  # noqa: F401
import base64
import zlib

import numpy as np

type_decider = {"Float32": "<f4", "Float64": "<f8"}


def decode_piece(xmlPiece):
    coord_type = type_decider[xmlPiece["Points"]["DataArray"]["@type"]]

    _, coords = decode_binary(
        xmlPiece["Points"]["DataArray"]["#text"].encode(), dtype=coord_type
    )
    _, conn = decode_binary(
        xmlPiece["Cells"]["DataArray"][0]["#text"].encode(), dtype="u4"
    )
    _, offsets = decode_binary(
        xmlPiece["Cells"]["DataArray"][1]["#text"].encode(), dtype="u4"
    )
    _, cell_types = decode_binary(
        xmlPiece["Cells"]["DataArray"][2]["#text"].encode(), dtype="u1"
    )

    coords = coords.reshape((coords.size // 3, 3))

    return coords, conn, offsets, cell_types


def decode_binary(blob, use_zlib=True, dtype="<f4"):
    split_location = blob.find(b"==") + 2
    first = base64.decodebytes(blob[:split_location])
    second = base64.decodebytes(blob[split_location:])
    if use_zlib:
        second = zlib.decompress(second)
    return np.frombuffer(first, dtype="<f4"), np.frombuffer(second, dtype=dtype)


def _recursive_key_check(dict_inst: dict, nested_key_list: list) -> bool:
    key_len = len(nested_key_list)
    if key_len == 0:
        raise ValueError("nested_key_list must have at least 1 element")

    c_key = nested_key_list[0]  # the current key
    if key_len == 1:
        # at the final level
        return c_key in dict_inst
    else:
        if c_key in dict_inst and isinstance(dict_inst[c_key], dict):
            # go deeper
            return _recursive_key_check(dict_inst[c_key], nested_key_list[1:])
        else:
            # either the key DNE or the next level is not another
            # dictionary, in which case the next keys cannot exist
            return False


def _valid_element_mask(conn: np.ndarray) -> Tuple[np.ndarray, int]:
    # consider an element invalid if all of the node indices are identical
    # conn here should be the 2D connectivity array
    #   conn[0, :] = the node indices of the first element
    #   conn[:, 0] = the first node of all the elements

    first_node = conn[:, 0]
    n_elements, nodes_per_cell = conn.shape

    first_nodes = np.repeat(first_node[:, np.newaxis], nodes_per_cell, axis=1)
    valid_element_mask = np.any(conn != first_nodes, axis=1)
    n_invalid = n_elements - np.sum(valid_element_mask)

    return valid_element_mask, n_invalid
