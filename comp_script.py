# -------------------------------------------------------------------------------- COMP ---------------------------------------------------------------------
    
    # add render layer node
    render_layer_node = nodetree.nodes.new("CompositorNodeRLayers")
    
    # add cryptomatte node
    cryptomatte_node = nodetree.nodes.new("CompositorNodeCryptomatteV2")
    
    # add file output node
    output_node = nodetree.nodes.new("CompositorNodeOutputFile")
    
    # output_node.output_file_add_socket()
    #ä output_file_node.new(Alpha)
    
    # place nodes in comp space
    cryptomatte_node.location = (400,200)
    output_node.location = (1000,100)
    render_layer_node.location = (0,200)

    # connecting nodes
    nodetree.links.new(cryptomatte_node.outputs["Image"],output_node.inputs[0])

    # nodetree.links.new(render_layer_node.outputs["Image"],
    nodetree.links.new(render_layer_node.outputs["CryptoObject00"],cryptomatte_node.inputs[0])
