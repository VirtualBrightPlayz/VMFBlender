# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "vmf",
    "author" : "VirtualBrightPlayz",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from .vmf_panel import VMF_PT_Panel, VMF_PT_Settings
from .vmf_save import VMF_Save_OT_Operator
from .vmf_loadtex import VMF_LoadTex_OT_Operator

classes = (VMF_PT_Panel, VMF_Save_OT_Operator, VMF_LoadTex_OT_Operator)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.vmf_texfolder = bpy.props.StringProperty(subtype="DIR_PATH")

def unregister():
    del bpy.types.Scene.vmf_texfolder
    for cls in classes:
        bpy.utils.unregister_class(cls)
# register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()