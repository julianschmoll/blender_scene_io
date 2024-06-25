import bpy


class FrBakeAllLineArtObjects\
            (bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.bake_lineart_objects"
    bl_label = "Bake all Lineart Objects"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.lineart_bake_strokes_all()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrBakeAllLineArtObjects
        .bl_idname, text=FrBakeAllLineArtObjects
        .bl_label
    )


def register():
    bpy.utils.register_class(FrBakeAllLineArtObjects
                             )
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrBakeAllLineArtObjects
                               )
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
