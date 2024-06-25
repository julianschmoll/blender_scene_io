bl_info = {
    "name": "GreasePencil: Project to View for all Frames",
    "blender": (4, 0, 2),
    "category": ""
}
import bpy
import os
import pathlib
import json

from blender_scene_io import scene_utils


class GpReprojectAllFramesOperator(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.reproject_all_frames"
    bl_label = "Reproject and Cleanup that Frog :)"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object

    def execute(self, context):
        scene = context.scene
        gp_obj = context.active_object
        bpy.ops.screen.frame_jump(end=False)

        source_collection = gp_obj.grease_pencil_modifiers[f"{gp_obj.name}_lineart"].source_collection.name

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
        if not os.path.isfile(json_path):
            bpy.ops.gpencil.check_animated_frames()

        with open(json_path, "r") as json_file:
            animated_frames = set(json.load(json_file).get(source_collection))

        start, end = scene_utils.get_frame_ramge()
        animated_frames.add(end)
        for _ in range(start, end+1):
            if not scene.frame_current in animated_frames:
                try:
                    bpy.ops.gpencil.delete(type='FRAME')
                except RuntimeError:
                    print(f"Could not delete {scene.frame_current}")
            bpy.ops.gpencil.select_all(action='SELECT')
            try:
                bpy.ops.gpencil.reproject(type='VIEW', keep_original=False)
            except RuntimeError:
                print(f"Did not reproject {scene.frame_current}")
            bpy.ops.screen.frame_offset(delta=1)

        bpy.ops.gpencil.frame_clean_loose()

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        GpReprojectAllFramesOperator.bl_idname, text=GpReprojectAllFramesOperator.bl_label
    )


def register():
    bpy.utils.register_class(GpReprojectAllFramesOperator)
    bpy.types.VIEW3D_MT_edit_gpencil.append(menu_func)


def unregister():
    bpy.utils.unregister_class(GpReprojectAllFramesOperator)
    bpy.types.VIEW3D_MT_edit_gpencil.remove(menu_func)


if __name__ == "__main__":
        register()