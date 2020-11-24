import bpy
import bpy_extras.io_utils
import bmesh
from .cbre import VersionInfo, VmfVertex
from .vmflib.vmflib import vmf
from .vmflib.vmflib.types import Vertex, Output, Origin, Plane
from .vmflib.vmflib.tools import Block
from .vmflib.vmflib.brush import Solid, Side

class VMF_Save_OT_Operator(bpy.types.Operator):
    bl_idname = "vmf.save"
    bl_description = "Saves as VMF"
    bl_label = "Save as VMF"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if (self.filepath.endswith(".vmf")):

            print("filepath=" + self.filepath)
            map = vmf.ValveMap()

            for ob in bpy.data.objects:
                if ob.type == 'MESH':
                    mesh = ob.to_mesh()

                    bm = bmesh.new()
                    bm.from_mesh(mesh)

                    data = bmesh.ops.triangulate(bm, faces=bm.faces)

                    edges = data['edges']
                    faces = data['faces']

                    blk = Solid()

                    for f in faces:
                        mat = bpy.data.materials[f.material_index]
                        verts = f.verts
                        if len(verts) == 3:
                            vert0 = Vertex(verts[0].co.x * 102.4, verts[0].co.y * 102.4, verts[0].co.z * 102.4)
                            vert1 = Vertex(verts[1].co.x * 102.4, verts[1].co.y * 102.4, verts[1].co.z * 102.4)
                            vert2 = Vertex(verts[2].co.x * 102.4, verts[2].co.y * 102.4, verts[2].co.z * 102.4)
                            side = Side(Plane(vert2, vert1, vert0), mat.name)
                            vertx = VmfVertex()
                            vertx.properties["count"] = 3
                            vertx.properties["vertex0"] = vert2
                            vertx.properties["vertex1"] = vert1
                            vertx.properties["vertex2"] = vert0
                            side.children.append(vertx)
                            blk.children.append(side)
                        else:
                            print("a face was missed! " + str(f))

                    map.world.children.append(blk)

            map.children.append(VersionInfo())
            map.world.skyname = None
            map.world.properties["mapversion"] = 1
            map.cordon.maxs.x = 1024.0
            map.cordon.maxs.y = 1024.0
            map.cordon.maxs.z = 1024.0
            map.cordon.mins.x = -1024.0
            map.cordon.mins.y = -1024.0
            map.cordon.mins.z = -1024.0

            # write to disk
            map.write_vmf(str(self.filepath))
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}