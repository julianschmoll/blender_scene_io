import bpy
import logging

LOGGER = logging.getLogger("Material Assigner")


def apply_shader(collection, metadata_dict):
    """This function finds a texture for every object that has one.
        The function iterates through all objects in the input collection.
        If it's a mesh and has a key, this function will use the function create_image_texture_material
        (it creates a new image texture material for each object that has an entry in a dictionary).
        input_dictionary is a string that is a key in the big texture_dict.

    """
    texture_map =  metadata_dict["textures"]

    for node in bpy.data.collections[collection.name].objects:
        name = node.name

        if not node.type == 'MESH':
            continue

        if not name in texture_map:
            LOGGER.warning(
                f"No Texture or base color defined for {name}, applying standard cell shader"
            )
            apply_cell_shader(node)
            continue

        node_data = texture_map[name]
        texture_filepath = node_data.get("filepath")

        if texture_filepath:
            LOGGER.info(f"Assigning {texture_filepath} to {name}")
            apply_texture(node, f"{name}_material", texture_filepath)

        else:
            color = node_data.get("based_color")
            LOGGER.info(f"Shading {node.name} with based color {color}.")
            apply_cell_shader(node, color=color, name=f"{name}_cel_shader")


def apply_texture(node, name, path):
    """
    This function creates a new image texture material node, links it to an output node.
    The new material is named after the key in the dictionary (eg. frog_whole_pants).
    It is then assigned to the obj which matches the keys name.
    The key's value is used as the path to load the image.
    """
    # create frodo material
    bpy.data.materials.new(f"{name}_material")
    # assign to varibale so we can use it
    material = bpy.data.materials.get(f"{name}_material")
    # add to obj
    node.data.materials.append(material)
    # enable use nodes to make editable
    material.use_nodes = True
    # remove default nodes and their connections
    material.node_tree.links.clear()
    material.node_tree.nodes.clear()
    # assign connection and node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    # create nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    transparent_node = nodes.new(type='ShaderNodeBsdfTransparent')
    mix_shader_node = nodes.new(type='ShaderNodeMixShader')
    # place nodes
    texture_node.location = (0,200)
    transparent_node.location = (450,450)
    mix_shader_node.location = (700,300)
    output_node.location = (900,300)
    # connect nodes
    links.new(texture_node.outputs['Alpha'], mix_shader_node.inputs['Fac'])
    links.new(transparent_node.outputs['BSDF'], mix_shader_node.inputs[1])
    links.new(texture_node.outputs['Color'], mix_shader_node.inputs[2])
    links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Surface'])
    # assign loaded image to variable
    try:
        image = bpy.data.images.load(path)
    except RuntimeError:
        LOGGER.error(f"Could not load image which should be located at {path}")
        return
    # create texture and assign to variable
    texture = bpy.data.textures.new(name="{name}_base_color", type='IMAGE')
    # assign loaded image to image texture
    texture.image = image
    texture_node.image = image
    # set texture mapping scale
    texture_node.texture_mapping.scale[0] = 1.0
    texture_node.texture_mapping.scale[1] = 1.0
    # set color space
    texture_node.image.colorspace_settings.name = 'ACES - ACEScg'
    # set alpha blend
    material.blend_method = 'HASHED'


def apply_cell_shader(node, color=None, name="standard_cel_shader", ramp_range=0.3):
    """
    This function creates a Cel Shader and assigns it to all objects in the stati collection
    """
    bpy.data.materials.new(name)
    cel_shader = bpy.data.materials.get(name)
    cel_shader.use_nodes=True

    cel_shader.node_tree.links.clear()
    cel_shader.node_tree.nodes.clear()

    nodes = cel_shader.node_tree.nodes
    links = cel_shader.node_tree.links

    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')

    color_ramp_node.location = (800,200)
    output_node.location = (1200, 200)

    if color:
        red_value, green_value, blue_value = color
        color_offset = ramp_range/2
        color_ramp_node.color_ramp.elements[0].color = (
            red_value - color_offset,
            green_value - color_offset,
            blue_value - color_offset,
            1
        )
        color_ramp_node.color_ramp.elements[1].color = (
            red_value + color_offset,
            green_value + color_offset,
            blue_value + color_offset,
            1
        )

    links.new(color_ramp_node.outputs['Color'], output_node.inputs['Surface'])
    node.data.materials.append(cel_shader)


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


def slim_shade(texture_dict):
    LOGGER.info("Setting up Shaders...")
    for collection in bpy.data.collections:
        if "cami" in collection.name:
            continue

        if "mattes" not in collection.name:
            guilded_grease(collection)
            for obj in bpy.data.collections[collection.name].objects:
                if obj.type == 'MESH':
                    subsurf = obj.modifiers.new(name='Subdivision', type='SUBSURF')
                    subsurf.levels = 0
                    subsurf.render_levels = 2

        apply_shader(collection, texture_dict)
