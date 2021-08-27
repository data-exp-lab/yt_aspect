import yt_aspect  # NOQA
from yt.utilities.object_registries import output_type_registry


def test_frontend_registry():
    assert "ASPECTDataset" in output_type_registry
