from .data_structures import (
    ASPECTDataset,
    ASPECTUnstructuredIndex,
    ASPECTUnstructuredMesh,
)
from .fields import ASPECTFieldInfo
from .io import IOHandlerASPECT

from yt.utilities.object_registries import output_type_registry



output_type_registry["ASPECTDataset"] = ASPECTDataset
