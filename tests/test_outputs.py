import pytest
import yt
import unyt
import os
import yt_aspect  # NOQA
import numpy as np

_node_names = ("velocity", "p", "T")
box_convect = "aspect/tests/shell_2d/solution/solution-00002.pvtu"

def get_file_path_from_data_info(data_info_dict, dataset_name):
    ds_info = data_info_dict["ASPECT"][dataset_name]
    final_folder = os.path.split(ds_info["archive_path"])[-1]
    fi_dir = os.path.join(data_info_dict["base_dir"],
                          ds_info["archive_path"],
                          final_folder,
                          ds_info["relative_unpacked_path"])
    return fi_dir

@pytest.mark.parametrize("dataset_name", ("cartesian_3D_nproc4", "cartesian_3D_nproc1"))
def test_3d_aspect_load(pvtu_test_data, dataset_name):

    fi_dir = get_file_path_from_data_info(pvtu_test_data, dataset_name)
    fi = os.path.join(fi_dir, "solution-00002.pvtu")

    if os.path.isfile(fi) is False:
        pytest.skip(f"Could not locate {fi}")

    ds = yt.load(fi)
    assert ds.dataset_type == "aspect"
    assert ds.dimensionality == 3

    ad = ds.all_data()
    T = ad[("connect0", "T")][0]
    assert T.units == unyt.K
