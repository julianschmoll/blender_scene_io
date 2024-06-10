import os
import logging
import json

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def dictionary_load(shot_name, json_file_name="metadata"):
    """
    This function loads the json file and returns the dictionary
    :param shot_name:
    :return:
    """
    export_path = get_highest_version(
        os.path.join(
            "M:/frogging_hell_prism", "02_Library", "Shots", shot_name, "Export", "Animation"
        )
    )

    json_path = os.path.join(export_path, "centimeter", f"{json_file_name}.json")

    with open(json_path, "r") as json_file:
        metadata_dict = json.load(json_file)

    return metadata_dict


def get_highest_version(input_path):
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
