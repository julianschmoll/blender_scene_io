from blender_scene_io import comp_script
from blender_scene_io import material_assigner
from blender_scene_io import render_setup
from blender_scene_io import sort_outliner

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def run_startup_scripts():
    """This method is always run when launching blender."""
    LOGGER.info("Running Startup Scripts...")
    sort_outliner.sort_scene()
    render_setup.main()
    assign_materials()
    comp_script.basic_comp_setup()

def assign_materials():
    material_assigner.texture_frodo()
    material_assigner.texture_bed()
