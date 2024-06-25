import bpy
from contextlib import contextmanager

@contextmanager
def render_subsurf_settings():
    initial_settings = {}
    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if modifier.type == "SUBSURF":
                initial_settings[obj.name] = modifier.levels
                modifier.levels = modifier.render_levels
    try:
        yield
    finally:
        for obj_name, subsurf_level in initial_settings.items():
            for modifier in bpy.data.objects[obj_name].modifiers:
                if modifier.type == "SUBSURF":
                    modifier.levels = subsurf_level


class FrBakeAllLineArtObjects(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.bake_lineart_objects"
    bl_label = "Bake all Lineart Objects"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        with render_subsurf_settings():
            bpy.ops.object.lineart_bake_strokes_all()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrBakeAllLineArtObjects.bl_idname,
        text=FrBakeAllLineArtObjects.bl_label
    )


def register():
    bpy.utils.register_class(FrBakeAllLineArtObjects)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrBakeAllLineArtObjects)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
