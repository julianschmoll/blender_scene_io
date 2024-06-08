from blender_scene_io import comp_script
from blender_scene_io import assemble_shot
from blender_scene_io import render_submission
from blender_scene_io import render_setup
from blender_scene_io import frogging_hell_menu

import bpy
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def run_startup_scripts():
    """This method is always run when launching blender."""
    LOGGER.info("Running Startup Scripts...")
    LOGGER.info("Set Paths To Absolute")
    bpy.context.preferences.filepaths.use_relative_paths = False
    LOGGER.info("Running Menu Scripts...")
    frogging_hell_menu.register()
    LOGGER.info("Running Render Setup Scripts...")
    render_setup.set_render_settings()
    LOGGER.info("Running Comp Scripts...")
    comp_script.comp_setup()
    LOGGER.info("Happy Blending!")


def assemble_and_submit_shot(shot_name):
    """Assembles shot, saves file and submits it to Renderpal."""
    shot_caches = frogging_hell_menu.get_shot_caches(shot_name)
    assemble_shot.load_shot(shot_caches, shot_name)
    render_submission.submit_render()
