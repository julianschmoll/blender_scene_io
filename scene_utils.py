import bpy
import os
import logging
import ctypes
import pathlib

from blender_scene_io import ui

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
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=filepath, relative_remap = False)
        ui.ShowMessageBox(
            message=f"Saved to {filepath}",
            title="Frog Pipeline"
        )
    else:
        bpy.ops.wm.save_mainfile(relative_remap = False)


def get_scene_file_path():
    return bpy.data.filepath


def get_frame_ramge():
    scn = bpy.context.scene
    return scn.frame_start, scn.frame_end


def get_user_abbr():
    get_user_name_ex = ctypes.windll.secur32.GetUserNameExW
    name_display = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    get_user_name_ex(name_display, None, size)

    name_buffer = ctypes.create_unicode_buffer(size.contents.value)
    get_user_name_ex(name_display, name_buffer, size)

    display_name = name_buffer.value.split()

    # this should be how prism does it
    return f"{display_name[-1][:1]}{display_name[0][:2]}".lower()


def clear_scene():
    """
    This function clears the default scene.
    """
    for vl in bpy.context.scene.view_layers:
        if vl.name not in ["View Layer", "ViewLayer", "MasterLayer"]:
            bpy.context.scene.view_layers.remove(vl)
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


def set_time_slider_view():
    for area in bpy.context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = region
                    with bpy.context.temp_override(**ctx):
                        bpy.ops.action.view_all()
                    break
            break


def save_increment():
    usr = get_user_abbr()
    filepath = pathlib.Path(get_scene_file_path())
    folder = filepath.parent
    version = get_highest_shot_version(folder)
    new_version = f"v{str(version + 1).zfill(4)}"
    original_name = filepath.name

    naming_elements = original_name.split("_")
    naming_elements[-3] = new_version
    naming_elements[-2] = usr

    file_name = "_".join(naming_elements)
    save_scenefile(os.path.join(folder, file_name))
    set_render_paths()


def get_highest_shot_version(folder, full_name=False):
    version = 1
    name = ""
    for file in os.listdir(folder):
        if not file.endswith(".blend"):
            continue
        current_version = int(file.split("_")[-3][1:])
        if current_version > version:
            version = current_version
            name = file
    if full_name:
        return name
    return version


def open_shot(shot_name):
    shot_folder = os.path.join(
        "M:/", "frogging_hell_prism", "02_Library", "Shots", shot_name, "Scenefiles", "shd", "Shading"
    )
    shot = get_highest_shot_version(shot_folder, full_name=True)
    shot_file = os.path.join(shot_folder, shot)
    bpy.ops.wm.open_mainfile(filepath=shot_file)


def cleanup_grease_collections():
    grease_layers = []

    for layer in bpy.context.scene.view_layers:
        if "Grease" in layer.name and not "NoGrease" in layer.name:
            grease_layers.append(layer)

    for layer in grease_layers:
        for collection in layer.layer_collection.children:
            if "grease" not in collection.name:
                collection.exclude = True
