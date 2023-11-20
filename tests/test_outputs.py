import os

import numpy as np
import pytest
import unyt
import yt

from yt_aspect.data_structures import _is_aspect_datafile, _is_pvtu_datafile


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
    "dataset_type, dataset_name, expected_dims",
    (
        ("ASPECT", "cartesian_3D_nproc4", 3),
        ("ASPECT", "cartesian_3D_nproc1", 3),
        ("ASPECT", "shell_2D", 2),
        ("PVTU", "cleaned_aspect", 3),
    ),
)
def test_3d_aspect_load(
    pvtu_test_data, dataset_type, dataset_name, expected_dims, tmp_path
):
    fi = get_file_path_from_data_info(dataset_type, pvtu_test_data, dataset_name)

    if os.path.isfile(fi) is False:
        pytest.skip(f"Could not locate {fi}")

    ds = yt.load(fi)
    assert ds.dataset_type == dataset_type.lower()
    assert ds.dimensionality == expected_dims

    ad = ds.all_data()
    T = ad[("connect0", "T")][0]
    if dataset_type == "ASPECT":
        assert T.units == unyt.K

    _ = ad[("connect0", "velocity_x")][0]

    outfi = tmp_path / "test.png"
    slc = yt.SlicePlot(ds, "z", ("connect0", "T"))
    slc.save(outfi)
    assert os.path.isfile(outfi)


def _get_slice_frb(ds):
    slc = yt.SlicePlot(ds, "z", ("connect0", "Temperature2"))
    slc._setup_plots()
    return slc.frb[("connect0", "Temperature2")]


def test_element_validation(pvtu_test_data):
    # this sample ds does not include null elements... so not a great test.
    fi = get_file_path_from_data_info("PVTU", pvtu_test_data, "two2_with_invalid_els")
    ds_1 = yt.load(fi, detect_null_elements=True)
    frb_1 = _get_slice_frb(ds_1)
    n_finite_no_null = np.isfinite(frb_1).sum()

    ds_0 = yt.load(fi, detect_null_elements=False)
    frb_0 = _get_slice_frb(ds_0)
    n_finite_w_null = np.isfinite(frb_0).sum()

    assert n_finite_no_null > n_finite_w_null


@pytest.mark.parametrize(
    "dataset_type, dataset_name",
    (
        ("ASPECT", "cartesian_3D_nproc4"),
        ("ASPECT", "cartesian_3D_nproc1"),
        ("ASPECT", "shell_2D"),
        ("PVTU", "cleaned_aspect"),
    ),
)
def test_dataset_validation(pvtu_test_data, dataset_type, dataset_name):
    fi = get_file_path_from_data_info(dataset_type, pvtu_test_data, dataset_name)
    if dataset_type == "ASPECT":
        assert _is_aspect_datafile(fi)
        assert _is_pvtu_datafile(fi)
    else:
        assert _is_aspect_datafile(fi) is False
        assert _is_pvtu_datafile(fi)


def test_dataset_invalidation():
    assert _is_aspect_datafile("file/that/does/not/exist") is False
    assert _is_pvtu_datafile("file/that/does/not/exist") is False

    assert _is_aspect_datafile("file/that/looks/like/file.pvtu") is False
    assert _is_pvtu_datafile("file/that/looks/like/file.pvtu") is False
