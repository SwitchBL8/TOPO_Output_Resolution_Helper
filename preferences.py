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
        split1 = row.split(factor=0.9)
        split2 = split1.split(factor=0.66)
        split3 = split2.split(factor=0.5)
        split4 = split3.split(factor=1)
        col = split1.column()
        col.label(text="enabled")
        col = split2.column()
        col.label(text="Height")
        col = split3.column()
        col.label(text="Width")
        col = split4.column()
        col.label(text="Name")
        # always add empty row?
        if "" not in self.custom_resolutions or len(self.custom_resolutions) == 0:
            self.custom_resolutions.add()
        for cr in self.custom_resolutions:
            row = box.row()
            split1 = row.split(factor=0.9)
            split2 = split1.split(factor=0.66)
            split3 = split2.split(factor=0.5)
            split4 = split3.split(factor=1)
            col = split1.column()
            col.prop(cr, 'enabled')
            col = split2.column()
            col.prop(cr, 'height')
            col = split3.column()
            col.prop(cr, 'width')
            col = split4.column()
            col.prop(cr, 'name')


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
