"""

Helper classes specific to creating rooms for SCPCB/CBRE

"""

from .vmflib.vmflib.vmf import Entity, Connections, VmfClass
from .vmflib.vmflib.types import Bool, Origin, Output

class VersionInfo(VmfClass):

    def __init__(self):
        self.vmf_class_name = "versioninfo"
        VmfClass.__init__(self)
        self.properties["editorname"] = "CBRE"
        self.properties["editorversion"] = "1.0"
        self.properties["editorbuild"] = "0"
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
