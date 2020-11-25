import bpy
import bpy_extras.io_utils
import bmesh
import mathutils
import math
from .cbre import VersionInfo, VmfVertex
from .vmflib.vmflib import vmf
from .vmflib.vmflib.types import Vertex, Output, Origin, Plane, Axis
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
                        mat = bpy.data.materials[f.material_index + 1]
                        verts = f.verts
                        pos = []
                        norms = []
                        for v in f.verts:
                            pos.append(ob.matrix_world @ v.co)
                            norms.append(ob.matrix_world @ v.normal)
                        if len(verts) == 3:
                            scale = 102.4
                            vert0 = Vertex(pos[0].x * scale, pos[0].y * scale, pos[0].z * scale)
                            vert1 = Vertex(pos[1].x * scale, pos[1].y * scale, pos[1].z * scale)
                            vert2 = Vertex(pos[2].x * scale, pos[2].y * scale, pos[2].z * scale)
                            plane = Plane(vert2, vert1, vert0)
                            side = Side(plane, mat.name)
                            vertx = VmfVertex()
                            vertx.properties["count"] = 3
                            vertx.properties["vertex0"] = vert2
                            vertx.properties["vertex1"] = vert1
                            vertx.properties["vertex2"] = vert0
                            side.children.append(vertx)
                            # side.uaxis, side.vaxis = plane.sensible_axes()
                            # side.uaxis, side.vaxis = self.axis_calc(plane)

                            matrix = ob.matrix_world
                            matrix2 = ob.matrix_world.inverted()


                            ## world space
                            d = f.normal.copy()
                            d.normalize()
                            d = mathutils.Vector((abs(d.x), abs(d.y), abs(d.z)))
                            d = self.nearest_axis(d)
                            ua = mathutils.Vector((1.0, 0.0, 0.0))
                            if (d.x != 0.0):
                                ua = mathutils.Vector((0.0, 1.0, 0.0))
                            va = mathutils.Vector((0.0, 0.0, -1.0))
                            if (d.z != 0.0):
                                va = mathutils.Vector((0.0, -1.0, 0.0))


                            ## face space
                            # ua = f.normal.copy()
                            # ua.normalize()
                            # ua = mathutils.Vector((abs(ua.x), abs(ua.y), abs(ua.z)))
                            # ua = self.nearest_axis(ua)
                            # va = mathutils.Vector((0.0, 0.0, -1.0))
                            # if (ua.z == 1.0):
                            #     va = mathutils.Vector((0.0, -1.0, 0.0))
                            # ua = f.normal.copy()
                            # ua.normalize()
                            # ua.cross(va)
                            # va = f.normal.copy()
                            # va.normalize()
                            # va.cross(ua)

                            side.uaxis = Axis(ua.x, ua.y, ua.z)
                            side.vaxis = Axis(va.x, va.y, va.z)

                            uv_layer = 0

                            xmin = min(min(f.loops[0][bm.loops.layers.uv.active].uv.x, f.loops[1][bm.loops.layers.uv.active].uv.x), f.loops[2][bm.loops.layers.uv.active].uv.x)
                            xmax = max(max(f.loops[0][bm.loops.layers.uv.active].uv.x, f.loops[1][bm.loops.layers.uv.active].uv.x), f.loops[2][bm.loops.layers.uv.active].uv.x)
                            ymin = min(min(f.loops[0][bm.loops.layers.uv.active].uv.y, f.loops[1][bm.loops.layers.uv.active].uv.y), f.loops[2][bm.loops.layers.uv.active].uv.y)
                            ymax = max(max(f.loops[0][bm.loops.layers.uv.active].uv.y, f.loops[1][bm.loops.layers.uv.active].uv.y), f.loops[2][bm.loops.layers.uv.active].uv.y)

                            # side.uaxis.scale = xmax - xmin
                            # side.uaxis.translate = xmin
                            # side.vaxis.scale = ymax - ymin
                            # side.vaxis.translate = ymin

                            xs = f.loops[0][bm.loops.layers.uv.active].uv.x + f.loops[1][bm.loops.layers.uv.active].uv.x + f.loops[2][bm.loops.layers.uv.active].uv.x
                            ys = f.loops[0][bm.loops.layers.uv.active].uv.y + f.loops[1][bm.loops.layers.uv.active].uv.y + f.loops[2][bm.loops.layers.uv.active].uv.y

                            # side.uaxis.scale = xs / 3.0
                            # side.vaxis.scale = ys / 3.0
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

    def nearest_axis(self, normal):
        if (normal.x >= normal.y and normal.x >= normal.z):
            return mathutils.Vector((1.0, 0.0, 0.0))
        if (normal.y >= normal.z):
            return mathutils.Vector((0.0, 1.0, 0.0))
        return mathutils.Vector((0.0, 0.0, 1.0))

    def axis_calc(self, axis):
        """Returns a sensible uaxis and vaxis for this plane."""
        # TODO: Rewrite this method to allow non-90deg planes to work
        # Figure out which axes the plane exists in
        axes = [1, 1, 1]
        axes[0] = (axis.v0.x - axis.v1.x - axis.v2.x) / 3.0
        axes[1] = (axis.v0.y - axis.v1.y - axis.v2.y) / 3.0
        axes[2] = (axis.v0.z - axis.v1.z - axis.v2.z) / 3.0
        # if axis.v0.x == axis.v1.x == axis.v2.x:
        #     axes[0] = 0
        # if axis.v0.y == axis.v1.y == axis.v2.y:
        #     axes[1] = 0
        # if axis.v0.z == axis.v1.z == axis.v2.z:
        #     axes[2] = 0

        # Figure out uaxis xyz
        u = [0, 0, 0]
        for i in range(3):
            if axes[i] != 0.0:
                u[i] = axes[i]
                axes[i] = 0
                break

        # Figure out vaxis xyz
        v = [0, 0, 0]
        for i in range(3):
            if axes[i] != 0.0:
                v[i] = -axes[i]
                break

        uaxis = Axis(u[0], u[1], u[2])
        vaxis = Axis(v[0], v[1], v[2])
        return (uaxis, vaxis)