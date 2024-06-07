import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("blender_scene_io")

base_dir = "M:/frogging_hell_prism/02_Library/Assets"


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
