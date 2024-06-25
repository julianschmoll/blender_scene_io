import bpy
import pathlib
import os
import json

from blender_scene_io import mesh_utils
from blender_scene_io import scene_utils
from blender_scene_io import ui


class FrSaveAnimatedFramesOperator(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.check_animated_frames"
    bl_label = "Check Animated Frames"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        file = pathlib.Path(scene_utils.get_scene_file_path())
        name = file.name
        json_path = os.path.join(
            file.parent,
            "_".join([
                *name.split("_")[0:3],
                "animation-data",
                *name.split("_")[4:6],
                ".json"
            ])
        )

        col_list = []

        for collection in bpy.data.collections:
            if not "grease" in collection.name:
                col_list.append(collection.name)

        with open(json_path, "w") as file:
            json.dump(mesh_utils.check_animated_frames(col_list), file, indent=6)


        ui.ShowMessageBox(
            message=json_path,
            title="Wrote Animated Frames info to:"
        )

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrSaveAnimatedFramesOperator.bl_idname, text=FrSaveAnimatedFramesOperator.bl_label
    )


def register():
    bpy.utils.register_class(FrSaveAnimatedFramesOperator)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrSaveAnimatedFramesOperator)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
