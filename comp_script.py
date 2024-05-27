from blender_scene_io import texture_dictionary

import bpy
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

# -------------------------------------------------------------------------------- COMP ---------------------------------------------------------------------

def pick_cryptomatte_materials(material_names, cryptomatte_node):
    for name in material_names:
        cryptomatte_node.matte_id = name
        bpy.ops.compositor.cryptomatte_add()

def basic_comp_setup():
    bpy.context.scene.use_nodes = True
    nodetree = bpy.context.scene.node_tree
    nodetree.links.clear()
    nodetree.nodes.clear()
    # add render layer node
    render_layer_node = nodetree.nodes.new("CompositorNodeRLayers")
    # add cryptomatte node
    frodo_cryptomatte_node = nodetree.nodes.new("CompositorNodeCryptomatteV2")
    # add file output node
    output_node = nodetree.nodes.new("CompositorNodeOutputFile")
    # add slots ro node
    output_node.layer_slots.new("Cryptomatte")
    # place nodes in comp space
    frodo_cryptomatte_node.location = (400,200)
    output_node.location = (1000,100)
    render_layer_node.location = (0,200)
    # ---------------------------------------------------------------------------- connecting nodes
    # render layer to output
    nodetree.links.new(render_layer_node.outputs["Image"],output_node.inputs["Image"])
    # crypto to output
    nodetree.links.new(frodo_cryptomatte_node.outputs["Matte"],output_node.inputs["Cryptomatte"])
    # render layer to crypto
    nodetree.links.new(render_layer_node.outputs["Image"],frodo_cryptomatte_node.inputs[0])
    LOGGER.info("Running Comp Script...")
    pick_cryptomatte_materials(texture_dictionary.frodo_list,frodo_cryptomatte_node)