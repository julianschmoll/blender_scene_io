import bpy


class FrRemoveUnusedLineArtMods(bpy.types.Operator):
    """Project to view for all frames"""
    bl_idname = "gpencil.remove_unused_lineart_mods"
    bl_label = "Remove unused mods"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects:
            for modifier in obj.grease_pencil_modifiers:
                if modifier.type == "GP_LINEART" and modifier.is_baked:
                    obj.grease_pencil_modifiers.remove(modifier)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        FrRemoveUnusedLineArtMods.bl_idname, text=FrRemoveUnusedLineArtMods.bl_label
    )


def register():
    bpy.utils.register_class(FrRemoveUnusedLineArtMods)
    # bpy.types.OBJECT_MT_frog_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FrRemoveUnusedLineArtMods)
    # bpy.types.OBJECT_MT_frog_menu.remove(menu_func)


if __name__ == "__main__":
        register()
