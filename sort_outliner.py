import bpy

def sort_scene():

    # ------------------------------------------------------------ create collections
    
    # frodo collections
    frodo_collection = bpy.data.collections.new("Frodo")
    mouth_collection = bpy.data.collections.new("Frodo Mouth")
    body_collection = bpy.data.collections.new("Frodo Body")
    
    # bed collections
    bed_collection = bpy.data.collections.new("Berd, The Mighty")
    bed_ball_collection = bpy.data.collections.new("Bed Ball")
    bed_body_collection = bpy.data.collections.new("Bed Body")
    bed_extras_collection = bpy.data.collections.new("Bed Bitch")
    
    # asset collections
    assets_collection = bpy.data.collections.new("Assets")
    canvas_collection = bpy.data.collections.new("Canvas")
    paint_bucket_collection = bpy.data.collections.new("Paint Bucket")
    background_collection = bpy.data.collections.new("Background Assets")
    broom_collection = bpy.data.collections.new("Broom")
    brush_collection = bpy.data.collections.new("Brush")
    foreground_collection = bpy.data.collections.new("Foreground Assets")

    # ------------------------------------------------------------- link to scene collection
    
    # frodo collections
    bpy.context.scene.collection.children.link(frodo_collection)
    frodo_collection.children.link(mouth_collection)
    frodo_collection.children.link(body_collection)
    
    # bed collections
    bpy.context.scene.collection.children.link(bed_collection)
    bed_collection.children.link(bed_ball_collection)
    bed_collection.children.link(bed_body_collection)
    bed_collection.children.link(bed_extras_collection)
    
    # asset collections
    bpy.context.scene.collection.children.link(assets_collection)
    assets_collection.children.link(background_collection)
    assets_collection.children.link(canvas_collection)
    assets_collection.children.link(paint_bucket_collection)
    assets_collection.children.link(foreground_collection)
    assets_collection.children.link(brush_collection)
    assets_collection.children.link(broom_collection)
    
    # ------------------------------------------------------------- sort objects into collections
    
    for ob in bpy.context.scene.objects:
        if type == "MESH":
            ob.scale = (0.01, 0.01, 0.01)
        
        # -------------------------------------------- check if frodo
        if 'chr_frodo' in ob.name:
                      
            # select if so
            ob.select_set(True)
            
            # unlink from other collections
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
                
            # check if teeth
            if 'teeth' in ob.name:
                mouth_collection.objects.link(ob)
            
            # check if tongue
            elif 'tongue' in ob.name:
                mouth_collection.objects.link(ob)
            
            # sort everything else in main collection
            else:
                body_collection.objects.link(ob)
                
        # --------------------------------------------- check if bed
        elif 'prp_bed' in ob.name:
            
            # select object
            ob.select_set(True)
            
            # unlink from other collections
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
                
            # check if balls in namne
            if 'balls' in ob.name:
                bed_ball_collection.objects.link(ob)
            
            # else in bed body collection
            else:
                bed_body_collection.objects.link(ob)
        
        # --------------------------------------------- check if bed extras
        elif ('pillow' in ob.name) or ('blanket' in ob.name):
            
            # select object
            ob.select_set(True)
            
            # unlink from other collections
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
                
            # check if balls in namne
            bed_extras_collection.objects.link(ob)
        
        # sort assets
        else:
            ob.select_set(True)
            
            # unlink from other collections
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
                
            # check if canvas
            if ob.location[1] > -2 :
                foreground_collection.objects.link(ob)
            
            # check if tongue
            elif 'paint_bucket' in ob.name:
                paint_bucket_collection.objects.link(ob)
            
            elif 'canvas' in ob.name:
                canvas_collection.objects.link(ob)
            
            # broom
            elif 'broom' in ob.name:
                broom_collection.objects.link(ob)
            
            # sort everything else in main collection
            else:
                background_collection.objects.link(ob)
    
    # ----------------------------------------------------------- create grease pencil for each collection
    counter = 0
    for coll in bpy.context.scene.collection.children:
        line_art = bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='LRT_COLLECTION')
        # rename object
        if counter == 0:
            rename = "Frodo"
            bpy.data.objects["LineArt"].name = rename
            counter = 1
        elif counter == 1:
            rename = "Berd, the mighty"
            bpy.data.objects["LineArt"].name = rename
            counter+= 1
        else:
            rename = "Assets"
            bpy.data.objects["LineArt"].name = rename
            
    # 
