import os

base_dir = "M:/frogging_hell_prism/02_Library/Assets"
"""MAKE DIRTY AND CLEAN SWITCH!!!!"""
frodo_path = "Character/chr-frodo/Export/Texturing/clean"
bed_path = "Props/prp-bed/Export/Texturing/Texturing_var_1"
matte_path = "Sets/set-room/Export/Texturing/v002/main_walls"


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

matte_list = ["set_room_Layout:door_plane",
              "set_room_Layout:main_left_grp",
              "set_room_Layout:floor_plane_left",
              "set_room_Layout:window_plane",
              "set_room_Layout:main_right_grp",
              "set_room_Layout:floor_plane_right",
              "set_room_Layout:main_walls_grp",
              "set_room_Layout:left",
              "set_room_Layout:walls_but_thick_right",
              "set_room_Layout:walls_but_thick_right_seperate",
              "set_room_Layout:projection_geo",
              "set_room_Layout:walls_but_thick_left",
              "set_room_Layout:walls_but_thick_left_seperate"
              ]

matte_dict = {
    "set_room_Layout:door_plane":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-door_plane.png"
    ),
    "set_room_Layout:floor_plane_right":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-floor_plane.png"
    ),
    "set_room_Layout:walls_but_thick_right_seperate"
    "":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-walls_but_thick_right_seperate.png"
    ),
    "set_room_Layout:walls_but_thick_right":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-walls_but_thick_right.png"
    ),
    "set_room_Layout:walls_but_thick_left":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-walls_but_thick_left.png"
    ),
    "set_room_Layout:walls_but_thick_left_seperate":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-walls_but_thick_left_seperate.png"
    ),
    "set_room_Layout:window_plane":os.path.join(
        base_dir,
        matte_path,
        "projection_walls-window_plane.png"
    )
}

texture_dict = {
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
    # bed frame
    "set_room_Layout:prp_bed_Rigging:prp_bed_Modeling:bedframe":os.path.join(
        base_dir,
        get_version(bed_path),
        "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1001.png"
    ),
    # bed pillow
    "set_room_Layout:prp_pillow_Modeling:fat_pillow_mod":os.path.join(
       "M:/frogging_hell_prism/02_Library/Assets/Props/prp - pillow/Export/Texturing/v001"
    ),
    # bed matress
    "set_room_Layout:prp_bed_Rigging:prp_bed_Modeling:prp_mattress":os.path.join(
        base_dir,
        get_version(bed_path),
        "bed_matress/prp-bed_Modeling_v0020_matress_mat_BaseColor_ACES - ACEScg.1001.png"
    ),
}

for geo, texture in texture_dict.items():
    print(f"\nGeometry: {geo}\nTexture:  {texture}")
