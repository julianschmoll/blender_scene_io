import bpy
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def set_render_settings():

    LOGGER.info("Render Script...")

    # ------------------------------------------ render settings
    bpy.context.scene.render.resolution_x = 2048
    bpy.context.scene.render.resolution_y = 1536
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.fps = 25
    bpy.context.scene.frame_start = 1001
    bpy.context.scene.camera.data.clip_end = 100000

    # ------------------------------------------ output settings
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
    bpy.context.scene.render.image_settings.exr_codec = 'ZIP'

    # ------------------------------------------ render layers
    bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_color = True
    bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_object = True
    bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_material = True
