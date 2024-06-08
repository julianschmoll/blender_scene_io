from blender_scene_io import material_assigner
from blender_scene_io import scene_utils

import json
import logging
import bpy
import os
import pathlib
from mathutils import Vector


LOGGER = logging.getLogger("Shot Assembly")

def load_shot(shot_caches, shot_name):
    # delete default scene
    clear_that_beeeeeach()
    mattes_collection = create_collection("mattes")
    # go through caches and load them
    for cache in shot_caches:
        cache_path = pathlib.Path(cache)

        # this way we don't get any unexpected files
        if not cache_path.suffix == ".abc":
            continue

        LOGGER.info(f"Loading {cache_path.stem}")

        # this could be written much nicer but i'm tired
        naming_elements = cache_path.stem.split("_")[-1].split("-")
        if len(naming_elements) > 1:
            cache_name = "_".join(naming_elements[0:-1])
        else:
            cache_name = naming_elements[0]

        LOGGER.info(cache_name)
        create_collection(cache_name)
        imported_objects =  import_alembic(cache)
        root_object = get_imported_root_objects(imported_objects)
        """ get hierarchy here"""
        # select root
        root_object.select_set(True)
        # get hierarchy except selected
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        # get root again
        root_object.select_set(True)
        bpy.context.active_object.scale=(0.01,0.01,0.01)

        for obj in bpy.context.selected_objects:
            if cache_name == "static":
                if deselect_matte(obj):
                    # matte nodes
                    bpy.context.scene.collection.objects.unlink(obj)
                    bpy.data.collections[mattes_collection.name].objects.link(obj)
                # if it is everything else
                else:
                    link_to_collection(obj, cache_name)
            else:
                LOGGER.info(obj.name)
                link_to_collection(obj, cache_name)

        LOGGER.info(f"Loaded and sorted {cache_path.stem} in {cache_name}")
        bpy.ops.object.select_all(action='DESELECT')

    metadata = dictionary_load(shot_name)
    context = metadata.get("context")

    camera_setup(metadata)
    material_assigner.slim_shade(metadata)

    blend_file_name = "_".join(
        [
            context["asset_name"],
            context["shot"],
            "shd_Shading",
            context["version"],
            scene_utils.get_user_abbr(),
        ]
    )
    save_path = os.path.join(
        context["base_path"], "Scenefiles", "shd", "Shading", f"{blend_file_name}_.blend"
    )
    LOGGER.info(f"Saving Scenefile to {save_path}")

    scene_utils.save_scenefile(save_path)
    scene_utils.set_render_paths()


# create collection
def create_collection(cache_name):
    """
    This function takes the cache name and creates a collection named after the cache.
    The function returns the created collection
    :param cache_name:
    :return:
    """
    bpy.data.collections.new(cache_name)
    bpy.context.scene.collection.children.link(bpy.data.collections[cache_name])
    return bpy.data.collections[cache_name]

# get root of imported cache
def get_root(cache):
    """
    This function gets the root of an object hierarchy here
    """
    parent = cache.parent
    # check if parent exists
    if parent:
        return get_root(parent)
    return cache


# get root of import
def get_imported_root_objects(imported_objects):
    """
    This function gets the root object of cache by using get_root()
    """
    imported_root = ""
    for ob in imported_objects:
        imported_root = get_root(ob)
    return imported_root


# import alembic cache
def import_alembic(cache):
    """
    This function imports the cache.
    The function retruns the cached objects
    """
    # Get current objects before import
    pre_import_objects = set(bpy.context.scene.objects)
    # Import the cache
    bpy.ops.wm.alembic_import(filepath=cache)
    # Get objects after import
    post_import_objects = set(bpy.context.scene.objects)
    # Determine the new objects
    imported_objects = post_import_objects - pre_import_objects
    return imported_objects


# link root to collection named after import
def link_to_collection(root_object, collection):
    """
    This function unlinks imported root from other collections and links it to the new created collection
    """
    bpy.context.scene.collection.objects.unlink(root_object)
    bpy.data.collections[collection].objects.link(root_object)


def clear_that_beeeeeach():
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
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)


def camera_setup(metadata):
    """
    This function takes care of the camera settings.
    It creates the driver and uses the pan_locator to match the camera move from maya.
    """
    # get pos of main ctrl
    LOGGER.info(bpy.context.scene.objects["set_room_Layout:prp_camera_Rigging:cam_main_ctrl"].location)
    # create cam on main ctrl pos
    mult_vector = Vector([0.01,0.01,0.01])
    bpy.ops.object.camera_add(
        location=((bpy.context.scene.objects["set_room_Layout:prp_camera_Rigging:cam_main_ctrl"].location.x*mult_vector.x),
                  (bpy.context.scene.objects["set_room_Layout:prp_camera_Rigging:cam_main_ctrl"].location.y*mult_vector.y),
                  (bpy.context.scene.objects["set_room_Layout:prp_camera_Rigging:cam_main_ctrl"].location.z*mult_vector.z)),
        rotation=[1.5708, 0, 0])
    render_cami = bpy.context.active_object
    render_cami.name = "RENDER_CAMI"
    render_cami.data.lens = metadata["cami"]["focal_length"]
    render_cami.data.sensor_fit = 'VERTICAL'
    # ------------------------------------------------------ set camera shift
    # add driver*0.1058  to x
    x_driver = render_cami.data.driver_add('shift_x').driver
    x_driver.type = 'SCRIPTED'
    # create variable for driver
    var = x_driver.variables.new()
    var.name = "locator_x"
    var.type = 'TRANSFORMS'
    # configure the variable to use for the drivers location
    target = var.targets[0]
    target.id = bpy.context.scene.objects["set_room_Layout:prp_camera_Rigging:pan_loc"]
    target.transform_type = 'LOC_X'
    target.transform_space = 'WORLD_SPACE'
    # set driver expression
    x_driver.expression = f"{var.name} * 0.1058"
    # data.shift_x)
    render_cami.data.shift_y = -0.442
    # link camera and locator to cami collection
    link_to_collection(render_cami, "cami")


def deselect_matte(obj):
    """
    This function is used to sort the matte paintings in a collection
    This function returns True if the input object si in the matte dictionary.
    """
    if "walls" in obj.name:
        LOGGER.info(obj.name)
        return True


def get_version(input_path):
    version_folders = os.listdir(os.path.join(input_path))
    versions = []
    for version_folder in version_folders:
        versions.append(int(version_folder.split("_")[0][-3:]))
    max_version = max(versions)
    if max_version < 10:
        max_version_string = "v000" + str(max_version)
    else:
        max_version_string = "v00" + str(max_version)
    max_version_folder = ""
    for version_folder in version_folders:
        if version_folder.startswith(max_version_string):
            max_version_folder = version_folder
    return os.path.join(input_path, max_version_folder)


def dictionary_load(shot_name):
    """
    This function loads the json file and returns the dictionary
    :param shot_name:
    :return:
    """
    json_path = get_version(
        "M:/frogging_hell_prism/02_Library/Shots/" + shot_name + "/Export/Animation/"
    ) + "/centimeter/metadata.json"

    with open(json_path, "r") as json_file:
        metadata_dict = json.load(json_file)

    return metadata_dict
