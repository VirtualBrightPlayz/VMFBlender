import bpy
import bpy_extras.io_utils
import bmesh
import mathutils
import math
import os, fnmatch
from .cbre import VersionInfoCBRE
from .hl2 import VersionInfoHL2, VmfVertex
from .vmflib.vmflib import vmf
from .vmflib.vmflib.types import Vertex, Output, Origin, Plane, Axis
from .vmflib.vmflib.tools import Block
from .vmflib.vmflib.brush import Solid, Side

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

class VMF_LoadTex_OT_Operator(bpy.types.Operator):
    bl_idname = "vmf.loadtex"
    bl_description = "Load VMF Textures"
    bl_label = "Load VMF Textures"

    def execute(self, context):
        vmf_texfolder = str(context.scene.vmf_texfolder)
        for texname in bpy.data.materials.keys():
            item = find(str(texname) + '.*', vmf_texfolder)
            if not item:
                continue
            mat = bpy.data.materials[texname]
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(item[0])
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
            mat.node_tree.links.new(bsdf.inputs['Alpha'], texImage.outputs['Alpha'])
        return {'FINISHED'}
