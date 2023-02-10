import os
import shutil
import tarfile

import pytest
import tomli


@pytest.fixture(scope="session", autouse=True)
def pvtu_test_data():

    data_info_file = "yt_aspect/_pvtu_test_data/data.toml"
    with open(data_info_file, "rb") as f:
        data_info = tomli.load(f)

    base_dir = os.path.join("yt_aspect", "_pvtu_test_data")
    archives_to_unpack = set()
    for datasets in data_info.values():
        for dataset in datasets.values():
            archive = dataset["archive_path"] + dataset["archive_ext"]
            archives_to_unpack.add(os.path.join(base_dir, archive))

    remove_folders = []
    for archive in archives_to_unpack:
        outfolder = archive.split(".tar")[0]
        print(outfolder)
        if os.path.isdir(outfolder) is False:
            with tarfile.open(archive) as tar:
                tar.extractall(path=outfolder)
            remove_folders.append(outfolder)

    data_info["base_dir"] = base_dir
    yield data_info

    for folder in remove_folders:
        shutil.rmtree(folder)
