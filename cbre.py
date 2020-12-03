"""

Helper classes specific to creating rooms for SCPCB/CBRE

"""

from .vmflib.vmflib.vmf import Entity, Connections, VmfClass
from .vmflib.vmflib.types import Bool, Origin, Output

class VersionInfoCBRE(VmfClass):

    def __init__(self):
        self.vmf_class_name = "versioninfo"
        VmfClass.__init__(self)
        self.properties["editorname"] = "CBRE"
        self.properties["editorversion"] = "1.0"
        self.properties["editorbuild"] = "0"
        self.properties["mapversion"] = "1"
        self.properties["formatversion"] = "100"
        self.properties["prefab"] = "0"