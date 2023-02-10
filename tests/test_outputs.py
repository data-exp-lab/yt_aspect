import os

import pytest
import unyt
import yt

import yt_aspect  # NOQA


def get_file_path_from_data_info(dataset_type, data_info_dict, dataset_name):
    ds_info = data_info_dict[dataset_type][dataset_name]
    final_folder = os.path.split(ds_info["archive_path"])[-1]
    fi_dir = os.path.join(
        data_info_dict["base_dir"],
        ds_info["archive_path"],
        final_folder,
        ds_info["relative_unpacked_path"],
    )
    full_file = os.path.join(fi_dir, ds_info["sample_file"])
    return full_file


@pytest.mark.parametrize(
    "dataset_type, dataset_name",
    (
        ("ASPECT", "cartesian_3D_nproc4"),
        ("ASPECT", "cartesian_3D_nproc1"),
        ("PVTU", "cleaned_aspect"),
    ),
)
def test_3d_aspect_load(pvtu_test_data, dataset_type, dataset_name, tmp_path):

    fi = get_file_path_from_data_info(dataset_type, pvtu_test_data, dataset_name)

    if os.path.isfile(fi) is False:
        pytest.skip(f"Could not locate {fi}")

    ds = yt.load(fi)
    assert ds.dataset_type == dataset_type.lower()
    assert ds.dimensionality == 3

    ad = ds.all_data()
    T = ad[("connect0", "T")][0]
    if dataset_type == "ASPECT":
        assert T.units == unyt.K

    _ = ad[("connect0", "velocity_x")][0]

    outfi = tmp_path / "test.png"
    slc = yt.SlicePlot(ds, "x", ("connect0", "T"))
    slc.save(outfi)
    assert os.path.isfile(outfi)
