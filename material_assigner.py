from blender_scene_io import texture_dictionary

import bpy
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

def texture_path(collection, input_dictionary):
    """This function finds a texture for every object that has one.
        The function iterates through all objects in the input collection.
        If it's a mesh and has a key, this function will use the function create_image_texture_material
        (it creates a new image texture material for each object that has an entry in a dictionary).
        input_dictionary is a string that is a key in the big texture_dict.

    """
    # iterate through input collection
    for obj in bpy.data.collections[collection.name].objects:
        # if object is a mesh continue
        if obj.type == 'MESH':
            # go through dictionaries in big dictionary
            for key in texture_dictionary.texture_dict:
                # check if collection has a key in big dictionary
                if key == input_dictionary:
                    for input_key in texture_dictionary.texture_dict[input_dictionary]:
                        # check if names are the same
                        if obj.name != input_key:
                            # if not go to next key
                            continue
                        else:
                            # check if texture image exists
                            if os.path.exists(texture_dictionary.texture_dict[input_dictionary][input_key]):
                                texture_material = input_key.split(":")[-1]
                                # create new material named after key
                                create_image_texture_material(obj, texture_material, texture_dictionary.texture_dict[input_dictionary][input_key])

def create_image_texture_material(obj,texture_material,path):
    """
    This function creates a new image texture material node, links it to an output node.
    The new material is named after the key in the dictionary (eg. frog_whole_pants).
    It is then assigned to the obj which matches the keys name.
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
    texture_node.image.colorspace_settings.name = 'ACES - ACEScg'
    # bpy.data.images["chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.001"].colorspace_settings.name = 'ACES - ACEScg'

def cel_shade():
    """This function creates a Cel Shader and assigns it to all objects in the stati collection"""
    # create Cel Shader material
    bpy.data.materials.new('Cel Shader')
    # get Cel Shader material
    cel_shader = bpy.data.materials.get('Cel Shader')
    cel_shader.use_nodes=True
    # remove default nodes and their connections
    cel_shader.node_tree.links.clear()
    cel_shader.node_tree.nodes.clear()
    # assign connection and node tree
    nodes = cel_shader.node_tree.nodes
    links = cel_shader.node_tree.links
    # create nodes
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    shader_to_rgb_node = nodes.new(type='ShaderNodeShaderToRGB')
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    # place nodes
    bsdf_node.location = (0, 200)
    shader_to_rgb_node.location = (400,200)
    color_ramp_node.location = (800,200)
    output_node.location = (1200, 200)
    # connect nodes
    links.new(bsdf_node.outputs['BSDF'],shader_to_rgb_node.inputs['Shader'])
    links.new(shader_to_rgb_node.outputs['Color'],color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'],output_node.inputs['Surface'])
    # loop through all objects in stati and assign the shader
    for obj in bpy.data.collections['stati'].objects:
        if obj.type=='MESH':
            obj.data.materials.append(cel_shader)

def guilded_grease(collection):
    # create gpencil and name it
    gpencil_data = bpy.data.grease_pencils.new(name=collection.name)
    gpencil_object = bpy.data.objects.new(name=collection.name + "_GP", object_data=gpencil_data)
    # add it to the collection
    bpy.data.collections[collection.name].objects.link(gpencil_object)
    # create a new gpencil layer
    gp_layer = gpencil_data.layers.new(name=collection.name+"_layer", set_active=True)
    # create a gpencil frame
    gp_frame = gp_layer.frames.new(0)
    # create a Line Art modifier for the gpencil object
    lineart_mod = gpencil_object.grease_pencil_modifiers.new(name="LineArt", type='GP_LINEART')
    # create modifier layer
    lineart_mod.target_layer = collection.name+"_layer"
    # create material for lines
    gp_mat = bpy.data.materials.new(name=collection.name + "_Black")
    gpencil_data.materials.append(gp_mat)
    # select gp material
    lineart_mod.target_material = gp_mat
    # don't use crease pls man
    lineart_mod.use_crease = False
    # Set the target collection for the Line Art modifier
    lineart_mod.source_collection = collection
    # show in viewport
    lineart_mod.show_render=True
    lineart_mod.show_viewport=True
    # make thinner
    lineart_mod.thickness = 10
    # subdivide gpencil
    subdiv_mod = gpencil_object.grease_pencil_modifiers.new(name="Subdivision", type="GP_SUBDIV")
    subdiv_mod.level=5
    # Return the created Grease Pencil object
    return gpencil_object

def slim_shade():
    LOGGER.info("Running Shader Script...")
    cel_shade()
    for collection in bpy.data.collections:
        if collection.name != "cami":
            texture_path(collection, collection.name.replace("-","_")+"_dict")
            guilded_grease(collection)