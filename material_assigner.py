import bpy
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("material")

def texture_path(collection,texture_dict):
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
            if obj.name in texture_dict["textures"]:
                # check if texture image exists
                if texture_dict["textures"][obj.name] == '':
                    continue
                LOGGER.info(obj.name)
                texture_material = obj.name.split(":")[-1]
                # create new material named after key
                create_image_texture_material(obj, texture_material, texture_dict["textures"][obj.name])
            else:
                cel_shade(obj)

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

def cel_shade(obj):
    """
    This function creates a Cel Shader and assigns it to all objects in the stati collection
    """
    LOGGER.info(obj)
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
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    # place nodes
    color_ramp_node.location = (800,200)
    output_node.location = (1200, 200)
    # connect nodes
    links.new(color_ramp_node.outputs['Color'],output_node.inputs['Surface'])
    # loop through all objects in stati and assign the shader
    obj.data.materials.append(cel_shader)

def guilded_grease(collection):
    """
    :param collection: Collection to apply the grease pencil line art object on
    :return: the newly created line art object
    """
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
    subdiv_mod.level=2
    # Return the created Grease Pencil object
    return gpencil_object

def shade_teeth(collection):
    """
    This function shades the teeth
    :return:
    """
    if "frodo" in collection.name:
        for obj in collection.objects:
            if (obj.type == "MESH") and ("teeth" in obj.name):
                cel_shade(obj)

def slim_shade(texture_dict):
    LOGGER.info("Running Shader Script...")
    for collection in bpy.data.collections:
        if "cami" in collection.name:
            continue
        else:
            shade_teeth(collection)
            if "mattes" not in collection.name:
                guilded_grease(collection)
                for obj in bpy.data.collections[collection.name].objects:
                    if obj.type == 'MESH':
                        subsurf = obj.modifiers.new(name='Subdivision', type='SUBSURF')
                        subsurf.levels = 0
                        subsurf.render_levels = 2
            texture_path(collection,texture_dict)
