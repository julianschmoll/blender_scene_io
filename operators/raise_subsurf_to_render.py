import bpy

class FrRaiseSubsurfToRender(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.raise_subsurf_to_render"
    bl_label = "Raise Subsurf Level to Render Settings"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object

    def execute(self, context):
        for obj in bpy.data.objects:
            for modifier in obj.modifiers:
                if modifier.type == "SUBSURF":
                    modifier.levels = modifier.render_levels

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrRaiseSubsurfToRender.bl_idname, text=FrRaiseSubsurfToRender.bl_label
    )


def register():
    bpy.utils.register_class(FrRaiseSubsurfToRender)
    bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrRaiseSubsurfToRender)
    bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()