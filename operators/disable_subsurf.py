import bpy

class FrDisableSubsurf(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.disable_subsurf"
    bl_label = "Lower All Subsurf to 0"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object

    def execute(self, context):
        for obj in bpy.data.objects:
            for modifier in obj.modifiers:
                if modifier.type == "SUBSURF":
                    modifier.levels = 0

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrDisableSubsurf.bl_idname, text=FrDisableSubsurf.bl_label
    )


def register():
    bpy.utils.register_class(FrDisableSubsurf)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrDisableSubsurf)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()