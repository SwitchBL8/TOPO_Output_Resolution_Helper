import bpy
from bpy.types import AddonPreferences

class TOPO_Preferences(AddonPreferences):
    bl_idname = __name__
    reso_names : bpy.props.StringProperty(name='Name', default="Custom")
    reso_dims : bpy.props.StringProperty(name='Dimensions', default="width height")

    def draw(self, context):
        layout = self.layout
        layout.label(text='Custom resolutions')
        row = layout.row()
        row.prop(self, 'reso_names')
        row.prop(self, 'reso_dims')
        print("Done drawing preferences")

