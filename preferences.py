import bpy
import os
#
# Preferences for the add-on
# add custom resolutions
#


def get_addon_preferences():
    addon_name = os.path.splitext(__name__)[0]
    addon_prefs = bpy.context.preferences.addons[addon_name].preferences
    return addon_prefs


class CustomResolution(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='', default="Enter name")
    #dimension: bpy.props.StringProperty(name='', default="width height")
    width: bpy.props.IntProperty(name='', default=1920)
    height: bpy.props.IntProperty(name='', default=1080)
    enabled: bpy.props.BoolProperty(name='', default=False)


class TOPO_Preferences(bpy.types.AddonPreferences):
    bl_idname = os.path.splitext(__name__)[0]
    custom_resolutions: bpy.props.CollectionProperty(type=CustomResolution)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Custom resolutions')
        box = layout.box()
        row = box.row()
        col = row.column(align=True)
        col.label(text="Name")
        col = row.column(align=True)
        col.label(text="Width")
        col = row.column(align=True)
        col.label(text="Height")
        col = row.column(align=True)
        col.label(text="enabled")
        # always add empty row?
        if "" not in self.custom_resolutions or len(self.custom_resolutions) == 0:
            self.custom_resolutions.add()
        for cr in self.custom_resolutions:
            row = box.row()
            col = row.column(align=True)
            col.prop(cr, 'name')
            col = row.column(align=True)
            col.prop(cr, 'width')
            col = row.column(align=True)
            col.prop(cr, 'height')
            col = row.column(align=True)
            col.prop(cr, 'enabled')


classes = (
    CustomResolution,
    TOPO_Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
