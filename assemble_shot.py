import logging
import bpy
import os

LOGGER = logging.getLogger("Frogging Hell Menu")

def load_shot(shot_caches):
    # go through caches and load them
    for cache in shot_caches:
        # cache_collection =
        LOGGER.info(f"Loading {cache}")
        cache_name = os.path.basename(cache)
        cache_name = cache_name[13:-4]
        bpy.ops.collection.create(name = cache_name)
        LOGGER.info(f"Collection: {cache_name}")
        bpy.context.scene.collection.children.link(bpy.data.collections[cache_name])
        bpy.ops.wm.alembic_import(filepath=cache)

caches = ['M:\\frogging_hell_prism\\02_Library\\Shots\\500-010\\Export\\Animation\\v0011_arms-fixxed_lre\\centimeter\\shot_500-010_chr-frodo-rig.abc', 'M:\\frogging_hell_prism\\02_Library\\Shots\\500-010\\Export\\Animation\\v0011_arms-fixxed_lre\\centimeter\\shot_500-010_prp-bed-rig.abc']
load_shot(caches)