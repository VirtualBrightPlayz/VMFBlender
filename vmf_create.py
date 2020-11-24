import bpy

class VMF_Create_OT_Operator(bpy.types.Operator):
    bl_idname = "vmf.create"
    bl_description = "Create a new VMF"
    bl_label = "VMF Create"

    def execute(self, context):
        # print("Not done")
        # empty = bpy.ops.object.empty_add(location=(0.0, 0.0, 0.0))
        # print("str" + str(empty))
        return {'FINISHED'}