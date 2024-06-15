import bpy
import logging


LOGGER = logging.getLogger("Grease Utils")


def apply_grease_pencil(collection):
    """
    :param collection: Collection to apply the grease pencil line art object on
    :return: the newly created line art object
    """
    gpencil_data = bpy.data.grease_pencils.new(name=collection.name)
    gpencil_object = bpy.data.objects.new(
        name=f"{collection.name}_gp", object_data=gpencil_data
    )
    gp_layer = gpencil_data.layers.new(
        name=f"{collection.name}_gp_layer", set_active=True
    )
    gp_layer.frames.new(0)

    gp_mat = add_material(collection, gpencil_data)
    add_lineart_modifier(collection, gp_mat, gpencil_object)

    add_subdiv_modifier(f"{collection.name}_gp_subdiv", gpencil_object)
    add_multiple_strokes_modifier(f"{collection.name}_gp_mult", gpencil_object)
    add_simplify_modifier(f"{collection.name}_gp_simpl", gpencil_object)
    add_length_modifier(f"{collection.name}_gp_length", gpencil_object)

    if "frodo" not in collection.name:
        add_noise_modifier(f"{collection.name}_gp_noise", gpencil_object)

    bpy.data.collections.new(f"{collection.name}_grease")
    bpy.context.scene.collection.children.link(bpy.data.collections[f"{collection.name}_grease"])
    bpy.data.collections[f"{collection.name}_grease"].objects.link(gpencil_object)

    return gpencil_object


def add_material(collection, gpencil_data):
    gp_mat = bpy.data.materials.new(name=f"{collection.name}_gp_material")
    gpencil_data.materials.append(gp_mat)
    return gp_mat


def add_subdiv_modifier(name, gpencil_object):
    subdiv_mod = gpencil_object.grease_pencil_modifiers.new(
        name=name, type="GP_SUBDIV"
    )
    subdiv_mod.level = 2


def add_lineart_modifier(collection, gp_mat, gpencil_object):
    lineart_mod = gpencil_object.grease_pencil_modifiers.new(
        name=f"{collection.name}_gp_lineart", type='GP_LINEART'
    )
    lineart_mod.target_layer = f"{collection.name}_gp_layer"
    lineart_mod.target_material = gp_mat
    lineart_mod.use_crease = False
    lineart_mod.source_collection = collection
    lineart_mod.show_render = True
    lineart_mod.show_viewport = True
    lineart_mod.use_intersection_mask[0] = True
    lineart_mod.thickness = 12
    lineart_mod.use_fuzzy_intersections = True

    return lineart_mod


def add_noise_modifier(name, gpencil_object):
    noise_mod = gpencil_object.grease_pencil_modifiers.new(
        name=name, type="GP_NOISE"
    )
    noise_mod.factor = 0.05
    noise_mod.factor_strength = 0.03
    noise_mod.factor_thickness = 0.2
    noise_mod.use_random = True
    noise_mod.random_mode = "STEP"
    noise_mod.step = 74

    return noise_mod


def add_multiple_strokes_modifier(name, gpencil_object):
    multi_stroke_mod = gpencil_object.grease_pencil_modifiers.new(
        name=name, type="GP_MULTIPLY"
    )
    multi_stroke_mod.duplicates = 2
    multi_stroke_mod.distance = 0.0005
    multi_stroke_mod.offset = 0

    return


def add_simplify_modifier(name, gpencil_object):
    simplify_mod = gpencil_object.grease_pencil_modifiers.new(
        name=name, type="GP_SIMPLIFY"
    )
    simplify_mod.mode = "ADAPTIVE"
    simplify_mod.factor = 0.02
    return


def add_length_modifier(name, gpencil_object):
    length_mod = gpencil_object.grease_pencil_modifiers.new(
        name=name, type="GP_LENGTH"
    )
    length_mod.mode = 'RELATIVE'
    length_mod.start_factor = 0
    length_mod.end_factor = 0.01
    length_mod.overshoot_factor = 0
    length_mod.use_curvature = True
    length_mod.point_density = 30
    length_mod.segment_influence = 0
    length_mod.max_angle = 2.96706
    length_mod.random_start_factor = -0.04
    length_mod.random_end_factor = 0.04
    length_mod.random_offset = 0
    length_mod.seed = 0

    return
