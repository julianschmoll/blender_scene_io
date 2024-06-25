import bpy

from blender_scene_io import scene_utils



class FrSaveIncrement(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.save_increment"
    bl_label = "Save Increment"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene_utils.save_increment()

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrSaveIncrement.bl_idname, text=FrSaveIncrement.bl_label
    )


def register():
    bpy.utils.register_class(FrSaveIncrement)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrSaveIncrement)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
