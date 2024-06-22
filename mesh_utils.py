import bpy
import logging
import pathlib


LOGGER = logging.getLogger("Mesh Stuff")
scene = bpy.context.scene


def get_vert_posisions(obj, dg):
    if not obj.type == 'MESH':
        return None
    eval_obj = obj.evaluated_get(dg)
    mesh_data = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
    vert_list = []
    verts = [eval_obj.matrix_world @ v.co for v in mesh_data.vertices]
    for vert in verts:
        vert_list.extend(vert.freeze())
    return tuple(vert_list)


def get_cache_file(name):
    for cache_file in bpy.data.cache_files:
        cache_path = pathlib.Path(cache_file.name)
        naming_elements = cache_path.stem.split("_")[-1].split("-")

        if len(naming_elements) > 1:
            cache_name = "_".join(naming_elements[0:-1])
        else:
            cache_name = naming_elements[0]

        if name == cache_name:
            return cache_file


def check_animated_frames(collection_names, framerange=None):
    if not framerange:
        framerange = (scene.frame_start, scene.frame_end)

    collection_map = {}
    for collection in collection_names:
        sequence_cache = get_cache_file(collection)
        if sequence_cache:
            collection_map[collection] = {
                "objects": bpy.data.collections.get(collection).all_objects,
                "animated_frames": [scene.frame_start],
                "sequence_cache": sequence_cache,
                "previous_frame_pos": set(),
            }

    for _, collection in collection_map.items():
        collection["sequence_cache"].override_frame = True
        collection["sequence_cache"].frame = scene.frame_start - 1

    dg = bpy.context.evaluated_depsgraph_get()

    for _, collection in collection_map.items():
        for obj in collection["objects"]:
            collection["previous_frame_pos"].add(get_vert_posisions(obj, dg))

    for frame in range(*framerange):
        for _, collection in collection_map.items():
            collection["sequence_cache"].frame = frame

        dg = bpy.context.evaluated_depsgraph_get()

        for _, collection in collection_map.items():
            current_frame_pos = set()

            for obj in collection["objects"]:
                current_frame_pos.add(get_vert_posisions(obj, dg))

            if not collection["previous_frame_pos"] == current_frame_pos:
                collection["animated_frames"].append(frame)

            collection["previous_frame_pos"] = current_frame_pos

    for _, collection in collection_map.items():
        collection["sequence_cache"].override_frame = False

    animated_frames = {}
    for collection in collection_map.keys():
        animated_frames[collection] = collection_map[collection]["animated_frames"]

    return animated_frames
