import os

base_dir = "M:/frogging_hell_prism/02_Library/Assets"
frodo_path = "Character/chr-frodo/Export/Texturing"
bed_path = "Props/prp-bed/Export/Texturing/Texturing_var_1"


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
    # bed balls
    
    # bed balls
    "set_room_Layout:prp_bed_Rigging:prp_bed_Modeling:balls4":
        [
            # first udim
            os.path.join(
            base_dir,
            get_version(bed_path),
            "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1001.png"),
            # second udim
            os.path.join(
            base_dir,
            get_version(bed_path),
            "bed_frame/prp-bed_Modeling_v0020_bed_frame_mat_BaseColor_ACES - ACEScg.1002.png")
        ],
    # bef matress
    "set_room_Layout:prp_bed_Rigging:prp_bed_Modeling:prp_mattress":os.path.join(
        base_dir,
        get_version(bed_path),
        "bed_matress/prp-bed_Modeling_v0020_matress_mat_BaseColor_ACES - ACEScg.1001.png"
    ),
}

for geo, texture in texture_dict.items():
    print(f"\nGeometry: {geo}\nTexture:  {texture}")
