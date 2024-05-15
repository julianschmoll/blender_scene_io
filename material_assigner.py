import bpy


# texture frodo
def texture_frodo():
    
    fart = "Fart"
    
    bpy.data.materials.new(fart)
    fart_material = bpy.data.materials.get(fart)
    fart_material.use_nodes = True
    fart_material.node_tree.links.clear()
    fart_material.node_tree.nodes.clear()
    # create nodes
    nodes = fart_material.node_tree.nodes
    links = fart_material.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    image = nodes.new(type='ShaderNodeTexImage')
    # place nodes
    image.location = (0,200)
    output.location = (400,200)
    # connect nodes
    links.new(image.outputs['Color'], output.inputs['Surface'])
    # set path and select color space
    image_path = ""
    texture_path = bpy.data.images.load(image_path)
    texture_path.image = texture_path
    
    
    
# texture bed
def texture_bed():
    return 0

texture_frodo()