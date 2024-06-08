import bpy
import os
import logging


LOGGER = logging.getLogger("Scene Utils")


# Having this here as we don't want to have prism in blender
USER_ABBR_DICT = {
    "js435": "jsc",
    "rl049": "rle",
    "lr059": "lre",
    "ch171": "cho",
    "mz095": "mzy",
    "lk181": "lku",
    "ab324": "abu",
    "nw086": "nwi",
    "ph081": "pho"
}


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
    LOGGER.info(f"Setting render path to {base_render_path}")
    file_name = "shot_{0}_3d_####.exr".format(naming_elem[1])

    bpy.context.scene.render.filepath = os.path.join(
        base_render_path, "rawr", file_name
    )
    bpy.context.scene.node_tree.nodes["File Output"].base_path = os.path.join(
        base_render_path, "out", file_name
    )


def save_scenefile(filepath=None):
    LOGGER.info("Saving Scenefile")
    if filepath:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.save_mainfile()


def get_scene_file_path():
    return bpy.data.filepath


def get_frame_ramge():
    scn = bpy.context.scene
    return scn.frame_start, scn.frame_end


def get_user_abbr():
    hdm_account = os.getlogin()
    return USER_ABBR_DICT.get(hdm_account) or "usr"


def clear_scene():
    """
    This function clears the default scene.
    """
    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lights,
            bpy.data.cameras,
            bpy.data.collections
    ):
        for node in bpy_data_iter:
            LOGGER.info(f"Removing {node.name}")
            bpy_data_iter.remove(node)
