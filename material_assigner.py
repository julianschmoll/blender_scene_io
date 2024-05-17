import bpy
import os


# texture frodo
def texture_frodo():
    
    fart = "Fart"
    
    # create frodo material
    bpy.data.materials.new(fart)
    
    # assign to varibale so we can use it
    fart_material = bpy.data.materials.get(fart)
    
    # add to frodo
    frodo = bpy.context.active_object
    frodo.data.materials.append(fart_material)
    
    # enable use nodes to make editable
    fart_material.use_nodes = True
    
    # remove default nodes and their connections
    fart_material.node_tree.links.clear()
    fart_material.node_tree.nodes.clear()
    
    # assign connection and node tree
    nodes = fart_material.node_tree.nodes
    links = fart_material.node_tree.links
    
    # create nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    
    # place nodes
    texture_node.location = (0,200)
    output_node.location = (400,200)
    
    # connect nodes
    links.new(texture_node.outputs['Color'], output_node.inputs['Surface'])
    
    # set path
    texture_path = "M:/frogging_hell_prism/02_Library/Assets/Character/chr-frodo/Export/Texturing/v007/frodo_skin/chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.1001.png"
    
    # if texture exists
    if os.path.exists(texture_path):   
        
        # assign loaded image to variable
        image = bpy.data.images.load(texture_path)
        
        # create texture and assign to variable
        texture = bpy.data.textures.new(name="Fart", type='IMAGE')
        
        # assign loaded image to image texture
        texture.image = image
        texture_node.image = image

        # set texture mapping scale
        texture_node.texture_mapping.scale[0] = 1.0
        texture_node.texture_mapping.scale[1] = 1.0
        
        # set color space
        bpy.data.images["chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.004"].colorspace_settings.name = 'ACES - ACEScg'

        
    
# texture bed
def texture_bed():
    return 0

texture_frodo()