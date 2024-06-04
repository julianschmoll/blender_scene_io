import bpy
import os
import logging


LOGGER = logging.getLogger("Scene Utils")


def set_render_paths(scene_path=None):
    if not scene_path:
        scene_path = get_scene_file_path()
    path_elem = scene_path.split(os.sep)
    path_elem[0] = "M:\\"
    naming_elem = path_elem[-1].split("_")

    LOGGER.info("Setting Render Paths")
    base_render_path = os.path.join(
        *path_elem[0:5],
        "Rendering",
        "3dRender",
        naming_elem[4],
    )
    file_name = "shot_{0}_3d_####.exr".format(naming_elem[1])

    bpy.context.scene.render.filepath = os.path.join(
        base_render_path, "rawr", file_name
    )
    bpy.context.scene.node_tree.nodes["File Output"].base_path = os.path.join(
        base_render_path, "out", file_name
    )


def save_scenefile():
    LOGGER.info("Saving Scenefile")
    bpy.ops.wm.save_mainfile()


def get_scene_file_path():
    return bpy.data.filepath


def get_frame_ramge():
    scn = bpy.context.scene
    return scn.frame_start, scn.frame_end