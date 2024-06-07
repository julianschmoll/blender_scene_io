from blender_scene_io import texture_dictionary
import bpy
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

# -------------------------------------------------------------------------------- COMP ---------------------------------------------------------------------
def comp_setup():
    basic_comp_setup()


def pick_cryptomatte_materials(material_names, cryptomatte_node):
    cryptomatte_node.matte_id = ",".join(material_names)

def basic_comp_setup():
    """
    This function clears the default compositing nodes, enables nodes and createes our node setup
    :return:
    """
    # use nodes and clear default scene
    bpy.context.scene.use_nodes = True
    nodetree = bpy.context.scene.node_tree
    nodetree.links.clear()
    nodetree.nodes.clear()
    # add render layer node
    render_layer_node = nodetree.nodes.new("CompositorNodeRLayers")
    # add cryptomatte node
    frodo_cryptomatte_node = nodetree.nodes.new("CompositorNodeCryptomatteV2")
    # add second cryptomatte node
    bed_cryptomatte_node = nodetree.nodes.new("CompositorNodeCryptomatteV2")
    # add file output node
    output_node = nodetree.nodes.new("CompositorNodeOutputFile")
    # add viewer node
    viewer_node = nodetree.nodes.new("CompositorNodeViewer")
    # add slots ro node
    LOGGER.info(output_node.name)
    output_node.layer_slots.new("Cryptomatte_Frodo")
    output_node.layer_slots.new("Cryptomatte_Bed")
    # place nodes in comp space
    frodo_cryptomatte_node.location = (400,400)
    bed_cryptomatte_node.location = (400,-200)
    output_node.location = (1000,100)
    viewer_node.location = (1000, 400)
    render_layer_node.location = (0,200)
    # ---------------------------------------------------------------------------- connecting nodes
    # render layer to output
    nodetree.links.new(render_layer_node.outputs["Image"],output_node.inputs["Image"])
    # crypto to output
    nodetree.links.new(frodo_cryptomatte_node.outputs["Image"],output_node.inputs["Cryptomatte_Frodo"])
    nodetree.links.new(bed_cryptomatte_node.outputs["Image"],output_node.inputs["Cryptomatte_Bed"])
    nodetree.links.new(render_layer_node.outputs["Image"],bed_cryptomatte_node.inputs["Image"])
    #nodetree.links.new(bed_cryptomatte_node.outputs["Matte"]),output_node.inputs["Cryptomatte_Bed"]
    # render layer to cryptomatte
    nodetree.links.new(render_layer_node.outputs["Image"],frodo_cryptomatte_node.inputs["Image"])
    # cryptomatte to viewer
    nodetree.links.new(frodo_cryptomatte_node.outputs["Matte"], viewer_node.inputs["Image"])
    # nodetree.links.new(render_layer_node.outputs["Image"],bed_cryptomatte_node.inputs[0])
    frodo_cryptomatte_node.layer_name = 'ViewLayer.CryptoObject'
    bed_cryptomatte_node.layer_name = 'ViewLayer.CryptoObject'
    pick_cryptomatte_materials(texture_dictionary.frodo_list,frodo_cryptomatte_node)
    pick_cryptomatte_materials(texture_dictionary.bed_list,bed_cryptomatte_node)
