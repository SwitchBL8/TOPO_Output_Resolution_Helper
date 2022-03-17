# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.types import Menu, Operator

bl_info = {
    "name" : "Output Resolution Helper",
    "author" : "TOPO - SwitchBL8",
    "description" : "Easily choose your output resolution from a pie menu",
    "blender" : (2, 83, 0),
    "version" : (0, 0, 1),
    "category" : "Render",
    "support" : "TESTING"
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
    reso : bpy.props.StringProperty(name="Resolution")
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
        layout = self.layout

        pie = layout.menu_pie()
        for index in range(len(self.reso_dims)):
            label = self.reso_names[index]
            param = self.reso_dims[index] + " " + label
            print(param)
            # Add TOPO_OT_setresolution for each menu option, with different paramters
            pie.operator("TOPO_OT_setresolution", text = label).reso = param
            print(f"Added {label}")
        return {'FINISHED'}

# this CLASS is what you can search for/execute from a keymap
class TOPO_OT_resolution_helper(Operator):
    bl_idname = "topo.resolution_helper"
    bl_label = "TOPO Resolution Helper"
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="TOPO_MT_chooseoutputresolution")
        return {'FINISHED'}


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("TOPO_OT_resolution_helper","R","PRESS",ctrl=True,shift=True)
        addon_keymaps.append((km,kmi))
    bpy.utils.register_class(TOPO_MT_chooseoutputresolution)
    bpy.utils.register_class(TOPO_OT_resolution_helper)
    bpy.utils.register_class(TOPO_OT_setresolution)



def unregister():
    bpy.utils.unregister_class(TOPO_MT_chooseoutputresolution)
    bpy.utils.unregister_class(TOPO_OT_resolution_helper)
    bpy.utils.unregister_class(TOPO_OT_setresolution)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
    #bpy.ops.wm.call_menu_pie(name="TOPO_MT_chooseoutputresolution")

