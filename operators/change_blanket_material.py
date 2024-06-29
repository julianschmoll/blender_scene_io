import bpy

from blender_scene_io import material_assigner


class FrChangeBlanketMaterial(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.change_blanket_material"
    bl_label = "Make Blanket go VROOM"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects:
            if "fat_pillow_mod" in obj.name:
                obj.data.materials.clear()
                material_assigner.apply_cell_shader(obj, name=f"{obj.name}_cel_shader", factor=0.4)
            if "blanket_geo" in obj.name:
                obj.data.materials.clear()
                material_assigner.apply_cell_shader(obj, name=f"{obj.name}_cel_shader", factor=0.4)
            if "facecurve_sweep" in obj.name:
                obj.data.materials.clear()
                material_assigner.apply_cell_shader(obj, color=(0,0,0), name=f"{obj.name}_cel_shader", factor=0)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrChangeBlanketMaterial.bl_idname, text=FrChangeBlanketMaterial.bl_label
    )


def register():
    bpy.utils.register_class(FrChangeBlanketMaterial)
    # bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrChangeBlanketMaterial)
    # bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
