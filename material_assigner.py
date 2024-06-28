import bpy
import logging

from blender_scene_io.grease import apply_grease_pencil

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
    bpy.data.materials.new(f"{name}_material")
    material = bpy.data.materials.get(f"{name}_material")
    node.data.materials.append(material)
    material.use_nodes = True
    material.node_tree.links.clear()
    material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    transparent_node = nodes.new(type='ShaderNodeBsdfTransparent')
    mix_shader_node = nodes.new(type='ShaderNodeMixShader')

    texture_node.location = (0,200)
    transparent_node.location = (450,450)
    mix_shader_node.location = (700,300)
    output_node.location = (900,300)

    links.new(texture_node.outputs['Alpha'], mix_shader_node.inputs['Fac'])
    links.new(transparent_node.outputs['BSDF'], mix_shader_node.inputs[1])
    links.new(texture_node.outputs['Color'], mix_shader_node.inputs[2])
    links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Surface'])

    try:
        image = bpy.data.images.load(path)
    except RuntimeError:
        LOGGER.error(f"Could not load image which should be located at {path}")
        return

    texture = bpy.data.textures.new(name="{name}_base_color", type='IMAGE')

    texture.image = image
    texture_node.image = image

    texture_node.texture_mapping.scale[0] = 1.0
    texture_node.texture_mapping.scale[1] = 1.0

    texture_node.image.colorspace_settings.name = 'ACES - ACEScg'

    material.blend_method = 'HASHED'


def apply_cell_shader(node, color=None, factor=None, name="standard_cel_shader", ramp_range=0.3):
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

    if factor:
        color_ramp_node.inputs[0].default_value = 0.4

    links.new(color_ramp_node.outputs['Color'], output_node.inputs['Surface'])
    node.data.materials.append(cel_shader)


def slim_shade(texture_dict):
    LOGGER.info("Setting up Shaders...")
    for collection in bpy.data.collections:
        if "mattes" not in collection.name:
            apply_grease_pencil(collection)
            for obj in bpy.data.collections[collection.name].objects:
                if obj.type == 'MESH':
                    subsurf = obj.modifiers.new(name='Subdivision', type='SUBSURF')
                    subsurf.levels = 0
                    subsurf.render_levels = 2

        apply_shader(collection, texture_dict)
