import bpy

def sort_scene():

    # create collections
    frodo_collection = bpy.data.collections.new("Frodo")
    bed_collection = bpy.data.collections.new("Berd, the mighty")
    assets_collection = bpy.data.collections.new("Assets")

    # link to scene collection
    bpy.context.scene.collection.children.link(frodo_collection)
    bpy.context.scene.collection.children.link(bed_collection)
    bpy.context.scene.collection.children.link(assets_collection)

    # go through outliner
    for ob in bpy.context.scene.objects:
        if type == "MESH":
            ob.scale = (0.01, 0.01, 0.01)
        # sort frodo parts
        if 'chr_frodo' in ob.name:
            ob.select_set(True)
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
            frodo_collection.objects.link(ob)
        # sort bed
        elif 'prp_bed' in ob.name:
            ob.select_set(True)
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
            bed_collection.objects.link(ob)
        # sort assets
        else:
            ob.select_set(True)
            for other_col in ob.users_collection:
                other_col.objects.unlink(ob)
            assets_collection.objects.link(ob)
    
    # create grease pencil for each collection
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
            
if __name__ == "__main__":
    sort_scene()