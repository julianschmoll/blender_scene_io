import bpy
import logging


LOGGER = logging.getLogger("Comp Setup")


def pick_cryptomatte_materials(cryptomatte_node, collection):
    material_names = []
    for obj in bpy.data.collections[collection].objects:
        if obj.type == 'MESH':
            material_names.append(obj.name)
    cryptomatte_node.matte_id = ",".join(material_names)


def comp_setup():
    nodetree = prepare_nodetree()
    master_layer = nodetree.nodes.new("CompositorNodeRLayers")
    output_node = nodetree.nodes.new("CompositorNodeOutputFile")

    output_node.layer_slots.new("rgb")
    output_node.layer_slots.new("alpha")
    nodetree.links.new(master_layer.outputs["Image"],output_node.inputs["Image"])
    nodetree.links.new(master_layer.outputs["Image"], output_node.inputs["rgb"])
    nodetree.links.new(master_layer.outputs["Alpha"], output_node.inputs["alpha"])

    setup_render_layers(nodetree, output_node)
    setup_crypto_mattes(master_layer, nodetree, output_node)


def prepare_nodetree():
    bpy.context.scene.use_nodes = True
    nodetree = bpy.context.scene.node_tree
    nodetree.links.clear()
    nodetree.nodes.clear()
    return nodetree


def setup_crypto_mattes(master_layer, nodetree, output_node):
    for coll in bpy.data.collections:
        if coll.name.lower() not in ["static", "mattes", "cami"]:
            crypto_matte = nodetree.nodes.new("CompositorNodeCryptomatteV2")
            output_node.layer_slots.new(f"{coll.name}_crypto")
            nodetree.links.new(master_layer.outputs["Image"], crypto_matte.inputs["Image"])
            nodetree.links.new(crypto_matte.outputs["Image"], output_node.inputs[f"{coll.name}_crypto"])
            crypto_matte.layer_name = "MasterLayer.CryptoObject"
            pick_cryptomatte_materials(crypto_matte, coll.name)


def setup_render_layers(nodetree, output_node):
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            if view_layer.name == "MasterLayer":
                continue
            render_layer = nodetree.nodes.new("CompositorNodeRLayers")
            render_layer.layer = view_layer.name
            output_node.layer_slots.new(view_layer.name)
            nodetree.links.new(render_layer.outputs["Image"], output_node.inputs[view_layer.name])
