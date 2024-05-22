import logging
import bpy
import os

LOGGER = logging.getLogger("Frogging Hell Menu")

def load_shot(shot_caches):

    import_group = []
    # go through caches and load them
    for cache in shot_caches:
        # log cache import
        LOGGER.info(f"Loading {cache}")
        cache_name= split_cache(cache)
        cache_collection = create_collection(cache_name)
        imported_objects =  import_alembic(cache)
        root_object = get_imported_root_objects(imported_objects)
        for child in bpy.data
        link_to_collection(root_object,cache_name)
        LOGGER.info(f"Loaded and sorted {cache_name} in collection")

# create collection
def create_collection(cache_name):
    bpy.data.collections.new(cache_name)
    bpy.context.scene.collection.children.link(bpy.data.collections[cache_name])
    return bpy.data.collections[cache_name]

# get root of imported cache
def get_root(cache):
    """Get the root of an object hierarchy here"""
    parent = cache.parent
    # check if parent exists
    if parent:
        return get_root(parent)
    return cache

# get root of import
def get_imported_root_objects(imported_objects):
    """Get the root object of cache"""
    imported_root = ""
    for ob in imported_objects:
        imported_root = get_root(ob)
    return imported_root

# import alembic cache
def import_alembic(cache):
    """Import cache and return names of import."""
    # Get current objects before import
    pre_import_objects = set(bpy.context.scene.objects)
    # Import the cache
    bpy.ops.wm.alembic_import(filepath=cache)
    # Get objects after import
    post_import_objects = set(bpy.context.scene.objects)
    # Determine the new objects
    imported_objects = post_import_objects - pre_import_objects
    return imported_objects

# link root to collection named after import
def link_to_collection(root_object, collection):
    """Unlink imported root from other collections and link it to the new created collection"""
    bpy.context.scene.collection.objects.unlink(root_object)
    bpy.data.collections[collection].objects.link(root_object)


# get cache name from path
def split_cache(cache):
    cache_name = os.path.basename(cache)
    return cache_name.split("_")[-1].rstrip(".abc")

def getChildren(root_object, imported_objects):
    children = []
    for ob in imported_objects:
        if ob.parent == root_object:
            children.append(ob)
    return children