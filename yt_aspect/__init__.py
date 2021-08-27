from yt.utilities.object_registries import output_type_registry

from .data_structures import ASPECTUnstructuredIndex  # noqa: F401
from .data_structures import ASPECTUnstructuredMesh  # noqa: F401
from .data_structures import ASPECTDataset
from .fields import ASPECTFieldInfo  # noqa: F401
from .io import IOHandlerASPECT  # noqa: F401

output_type_registry["ASPECTDataset"] = ASPECTDataset
