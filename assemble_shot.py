from blender_scene_io import material_assigner
from blender_scene_io import scene_utils
from blender_scene_io.texture_dictionary import dictionary_load
from blender_scene_io import comp_script

import logging
import bpy
import os
import pathlib
import math

LOGGER = logging.getLogger("Shot Assembly")
scene = bpy.context.scene

def load_shot(shot_caches, shot_name):
    view_layer = bpy.context.view_layer
    view_layer.name = "MasterLayer"
    view_layer.use_pass_combined = True
    view_layer.use_pass_z = True
    view_layer.use_pass_normal = True
    view_layer.eevee.use_pass_transparent = True

    # delete default scene
    scene_utils.clear_scene()

    for cache in shot_caches:
        load_cache_in_collection(cache)

    metadata = dictionary_load(shot_name)
    cam_bake = dictionary_load(shot_name, json_file_name="camera")

    camera_setup(cam_bake, overscan=15)
    material_assigner.slim_shade(metadata)

    for collection in bpy.data.collections:
        create_renderlayer_from_collection(collection)

    create_grease_layer()
    create_clean_layer()

    bpy.context.window.view_layer = bpy.context.scene.view_layers['MasterLayer']

    comp_script.comp_setup()

    scene_utils.save_scenefile(assemble_save_path(metadata.get("context")))
    scene_utils.set_render_paths()
    bpy.context.scene.eevee.taa_render_samples = 1
    bpy.context.scene.eevee.taa_samples = 1
    scene_utils.set_time_slider_view()


def create_clean_layer():
    bpy.ops.scene.view_layer_add(type='EMPTY')

    view_layer = bpy.context.view_layer
    view_layer.name = "NoGreaseLayer"
    view_layer.use_pass_combined = True
    view_layer.use_pass_z = True
    view_layer.use_pass_normal = True
    view_layer.eevee.use_pass_transparent = True

    wanted_collections = []

    for collection in bpy.data.collections:
        if "_grease" not in collection.name:
            wanted_collections.append(collection)

    include_collections(view_layer, wanted_collections)


def create_grease_layer():
    bpy.ops.scene.view_layer_add(type='EMPTY')

    view_layer = bpy.context.view_layer
    view_layer.name = "GreaseLayer"
    view_layer.use_pass_combined = True
    view_layer.use_pass_z = True
    view_layer.use_pass_normal = True
    view_layer.eevee.use_pass_transparent = True

    holdout_collections = []

    for collection in bpy.data.collections:
        if "_grease" not in collection.name:
            holdout_collections.append(collection)

    collections = [collection for collection in bpy.data.collections]
    include_collections(view_layer, collections)
    for collection in holdout_collections:
        holdout_collection(view_layer, collection)


def assemble_save_path(context):
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
    return save_path


def create_renderlayer_from_collection(collection):
    layer_name = collection.name.replace("_", " ").title().replace(" ", "")
    bpy.ops.scene.view_layer_add(type='EMPTY')
    view_layer = bpy.context.view_layer
    view_layer.name = f"{layer_name}Layer"
    view_layer.use_pass_combined = True
    view_layer.use_pass_z = True
    view_layer.use_pass_normal = True
    view_layer.eevee.use_pass_transparent = True
    include_collections(view_layer, [collection])
    bpy.context.scene.render.film_transparent = True

    if not collection.name.endswith("_grease"):
        return

    corresponding_collection = bpy.data.collections.get(collection.name.removesuffix("_grease"))
    if not corresponding_collection:
        return

    include_collections(view_layer, [collection, corresponding_collection])
    holdout_collection(view_layer, corresponding_collection)


def holdout_collection(view_layer, collection):
    for layer_collection in view_layer.layer_collection.children:
        if layer_collection.collection == collection:
            layer_collection.holdout = True


def load_cache_in_collection(cache):
    cache_path = pathlib.Path(cache)

    if not cache_path.suffix == ".abc":
        return

    LOGGER.info(f"Loading {cache_path.stem}")
    naming_elements = cache_path.stem.split("_")[-1].split("-")

    if len(naming_elements) > 1:
        cache_name = "_".join(naming_elements[0:-1])
    else:
        cache_name = naming_elements[0]

    collection = create_collection(cache_name, unique=False)
    imported_objects = import_alembic(cache)
    root_object = get_imported_root_objects(imported_objects)
    root_object.select_set(True)

    bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')

    root_object.select_set(True)
    bpy.context.active_object.scale = (0.01, 0.01, 0.01)

    for obj in bpy.context.selected_objects:
        if cache_name == "static":
            if deselect_matte(obj):
                # matte nodes
                bpy.context.scene.collection.objects.unlink(obj)
                mattes_collection = create_collection("mattes", unique=False)
                mattes_collection.objects.link(obj)
            # if it is everything else
            else:
                link_to_collection(obj, collection)
        else:
            LOGGER.info(obj.name)
            link_to_collection(obj, collection)

    LOGGER.info(f"Loaded and sorted {cache_path.stem} in {collection}")
    bpy.ops.object.select_all(action='DESELECT')


def create_collection(collection_name, unique=True):
    if unique:
        collection_name = get_unique_collection_name(collection_name)
    elif bpy.data.collections.get(collection_name):
        return bpy.data.collections.get(collection_name)
    bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(bpy.data.collections[collection_name])
    return bpy.data.collections[collection_name]


def get_unique_collection_name(name):
    counter = 1
    original_name = name
    while bpy.data.collections.get(name):
        name = f"{original_name}_{counter:02d}"
        counter += 1
    return name


def get_root(cache):
    """
    This function gets the root of an object hierarchy here
    """
    parent = cache.parent
    # check if parent exists
    if parent:
        return get_root(parent)
    return cache


def include_collections(view_layer, collections):
    for layer_collection in view_layer.layer_collection.children:
        if layer_collection.collection not in collections:
            layer_collection.exclude = True
        else:
            layer_collection.exclude = False


def get_imported_root_objects(imported_objects):
    """
    This function gets the root object of cache by using get_root()
    """
    imported_root = ""
    for ob in imported_objects:
        imported_root = get_root(ob)
    return imported_root


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
    collection.objects.link(root_object)


def camera_setup(cam_bake, overscan=0):
    """Sets up camera from Maya bake data.

    Args:
        cam_bake: Dictionary with Cam Values from Maya
        overscan: Overscan in Percent

    Returns:
        cam: Camera Node in Blender
    """
    scale_fac = add_overscan(overscan)
    bpy.ops.object.camera_add()
    render_cami = bpy.context.active_object
    render_cami.name = "render_cami"
    render_cami.data.sensor_fit = 'VERTICAL'

    for frame, frame_data in cam_bake.items():
        vertical_film_aperture = frame_data.get("vertical_film_aperture") or 1
        filmback_factor = 1 / vertical_film_aperture
        frame = int(frame)

        tx, ty, tz = frame_data["translation"]
        rx, ry, rz = frame_data["rotation"]

        render_cami.location = (tx / 100, -tz / 100, ty / 100)
        render_cami.rotation_euler = (
            math.radians(rx+90),
            math.radians(rz),
            math.radians(ry)
        )

        render_cami.data.lens = frame_data["focal_length"] * scale_fac
        render_cami.data.shift_x = frame_data["horizontal_pan"] * scale_fac * filmback_factor
        render_cami.data.shift_y = frame_data["vertical_pan"] * scale_fac * filmback_factor

        render_cami.keyframe_insert("location", frame=frame)
        render_cami.keyframe_insert("rotation_euler", frame=frame)
        render_cami.data.keyframe_insert('shift_x', frame=frame)
        render_cami.data.keyframe_insert('shift_y', frame=frame)
        render_cami.data.keyframe_insert('lens', frame=frame)

    bpy.context.scene.camera = render_cami

    return render_cami


def add_overscan(overscan):
    overscan_fac = 1 + (overscan / 100)
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    scene.render.resolution_x = int(res_x * overscan_fac)
    scene.render.resolution_y = int(res_y * overscan_fac)
    scale_fac = res_x / scene.render.resolution_x

    return scale_fac


def deselect_matte(obj):
    """This function does blah.

    Longer description can be written here.

    Args:
        obj (bpy.something.something): What is this

    Returns:

    """
    # added plane here because apparently this is a name we use for mattes
    # and come on, if we want something to be shaded correctly lets not name it plane
    if "walls" in obj.name.lower() or "plane" in obj.name.lower() or "tintoy" in obj.name.lower() or "gertie" in obj.name.lower():
        LOGGER.info(obj.name)
        return True
    return False
