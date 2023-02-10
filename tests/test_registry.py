from yt.utilities.object_registries import output_type_registry

import yt_aspect  # NOQA


def test_frontend_registry():
    assert "ASPECTDataset" in output_type_registry
    assert "PVTUDataset" in output_type_registry
