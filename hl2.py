"""

Helper classes specific to creating rooms for HL2/Source (GMod in mind)

"""

from .vmflib.vmflib.vmf import Entity, Connections, VmfClass
from .vmflib.vmflib.types import Bool, Origin, Output

class VersionInfoHL2(VmfClass):

    def __init__(self):
        self.vmf_class_name = "versioninfo"
        VmfClass.__init__(self)
        self.properties["editorname"] = "GMOD"
        self.properties["editorversion"] = "400"
        self.properties["editorbuild"] = "8538"
        self.properties["mapversion"] = "1"
        self.properties["formatversion"] = "100"
        self.properties["prefab"] = "0"

class VmfVertex(VmfClass):

    """An XYZ location given by 3 decimal values and printed with parens."""

    def __init__(self):
        """Create a new Vertex representing the position (x, y, z)."""
        self.vmf_class_name = "vertex"
        VmfClass.__init__(self)
        self.properties["count"] = 0
