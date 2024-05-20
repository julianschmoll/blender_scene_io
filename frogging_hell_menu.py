import bpy
import os

base_dir = r"M:\frogging_hell_prism\02_Library\Shots"
shots = os.listdir(base_dir)
shot_string = bpy.props.StringProperty(name="String Value")


class MY_MT_FrogMenu(bpy.types.Menu):
    bl_label = "Frogging Hell"
    bl_idname = "OBJECT_MT_custom_menu"
    print("hello")

    def draw(self, context):
        layout = self.layout
        layout.label(text="Common Tools", icon='RENDER_ANIMATION')

        # call the second custom menu
        layout.menu("OBJECT_MT_sub_menu", icon="ASSET_MANAGER")


class MY_MT_FrogSubMenu(bpy.types.Menu):
    bl_label = "Assemble Shot"
    bl_idname = "OBJECT_MT_sub_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Shot to assemble", icon='IMPORT')

        for shot in get_shot_list():
            layout.operator("object.simple_operator", text=shot).shot_name = shot


class ImportShot(bpy.types.Operator):
    """Import Shot Caches for selected shot"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    shot_name: bpy.props.StringProperty(name="")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        shot_name = self.shot_name
        shot_caches = get_shot_caches(self.shot_name)
        # ToDo: Call assemble shot here
        return {'FINISHED'}


def get_shot_list():
    return os.listdir(base_dir)


def get_shot_caches(shot):
    export_folder = os.path.join(base_dir, shot, "Export", "Animation")

    try:
        version_folders = os.listdir(export_folder)
    except FileNotFoundError:
        raise RuntimeError(f"Kein gültiger Cache für {shot}")

    versions = []

    for version_folder in version_folders:
        versions.append(int(version_folder.split("_")[0][-4:]))

    max_version = max(versions)
    max_version_string = f"v{str(max_version).zfill(4)}"
    max_version_folder = ""

    for version_folder in version_folders:
        if version_folder.startswith(max_version_string):
            max_version_folder = version_folder

    cache_folder = os.path.join(export_folder, max_version_folder, "centimeter")

    cache_list = []
    for cache in os.listdir(cache_folder):
        cache_path = os.path.join(cache_folder, cache)
        # import this cache
        cache_list.append(cache_path)
    return cache_list


def draw_menu(self, context):
    self.layout.menu(MY_MT_FrogMenu.bl_idname)


def register():
    bpy.utils.register_class(MY_MT_FrogMenu)
    bpy.utils.register_class(ImportShot)
    bpy.utils.register_class(MY_MT_FrogSubMenu)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.types.VIEW3D_MT_curve_add.remove(draw_menu)
    bpy.utils.unregister_class(ImportShot)
    bpy.utils.unregister_class(MY_MT_FrogSubMenu)
    bpy.utils.unregister_class(MY_MT_FrogMenu)
