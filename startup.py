from blender_scene_io import comp_script
from blender_scene_io import render_setup
from blender_scene_io import frogging_hell_menu

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def run_startup_scripts():
    """This method is always run when launching blender."""
    LOGGER.info("Running Startup Scripts...")
    LOGGER.info("Running Menu Scripts...")
    frogging_hell_menu.register()
    LOGGER.info("Running Render Setup Scripts...")
    render_setup.set_render_settings()
    LOGGER.info("Running Comp Scripts...")
    comp_script.comp_setup()
    LOGGER.info("Happy Blending!")
