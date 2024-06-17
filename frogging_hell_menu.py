from blender_scene_io import assemble_shot
from blender_scene_io import render_submission
from blender_scene_io import comp_script

import bpy
import os
import logging

BASE_DIR = r"M:\frogging_hell_prism\02_Library\Shots"
SHOT_STRING = bpy.props.StringProperty(name="String Value")
LOGGER = logging.getLogger("Frogging Hell Menu")


class FrogMenu(bpy.types.Menu):
    bl_label = "Frogging Hell"
    bl_idname = "OBJECT_MT_frog_menu"
    LOGGER.info("Initializing Frog Menu")

    def draw(self, context):
        layout = self.layout
        layout.label(text="Import", icon='IMPORT')
        layout.menu("OBJECT_MT_shot_assembly_menu", icon="ASSET_MANAGER")
        layout.separator()
        layout.label(text="Export", icon='EXPORT')
        layout.operator(
            "object.render_submission_operator",
            text=f"Submit to Renderpal",
            icon='RENDER_ANIMATION'
        )

class AssembleShotSubMenu(bpy.types.Menu):
    bl_label = "Assemble Shot"
    bl_idname = "OBJECT_MT_shot_assembly_menu"
    LOGGER.info("Adding Shot Assembly Menu")

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Shot to assemble")

        sequence = ""
        for shot in get_shot_list():
            if sequence != shot.split("-")[0]:
                layout.separator()
                sequence = shot.split("-")[0]
                layout.label(text=f"Sequence {sequence}", icon='SEQUENCE')
            LOGGER.debug(f"Populated Shot Assembly menu with {shot}")
            layout.operator(
                "object.shot_assembly_operator",
                text=f"Shot {' '.join(shot.split('-')[1:]).title()}"
            ).shot_name = shot


class ImportShot(bpy.types.Operator):
    """Import Shot Caches for selected shot"""
    bl_label = "Shot Assembly Operator"
    bl_idname = "object.shot_assembly_operator"
    shot_name: bpy.props.StringProperty(name="")

    def execute(self, context):
        shot_caches = get_shot_caches(self.shot_name)
        if not shot_caches:
            self.report({"ERROR"}, f"No valid cache found for {self.shot_name}")
            return {'CANCELLED'}
        LOGGER.info(f"Executing Shot Assembly for {self.shot_name}")
        self.report({"INFO"}, f"Executing Shot Assembly for {self.shot_name}")
        assemble_shot.load_shot(shot_caches, self.shot_name)
        return {'FINISHED'}

class RenderShot(bpy.types.Operator):
    """Submit Job to render with RenderPal"""
    bl_label = "Render Submission Operator"
    bl_idname = "object.render_submission_operator"

    def execute(self, context):
        LOGGER.info("Submitting Job")
        render_submission.submit_render()
        return {'FINISHED'}


def get_shot_list():
    return os.listdir(BASE_DIR)


def get_shot_caches(shot):
    export_folder = os.path.join(BASE_DIR, shot, "Export", "Animation")

    try:
        version_folders = os.listdir(export_folder)
    except FileNotFoundError:
        LOGGER.error(f"No valid cache found for {shot}")
        return

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
    self.layout.menu(FrogMenu.bl_idname)


def register():
    bpy.utils.register_class(FrogMenu)
    bpy.utils.register_class(ImportShot)
    bpy.utils.register_class(RenderShot)
    bpy.utils.register_class(AssembleShotSubMenu)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.types.VIEW3D_MT_curve_add.remove(draw_menu)
    bpy.utils.unregister_class(ImportShot)
    bpy.utils.unregister_class(AssembleShotSubMenu)
    bpy.utils.unregister_class(FrogMenu)
    bpy.utils.unregister_class(RenderShot)
