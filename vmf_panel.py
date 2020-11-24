import bpy

class VMF_PT_Panel(bpy.types.Panel):
    bl_idname = "VMF_PT_Panel"
    bl_label = "VMF Panel"
    bl_category = "VMF"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("vmf.save", text="Save")