import bpy

class VMF_PT_Settings(bpy.types.PropertyGroup):
    texfolder: bpy.props.StringProperty(subtype="DIR_PATH")

class VMF_PT_Panel(bpy.types.Panel):
    bl_idname = "VMF_PT_Panel"
    bl_label = "VMF Panel"
    bl_category = "VMF"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        vmf_panel = context.scene.vmf_texfolder

        row = layout.row()
        row.prop(context.scene, "vmf_texfolder")
        row = layout.row()
        row.operator("vmf.loadtex", text="Load Textures")
        row = layout.row()
        row.operator("vmf.save", text="Save")