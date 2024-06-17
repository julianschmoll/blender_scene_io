import bpy
import logging
import os


LOGGER = logging.getLogger("Grease Utils")


def apply_grease_pencil(collection):
    pixel_size = 300.0
    if "bed" in collection.name:
        pixel_size=1000
    gp_mat = add_material(
        collection,
        load_image(r"M:\frogging_hell_prism\06_Artist\juschli\brushes\frodo_outline_v7.png"),
        pixel_size=pixel_size
    )
    gpencil_data = bpy.data.grease_pencils.new(name=collection.name)
    gpencil_object = bpy.data.objects.new(
        name=f"{collection.name}_gp", object_data=gpencil_data
    )
    gp_layer = gpencil_data.layers.new(
        name=f"{collection.name}_gp_layer", set_active=True
    )
    gp_layer.frames.new(0)
    gpencil_data.materials.append(gp_mat)

    thickness=10

    if "frodo" in collection.name:
        thickness = 16

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_lineart",
        "GP_LINEART",
        target_layer=f"{collection.name}_gp_layer",
        target_material=gp_mat,
        use_crease=False,
        source_collection=collection,
        show_render=True,
        show_viewport=True,
        use_intersection_mask=[True, False, False, False, False, False, False, False],
        thickness=thickness,
        use_fuzzy_intersections=True,
        use_geometry_space_chain = True,
        chaining_image_threshold = 0.2,
        smooth_tolerance = 0.1,
    )

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_mult",
        "GP_MULTIPLY",
        duplicates = 2,
        distance = 0.00025,
        offset = 0
    )

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_simpl",
        "GP_SIMPLIFY",
        mode = "ADAPTIVE",
        factor = 0.01,
    )

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_length",
        "GP_LENGTH",
        mode = 'RELATIVE',
        start_factor = 0,
        end_factor = 0.01,
        overshoot_factor = 0,
        use_curvature = True,
        point_density = 30,
        segment_influence = 0,
        max_angle = 2.96706,
        random_start_factor = -0.04,
        random_end_factor = 0.04,
        random_offset = 0,
        seed = 0,
    )

    if "frodo" not in collection.name:
        add_gp_modifier(
            gpencil_object,
            f"{collection.name}_gp_noise",
            "GP_NOISE",
            factor = 0.05,
            factor_strength = 0.03,
            factor_thickness = 0.2,
            use_random = True,
            random_mode = "STEP",
            step = 74,
        )

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_subdiv",
        "GP_SUBDIV",
        level=2
    )

    add_gp_modifier(
        gpencil_object,
        f"{collection.name}_gp_pencil_noise",
        "GP_NOISE",
        factor = 0,
        factor_strength = 0.2,
        factor_thickness = 0.253521,
        factor_uvs = 0,
        noise_scale = 1,
        noise_offset = 0,
        seed = 1,
        use_random = True,
    )

    bpy.data.collections.new(f"{collection.name}_grease")
    bpy.context.scene.collection.children.link(bpy.data.collections[f"{collection.name}_grease"])
    bpy.data.collections[f"{collection.name}_grease"].objects.link(gpencil_object)

    return gpencil_object


def load_image(path):
    img_name = os.path.basename(path)
    if bpy.data.images.get(img_name):
        return bpy.data.images.get(img_name)
    return bpy.data.images.load(path)


def add_material(collection, image=None, pixel_size=300.0):
    mat_name =f"{collection.name}_gp_material"
    if mat_name in bpy.data.materials.keys():
        gp_mat = bpy.data.materials[mat_name]
    else:
        gp_mat = bpy.data.materials.new(mat_name)

    if not gp_mat.is_grease_pencil:
        bpy.data.materials.create_gpencil_data(gp_mat)

    material = gp_mat.grease_pencil
    material.color = (0.0240566, 0.0240566, 0.0240566, 1)

    if image:
        material.stroke_style = "TEXTURE"
        material.pixel_size = pixel_size
        material.use_overlap_strokes = True
        material.stroke_image = image
        material.mix_stroke_factor = 1

    return gp_mat


def add_gp_modifier(gpencil_object, name, type, **kwargs):
    modifier = gpencil_object.grease_pencil_modifiers.new(
        name=name, type=type
    )
    for setting, value in kwargs.items():
        setattr(modifier, setting, value)

    return modifier
