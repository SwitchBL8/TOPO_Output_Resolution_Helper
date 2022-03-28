import bpy
from bpy.types import Menu, Operator
from . import preferences #import get_addon_preferences

bl_info = {
    "name": "Output Resolution Helper",
    "author": "TOPO - SwitchBL8",
    "description": "Easily choose your output resolution from a pie menu",
    "blender": (2, 83, 0),
    "version": (0, 0, 3),
    "category": "Render",
    "support": "TESTING",
    "doc_url": "https://github.com/SwitchBL8/TOPO_Output_Resolution_Helper/blob/main/README.md"
}

addon_keymaps = []


# this is the main FUNCTION that sets the output resolution
def main(context):
    x = context[0]
    y = context[1]
    label = context[2]
    bpy.context.scene.render.resolution_x = int(x)
    bpy.context.scene.render.resolution_y = int(y)
    print(f"Output resolution set to {x} x {y} ({label})")
    return {'FINISHED'}


# This CLASS is connected to each pie menu option and calls the main function
# It's the same for each choice, but with different parameters
class TOPO_OT_setresolution(Operator):
    bl_idname = "topo.setresolution"
    bl_label = "Set Resolution operator"
    reso: bpy.props.StringProperty(name="Resolution")

    def execute(self, context):
        reso_split = self.reso.split(" ")
        main(reso_split)
        return {'FINISHED'}


# this is the CLASS to set up the pie menu
class TOPO_MT_chooseoutputresolution(Menu):
    bl_label = "Choose Output Resolution"
    bl_idname = "TOPO_MT_chooseoutputresolution"

    reso_names = ["FullHD", "TikTok", "4K", "2K"]
    reso_dims = ["1920 1080", "1080 1920", "3840 2160", "2048 1024" ]

    def draw(self, context):
        addon_preferences = preferences.get_addon_preferences()
        if len(addon_preferences.custom_resolutions) > 0:
            for cs in addon_preferences.custom_resolutions:
                # add enabled custom resolutions to the pie menu
                if cs.enabled:
                    if cs.name not in self.reso_names:
                        self.reso_names.append(cs.name)
                        self.reso_dims.append(str(cs.width) + " " + str(cs.height))
                # remove custom resolutions from the pie menu when they have been disabled
                else:
                    if cs.name in self.reso_names:
                        self.reso_names.remove(cs.name)
                        self.reso_dims.remove(str(cs.width) + " " + str(cs.height))

        layout = self.layout

        pie = layout.menu_pie()
        for index in range(len(self.reso_dims)):
            label = self.reso_names[index]
            param = self.reso_dims[index] + " " + label
            # Add TOPO_OT_setresolution for each menu option, with different paramters
            pie.operator("TOPO_OT_setresolution", text=label).reso = param


# this CLASS is what you can search for/execute from a keymap
class TOPO_OT_resolution_helper(Operator):
    bl_idname = "topo.resolution_helper"
    bl_label = "TOPO Resolution Helper"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="TOPO_MT_chooseoutputresolution")
        return {'FINISHED'}


classes = (
    TOPO_MT_chooseoutputresolution,
    TOPO_OT_resolution_helper,
    TOPO_OT_setresolution,
)


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("TOPO_OT_resolution_helper", "R", "PRESS", ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))
    preferences.register()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    preferences.unregister()
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
    #bpy.ops.wm.call_menu_pie(name="TOPO_MT_chooseoutputresolution")

