import bpy
import logging


LOGGER = logging.getLogger("Render Setup")
scene = bpy.context.scene


def set_render_settings():
    scene.render.resolution_x = 2048
    scene.render.resolution_y = 1536
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.fps = 25
    scene.frame_start = 1001
    scene.camera.data.clip_end = 100000

    scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
    scene.render.image_settings.exr_codec = 'ZIP'

    scene.view_layers["ViewLayer"].use_pass_cryptomatte_object = True
    scene.view_layers["ViewLayer"].use_pass_cryptomatte_material = True
