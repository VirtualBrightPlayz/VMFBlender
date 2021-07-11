import bpy
import bpy_extras.io_utils
import bmesh
import mathutils
import math
from .cbre import VersionInfoCBRE
from .hl2 import VersionInfoHL2, VmfVertex
from .vmflib.vmflib import vmf
from .vmflib.vmflib.types import Vertex, Output, Origin, Plane, Axis
from .vmflib.vmflib.tools import Block
from .vmflib.vmflib.brush import Solid, Side

class VMF_Save_OT_Operator(bpy.types.Operator):
    bl_idname = "vmf.save"
    bl_description = "Saves as VMF"
    bl_label = "Save as VMF"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    texpath = ""

    def execute(self, context):
        print("filepath=" + str(self.filepath))
        if (str(self.filepath).endswith(".vmf")):

            map = vmf.ValveMap()
            # change to 102.4 for cbre
            # 102.4 = hl2
            scale = 102.4

            for ob in bpy.data.objects:
                if ob.type == 'MESH':
                    mesh = ob.to_mesh()

                    mesh.validate_material_indices()

                    faces = mesh.polygons
                    loops = mesh.loops
                    edges = mesh.edges
                    vertices = mesh.vertices
                    uv = mesh.uv_layers.active.data

                    blk = Solid()

                    for f in faces:
                        if f.hide:
                            continue
                        mat = ob.material_slots[f.material_index].material
                        verts = f.vertices
                        pos = []
                        norms = []
                        uvs = []
                        for v in f.loop_indices:
                            pos.append(ob.matrix_world @ vertices[loops[v].vertex_index].co)
                            norms.append(vertices[loops[v].vertex_index].normal)
                            uvs.append(uv[v].uv)
                        if len(pos) >= 3:
                            vert0 = Vertex(pos[0].x * scale, pos[0].y * scale, pos[0].z * scale)
                            vert1 = Vertex(pos[1].x * scale, pos[1].y * scale, pos[1].z * scale)
                            vert2 = Vertex(pos[2].x * scale, pos[2].y * scale, pos[2].z * scale)
                            plane = Plane(vert2, vert1, vert0)
                            side = Side(plane, mat.name)
                            vertx = VmfVertex()
                            vertx.properties["count"] = len(pos)
                            for i in range(0, len(pos)):
                                p = -i + len(pos) - 1
                                vertx.properties["vertex" + str(p)] = Vertex(pos[i].x * scale, pos[i].y * scale, pos[i].z * scale)
                            # vertx.properties["vertex0"] = vert2
                            # vertx.properties["vertex1"] = vert1
                            # vertx.properties["vertex2"] = vert0
                            side.children.append(vertx)
                            # side.uaxis, side.vaxis = plane.sensible_axes()
                            # side.uaxis, side.vaxis = self.axis_calc(plane)

                            #calculate tri-normal
                            norm = (pos[2] - pos[0]).cross((pos[1] - pos[0]))
                            mypos = (pos[0] + pos[1] + pos[2]) / 3.0

                            ## world space
                            # d = norm.copy()
                            # d.normalize()
                            # d = mathutils.Vector((abs(d.x), abs(d.y), abs(d.z)))
                            # iod = self.nearest_axis(d)
                            # ua = mathutils.Vector((1.0, 0.0, 0.0))
                            # if (iod == 1):
                            #     ua = mathutils.Vector((0.0, 1.0, 0.0))
                            # va = mathutils.Vector((0.0, 0.0, -1.0))
                            # if (iod == 3):
                            #     va = mathutils.Vector((0.0, -1.0, 0.0))


                            ## face space
                            d = norm.copy()
                            d.normalize()
                            d = mathutils.Vector((abs(d.x), abs(d.y), abs(d.z)))
                            iod = self.nearest_axis(d)
                            tempv = mathutils.Vector((0.0, 0.0, -1.0))
                            # if (iod == 1):
                                # tempv = mathutils.Vector((0.0, 0.0, -1.0))
                            # if (iod == 1):
                            #     tempv = mathutils.Vector((-1.0, 0.0, 0.0))
                            if (iod == 3):
                                tempv = mathutils.Vector((0.0, -1.0, 0.0))
                            ua = norm.copy().normalized().cross(tempv).normalized()
                            va = ua.cross(norm.copy().normalized()).normalized()

                            side.uaxis = Axis(ua.x, ua.y, ua.z)
                            side.vaxis = Axis(va.x, va.y, va.z)
                            side.rotation = 0

                            uv_layer = 0

                            xmin = min(uvs[0][0], uvs[1][0])
                            xmax = max(uvs[0][0], uvs[1][0])
                            ymin = min(uvs[0][1], uvs[1][1])
                            ymax = max(uvs[0][1], uvs[1][1])
                            xcent = 0
                            ycent = 0

                            amnt = len(uvs)

                            for i in range(0, amnt):
                                xmin = min(xmin, uvs[i][0])
                                xmax = max(xmax, uvs[i][0])
                                ymin = min(ymin, uvs[i][1])
                                ymax = max(ymax, uvs[i][1])
                                xcent += uvs[i][0] #% 1.0
                                ycent += uvs[i][1] #% 1.0
                            
                            xcent /= float(amnt)
                            ycent /= float(amnt)

                            idxmin = 0
                            idxmax = 0
                            idymin = 0
                            idymax = 0
                            idzmin = 0
                            idzmax = 0

                            idmin = 0
                            idmax = 0

                            pos2 = []
                            mymatrix = mathutils.Matrix.OrthoProjection(mathutils.Vector((0.0, 0.0, 1.0)), 4)
                            d = norm.copy()
                            d.normalize()
                            # mymatrix = mathutils.Matrix.OrthoProjection(d, 4)

                            # print(mymatrix @ pos[0])

                            for p in pos:
                                pos2.append(mymatrix @ p)
                            
                            for i in range(0, len(pos2)):
                                if pos2[i].x > pos2[idxmax].x:
                                    idxmax = i
                                if pos2[i].x < pos2[idxmin].x:
                                    idxmin = i
                                if pos2[i].y > pos2[idymax].y:
                                    idymax = i
                                if pos2[i].y < pos2[idymin].y:
                                    idymin = i
                                if pos2[i].z > pos2[idzmax].z:
                                    idzmax = i
                                if pos2[i].z < pos2[idzmin].z:
                                    idzmin = i

                                if pos2[i] > pos2[idmax]:
                                    idmax = i
                                if pos2[i] < pos2[idmin]:
                                    idmin = i

                            if mat is not None and mat.node_tree:
                                for x in mat.node_tree.nodes:
                                    if x.type == 'TEX_IMAGE':
                                        # print(x.image.name)
                                        # print(x.image.size[0])
                                        # print(xmin)
                                        # print(xmax)
                                        s = x.image.size
                                        # print(s[0])
                                        # side.uaxis.scale = -((xmin / pos2[idxmin].x) - (xmax / pos2[idxmax].x)) % 1.0 #- 1.0
                                        # side.uaxis.scale = (pos2[idxmax].x - pos2[idxmin].x) % 1.0 #- 1.0
                                        side.uaxis.scale = (xmax + xmin) / 2.0 #% 1.0
                                        side.uaxis.translate = (xmin) * s[0]
                                        # side.vaxis.scale = -((ymin / pos2[idzmin].y) - (ymax / pos2[idzmax].y)) % 1.0 #- 1.0
                                        # side.vaxis.scale = (pos2[idymax].y - pos2[idymin].y) % 1.0 #- 1.0
                                        side.vaxis.scale = (ymax + ymin) / 2.0 #% 1.0
                                        side.vaxis.translate = (ymin) * s[1]
                                        break

                            # xs = f.loops[0][bm.loops.layers.uv.active].uv.x + f.loops[1][bm.loops.layers.uv.active].uv.x + f.loops[2][bm.loops.layers.uv.active].uv.x
                            # ys = f.loops[0][bm.loops.layers.uv.active].uv.y + f.loops[1][bm.loops.layers.uv.active].uv.y + f.loops[2][bm.loops.layers.uv.active].uv.y

                            # side.uaxis.scale = xs / 3.0
                            # side.vaxis.scale = ys / 3.0
                            blk.children.append(side)
                        else:
                            print("a face was missed! " + str(f))

                    map.world.children.append(blk)

                    # bm.free()
            map.children.append(VersionInfoCBRE())
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
            return 1 # x
        if (normal.y >= normal.z):
            return 2 # y
        return 3 # z

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