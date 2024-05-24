from blender_scene_io import texture_dictionary

import bpy
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

# texture frodo
def texture_objects_in_scene():

    LOGGER.info("Running Texture Script...")

    texture_dict = texture_dictionary.texture_dict
    # go through dictionary
    for obj in bpy.data.objects:
        # loop through dictionary
        for key in texture_dict:
            # check if names are the same
            if obj.name!=key:
                # if not go to next key
                continue
            else:
                # check if texture image exists
                if os.path.exists(texture_dict.value):
                    texture_material = key.split(":")[-1]
                    # create new material named after key
                    create_material(obj,texture_material,texture_dictionary.value)

def create_material(obj,texture_material,path):
    """
    This function creates a new image texture material node, links it to an output node.
    The new material is named after the key in the dictionary (eg. frog_whole_pants).
    It is thenm assigned to the obj which matches the keys name.
    The key's value is used as the path to load the image.

    """
    # create frodo material
    bpy.data.materials.new(texture_material)
    # assign to varibale so we can use it
    new_material = bpy.data.materials.get(texture_material)
    # add to obj
    obj.data.materials.append(new_material)
    # enable use nodes to make editable
    new_material.use_nodes = True
    # remove default nodes and their connections
    new_material.node_tree.links.clear()
    new_material.node_tree.nodes.clear()
    # assign connection and node tree
    nodes = new_material.node_tree.nodes
    links = new_material.node_tree.links
    # create nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    # place nodes
    texture_node.location = (0,200)
    output_node.location = (400,200)
    # connect nodes
    links.new(texture_node.outputs['Color'], output_node.inputs['Surface'])
    # assign loaded image to variable
    image = bpy.data.images.load(path)
    # create texture and assign to variable
    texture = bpy.data.textures.new(name=texture_material, type='IMAGE')
    # assign loaded image to image texture
    texture.image = image
    texture_node.image = image
    # set texture mapping scale
    texture_node.texture_mapping.scale[0] = 1.0
    texture_node.texture_mapping.scale[1] = 1.0
    # set color space
    bpy.data.images["chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.004"].colorspace_settings.name = 'ACES - ACEScg'