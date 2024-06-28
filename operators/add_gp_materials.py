import bpy
import os

from blender_scene_io import grease


class FrAddGpMaterials(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.add_gp_materials"
    bl_label = "Add GPencil Materials"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        brush_dir = r"M:\frogging_hell_prism\06_Artist\juschli\brushes"
        for image in os.listdir(brush_dir):
            if bpy.data.images.get(image):
                continue
            filepath = os.path.join(brush_dir, image)
            image_obj = grease.load_image(filepath)
            grease.add_material(name=image.split(",")[0], image=image_obj)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrAddGpMaterials.bl_idname,
        text=FrAddGpMaterials.bl_label
    )


def register():
    bpy.utils.register_class(FrAddGpMaterials)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrAddGpMaterials)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
