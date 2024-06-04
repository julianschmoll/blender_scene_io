import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

base_dir = "M:/frogging_hell_prism/02_Library/Assets"
"""MAKE DIRTY AND CLEAN SWITCH!!!!"""
frodo_path = "Character/chr-frodo/Export/Texturing/clean"
bed_path = "Props/prp-bed/Export/Texturing/Texturing_var_1"
matte_path = "Sets/set-room/Export/Texturing"



def get_version(input_path):
    version_folders = os.listdir(os.path.join(base_dir, input_path))
    versions = []
    for version_folder in version_folders:
        versions.append(int(version_folder.split("_")[0][-3:]))

    max_version = max(versions)
    max_version_string = f"v{str(max_version).zfill(3)}"
    max_version_folder = ""
    for version_folder in version_folders:
        if version_folder.startswith(max_version_string):
            max_version_folder = version_folder
    return os.path.join(input_path, max_version_folder)

matte_list = ["door_plane",
              "main_left_grp",
              "floor_plane_left",
              "window_plane",
              "main_right_grp",
              "floor_plane_right",
              "main_walls_grp",
              "left",
              "walls_but_thick_right",
              "walls_but_thick_right_seperate",
              "projection_geo",
              "walls_but_thick_left",
              "walls_but_thick_left_seperate",
              "prp_broken_wall_1_Modeling:pPlane1",
              "prp_broken_wall_left_Modeling:walls_thick_left_",
              "pPlaneBack",
              "pPlane1"
              ]

frodo_list = ["chr_frodo_Rigging:eye_l",
              "chr_frodo_Rigging:eye_r",
              "chr_frodo_Rigging:chr_frodo_Modeling:frog_martins",
              "chr_frodo_Rigging:chr_frodo_Modeling:frog_whole_pants",
              "chr_frodo_Rigging:chr_frodo_Modeling:grab_grab",
              "chr_frodo_Rigging:chr_frodo_Modeling:leggy_boy",
              "chr_frodo_Rigging:chr_frodo_Modeling:toxic_body_standards",
              "chr_frodo_Rigging:eye_l_upper_lid",
              "chr_frodo_Rigging:eye_l_lower_lid",
              "chr_frodo_Rigging:chr_optic_nerve_Modeling:opticnerve_r",
              "chr_frodo_Rigging:eye_r_upper_lid",
              "chr_frodo_Rigging:eye_r_lower_lid",
              "chr_frodo_Rigging:chr_optic_nerve_Modeling:optivnerve_l",
              "chr_frodo_Rigging:chr_teeth_Modeling:top_gums",
              "chr_frodo_Rigging:chr_teeth_Modeling:bottom_gums",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_14",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_13",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_12",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_11",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_21",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_22",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_23",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_24",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_31",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_32",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_33",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_34",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_41",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_42",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_43",
              "chr_frodo_Rigging:chr_teeth_Modeling:tooth_44"
              ]

bed_list = ["prp_bed_Rigging:prp_bed_Modeling:prp_mattress",
            "prp_bed_Rigging:prp_bed_Modeling:balls1",
            "prp_bed_Rigging:prp_bed_Modeling:balls2",
            "prp_bed_Rigging:prp_bed_Modeling:balls3",
            "prp_bed_Rigging:prp_bed_Modeling:balls4",
            "prp_bed_Rigging:prp_bed_Modeling:bedframe",
            "prp_bed_Rigging:blanket_geo",
            "prp_bed_Rigging:prp_pillow_Modeling:fat_pillow_"
]

texture_dict = {
        # walls
        "door_plane":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-door_plane.png"
        ),
        "floor_plane_right":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-floor_plane.png"
        ),
        "walls_but_thick_right_seperate":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-walls_but_thick_right_seperate.png"
        ),
        "walls_but_thick_right":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-walls_but_thick_right.png"
        ),
        "walls_but_thick_left":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-walls_but_thick_left.png"
        ),
        "walls_but_thick_left_seperate":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-walls_but_thick_left_seperate.png"
        ),
        "window_plane":os.path.join(
            base_dir,
            get_version(matte_path),
            "main_walls/projection_walls-window_plane.png"
        ),
    # broken walls
        "prp_broken_wall_1_Modeling:pPlane1":os.path.join(
            base_dir,
            get_version(matte_path),
            "broken_wall_v1/projection-wall-door_plane_broken.png"
        ),
        # frodo pants
        "chr_frodo_Rigging:chr_frodo_Modeling:frog_whole_pants":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_pants/chr-frodo_Modeling_v0051_frodo_pants_BaseColor_ACES - ACEScg.1001.png"
        ),
        # frodo gloves
        "chr_frodo_Rigging:chr_frodo_Modeling:grab_grab":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_shoes/chr-frodo_Modeling_v0051_frodo_shoes_and_gloves_BaseColor_ACES - ACEScg.1001.png"
        ),
        # frodo shoes
        "chr_frodo_Rigging:chr_frodo_Modeling:frog_martins":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_shoes/chr-frodo_Modeling_v0051_frodo_shoes_and_gloves_BaseColor_ACES - ACEScg.1001.png"
        ),
        # eye left
        "chr_frodo_Rigging:eye_l":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_eyes/chr-frodo_Modeling_v0051_frodo_eyes_BaseColor_ACES - ACEScg.1001.png"
        ),
        # eye right
        "chr_frodo_Rigging:eye_r":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_eyes/chr-frodo_Modeling_v0051_frodo_eyes_BaseColor_ACES - ACEScg.1001.png"
        ),
        # frodo legs
        "chr_frodo_Rigging:chr_frodo_Modeling:leggy_boy":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_skin/chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.1001.png"
        ),
        # frodo torso
        "chr_frodo_Rigging:chr_frodo_Modeling:toxic_body_standards":os.path.join(
            base_dir,
            get_version(frodo_path),
            "frodo_skin/chr-frodo_Modeling_v0051_frodo_skin_BaseColor_ACES - ACEScg.1001.png"
        ),
        # cowboy hat
        "Object":os.path.join(
            base_dir,
            get_version("Props/prp-cowboy-hat/Export/Texturing"),
            "prp-cowboy-hat_Modeling_v0008_DefaultMaterial_BaseColor_ACES - ACEScg.1001"
        ),
        # eye lid left
        "chr_frodo_Rigging:eye_l_lower_lid":os.path.join(
            "M:/frogging_hell_prism/06_Artist/DAS_ROB/chr-frodo_skin_BaseColor_ACES - ACEScg.1001.png"),
        "chr_frodo_Rigging:eye_l_upper_lid": os.path.join(
            "M:/frogging_hell_prism/06_Artist/DAS_ROB/chr-frodo_skin_BaseColor_ACES - ACEScg.1001.png"),
        # eye lid right
        "chr_frodo_Rigging:eye_r_lower_lid":os.path.join(
            "M:/frogging_hell_prism/06_Artist/DAS_ROB/chr-frodo_skin_BaseColor_ACES - ACEScg.1001.png"),
        "chr_frodo_Rigging:eye_r_upper_lid":os.path.join(
            "M:/frogging_hell_prism/06_Artist/DAS_ROB/chr-frodo_skin_BaseColor_ACES - ACEScg.1001.png"),
        # bed frame
        "prp_bed_Rigging:prp_bed_Modeling:bedframe":os.path.join(
            base_dir,
            get_version(bed_path),
            "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1001.png"
        ),
        # bed pillow
        "prp_pillow_Modeling:fat_pillow_mod":os.path.join(
                base_dir,
                "Props/prp-pillow/Export/Texturing/v001/prp-pillow_Modeling_v0003_DefaultMaterial_BaseColor_ACES - ACEScg.1001.png"
        ),
        # bed matress
        "prp_bed_Rigging:prp_bed_Modeling:prp_mattress":os.path.join(
                base_dir,
                get_version(bed_path),
                "bed_matress/prp-bed_Modeling_v0020_matress_mat_BaseColor_ACES - ACEScg.1001.png"
        ),
        # bed balls
        "prp_bed_Rigging:prp_bed_Modeling:balls1":os.path.join(
                base_dir,
                get_version(bed_path),
                "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1002.png"),
        "prp_bed_Rigging:prp_bed_Modeling:balls2":os.path.join(
                base_dir,
                get_version(bed_path),
                "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1002.png"),
        "prp_bed_Rigging:prp_bed_Modeling:balls3":os.path.join(
                base_dir,
                get_version(bed_path),
                "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1002.png"),
        "prp_bed_Rigging:prp_bed_Modeling:balls4":os.path.join(
                base_dir,
                get_version(bed_path),
                "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1002.png"),
        # gertie
        "gertie1":os.path.join(
                "M:/frogging_hell_prism/06_Artist/random/2DAssets/02_export/gertie.png"),
        # standing frame
        "prp_standing_frame_h_Rigging:prp_standing_frame":os.path.join(
               base_dir,
                "Props/prp-standing-frame/Export/Texturing/prp_standing_frame_Modeling_frame.png"),
        # standing frame horizontal
        "prp_standing_frame_Rigging:prp_standing_frame_M":os.path.join(
                base_dir,
                "Props/prp-standing-frame/Export/Texturing/prp_standing_frame_Modeling_frame.png"),
        # ----------------------------------------------------------------  drawer
        # drawer body
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_body":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/body_mat/prp-drawer_Modeling_v0010_prp_body_mat_BaseColor_ACES - ACEScg.1001.png"),
        # drawer drawer
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_fron":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/drawer_mat/prp-drawer_Modeling_v0010_prp_drawer_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_.002":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/drawer_mat/prp-drawer_Modeling_v0010_prp_drawer_mat_BaseColor_ACES - ACEScg.1001.png"),
        # rings
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_ring":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_ball":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:poly.004":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:poly.001":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:poly.003":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:polySurf":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:poly.002":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:poly":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/ring_mat/prp-drawer_Modeling_v0010_prp_ring_mat_BaseColor_ACES - ACEScg.1001.png"),
        # legs
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_leg3":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/leg_mat/prp-drawer_Modeling_v0010_prp_leg_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_leg2":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/leg_mat/prp-drawer_Modeling_v0010_prp_leg_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_leg1":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/leg_mat/prp-drawer_Modeling_v0010_prp_leg_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_Rigging:prp_drawer_Modeling:prp_leg":os.path.join(
                base_dir,
                "Props/prp-drawer/Export/Texturing/v001/leg_mat/prp-drawer_Modeling_v0010_prp_leg_mat_BaseColor_ACES - ACEScg.1001.png"),
        # ------------------------------------------------------------------ urne
        "prp_urn_flip_Modeling:urn":os.path.join(
                base_dir,
                "Props/prp-urn-flip/Export/Texturing/v001/prp-urn-flip_Modeling_v0003_DefaultMaterial_BaseColor_ACES - ACEScg.1001.png"),
        "prp_urn_flip_Modeling:urntop":os.path.join(
                base_dir,
                "Props/prp-urn-flip/Export/Texturing/v001/prp-urn-flip_Modeling_v0003_DefaultMaterial_BaseColor_ACES - ACEScg.1001.png"),
        # ------------------------------------------------------------------ small paint buckets
        "prp_paint_bucket_small_Rigging1:prp_paint_b":os.path.join(
                base_dir,
                "Props/prp-paint-bucket-small/Export/Texturing/v001/bucket_mat/prp-paint-bucket-small_Modeling_v0004_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_small_Rigging1:prp_paint_bucke":os.path.join(
                base_dir,
                "Props/prp-paint-bucket-small/Export/Texturing/v001/handle_mat/prp-paint-bucket-small_Modeling_v0004_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_small_Rigging:prp_paint_bu": os.path.join(
                base_dir,
                "Props/prp-paint-bucket-small/Export/Texturing/v001/bucket_mat/prp-paint-bucket-small_Modeling_v0004_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_small_Rigging:prp_paint_bucket": os.path.join(
                base_dir,
                "Props/prp-paint-bucket-small/Export/Texturing/v001/handle_mat/prp-paint-bucket-small_Modeling_v0004_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        # palette
        "prp_palette_Rigging1:prp_palette_Modeling:palet":os.path.join(
                base_dir,
                "Props/prp-palette/Export/Texturing/v001/prp-palette_Modeling_v0005_palette_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_palette_Rigging:prp_palette_Modeling:palett": os.path.join(
                base_dir,
                "Props/prp-palette/Export/Texturing/v001/prp-palette_Modeling_v0005_palette_mat_BaseColor_ACES - ACEScg.1001.png"),
        # ------------------------------------------------------------------ paint bucket
        "prp_paint_bucket_Rigging2:prp_paint_bucket_Mode": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/bucket_mat/prp-paint-bucket_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_Rigging2:prp_paint_bucket_": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/handle_mat/prp-paint-bucket_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_Rigging:prp_paint_bucket_Model": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/bucket_mat/prp-paint-bucket_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_Rigging:prp_paint_bucket_M": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/handle_mat/prp-paint-bucket_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_Rigging1rp_paint_bucket_Mode": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/bucket_mat/prp-paint-bucket_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket_Rigging1:prp_paint_bucket_": os.path.join(
                base_dir,
                "Props/prp-paint-bucket/Export/Texturing/v001/handle_mat/prp-paint-bucket_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),

        # ------------------------------------------------------------------- paint bucket 2
        "prp_paint_bucket2_Rigging:prp_paint_bucket2_Mod": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/bucket_mat/prp-paint-bucket2_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging:prp_paint_bucket2": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/handle_mat/prp-paint-bucket2_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging1:prp_paint_bucket2_Mo": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/bucket_mat/prp-paint-bucket2_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging1:prp_paint_bucket": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/handle_mat/prp-paint-bucket2_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging2:prp_paint_bucket2_Mo": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/bucket_mat/prp-paint-bucket2_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging2:prp_paint_bucket": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/handle_mat/prp-paint-bucket2_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging3:prp_paint_bucket2_Mo": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/bucket_mat/prp-paint-bucket2_Modeling_v0006_bucket_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_paint_bucket2_Rigging3:prp_paint_bucket": os.path.join(
                base_dir,
                "Props/prp-paint-bucket2/Export/Texturing/v001/handle_mat/prp-paint-bucket2_Modeling_v0006_handle_mat_BaseColor_ACES - ACEScg.1001.png"),


        # ------------------------------------------------------------------- wickie helmet
        "prp_wickie_helmet_Rigging:prp_wickie_helmet.002":os.path.join(
                base_dir,
                "Props/prp-wickie-helmet/Export/Texturing/v001/helmet_mat/prp-wickie-helmet_Modeling_v0004_helmet_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_wickie_helmet_Rigging:prp_wickie_helmet.001":os.path.join(
                base_dir,
                "Props/prp-wickie-helmet/Export/Texturing/v001/bubble_mat/prp-wickie-helmet_Modeling_v0004_bubble_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_wickie_helmet_Rigging:prp_wickie_helmet_Mod":os.path.join(
                base_dir,
                "Props/prp-wickie-helmet/Export/Texturing/v001/bubble_mat/prp-wickie-helmet_Modeling_v0004_bubble_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_wickie_helmet_Rigging:prp_wickie_helmet":os.path.join(
                base_dir,
                "Props/prp-wickie-helmet/Export/Texturing/v001/bubble_mat/prp-wickie-helmet_Modeling_v0004_bubble_mat_BaseColor_ACES - ACEScg.1001.png"),
        # tintoy
        "tintoy1":os.path.join(
                "M:/frogging_hell_prism/06_Artist/random/2DAssets/02_export/TinToy.png"),
        # canvas 1
        #"prp_canvas_01_Rigging:prp_canvas_01_Modelin.002":os.path.join(
        #        base_dir,
        #        "Props/prp-canvas-01/Export"),
        # canvas 2
        "prp_canvas_02_Rigging:prp_canvas_02_Modelin.004":os.path.join(
                base_dir,
                "Props/prp-canvas-02/Export/Texturing/v001/projection1-canvas.png"),
        # canvas 3
        "prp_canvas_03_Rigging:prp_canvas_03_Modeling_v0":os.path.join(
                base_dir,
                "Props/prp-canvas-03/Export/Texturing/v001/projection1-prp_canvas.png"),
        # canvas 4
        #"prp_canvas_04_Rigging:prp_canvas_04_Modeling:ca":os.path.join(
        #        base_dir,
        #        "Props/prp-canvas-04/Export/"
        #),
        # broom
        "prp_broom_big_Rigging:prp_broom_big_Modeling:pC":os.path.join(
                base_dir,
                "Props/prp-broom-big/Export/Texturing/v001/prp-broom-big_Modeling_v0004_DefaultMaterial_BaseColor_ACES - ACEScg.1001.png"),
        # drawer small drawer
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.002":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/drawer_mat/prp-drawer-smol_Modeling_v0020_drawer_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/drawer_mat/prp-drawer-smol_Modeling_v0020_drawer_mat_BaseColor_ACES - ACEScg.1001.png"),
        # drawer small body
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.005":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/body_mat/prp-drawer-smol_Modeling_v0020_body_mat_BaseColor_ACES - ACEScg.1001.png"),
        # drawer knobs
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.007":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/knob_mat/prp-drawer-smol_Modeling_v0020_knob_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.008":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/knob_mat/prp-drawer-smol_Modeling_v0020_knob_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.009":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/knob_mat/prp-drawer-smol_Modeling_v0020_knob_mat_BaseColor_ACES - ACEScg.1001.png"),
        "prp_drawer_smol_Rigging:prp_drawer_smol_Mod.010":os.path.join(
                base_dir,
                "Props/prp-drawer-smol/Export/Texturing/v001/knob_mat/prp-drawer-smol_Modeling_v0020_knob_mat_BaseColor_ACES - ACEScg.1001.png"),
        # spatula
        "prp_spongebob_spatula_Rigging:prp_spongebob_spa":os.path.join(
                base_dir,
                "Props/prp-spongebob-spatula/Export/Texturing/v001/prp-spongebob-spatula_Modeling_v0004_DefaultMaterial_BaseColor_ACES - ACEScg.1001.png")
        # ------------------------------------------------------- bucket
}

