import bpy
import os
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Render Submission")


def submit_render():
    scene_path = get_scene_file_path()
    path_elem = scene_path.split(os.sep)
    naming_elem = path_elem[-1].split("_")
    nice_name = "_".join(
        ["Frogging-Hell", path_elem[4], naming_elem[-3], naming_elem[-2]]
    )
    parent_path = os.path.dirname(scene_path)
    cmd = assemble_cmd(
        nice_name,
        create_import_set(parent_path),
        scene_path
    )
    LOGGER.info(f"Submitting to Renderpal with: \n{cmd}")
    run_wake_up_bats()
    subprocess.Popen(cmd)


def assemble_cmd(render_name, import_set, scene_path, chunk_size=10):
    return " ".join(
        [
            f'"{get_renderpal_exe()}"',
            '-nj_renderer="Blender/Frog Render"',
            f'-nj_splitmode="2,{chunk_size}"',
            f'-nj_name="{render_name}"',
            '-nj_project="Frogging Hell"',
            f'-importset="{import_set}"',
            f'"{scene_path}"'
        ]
    )


def create_import_set(parent_path):
    content = """
    <RenderSet>
        <Values>
            <frames>
                <Value>{0}-{1}</Value>
            </frames>
        </Values>
    </RenderSet>
    """.format(*get_frame_ramge())
    r_set_file = os.path.join(parent_path, "renderpal.rset")
    with open(r_set_file, "w") as r_set:
        r_set.write(content)
    return r_set_file


def get_scene_file_path():
    return bpy.data.filepath


def get_frame_ramge():
    scn = bpy.context.scene
    return scn.frame_start, scn.frame_end


def run_wake_up_bats():
    LOGGER.info("Waking up computers :)")
    subprocess.Popen("K:/wake_042.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.Popen("K:/wake_043.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def get_renderpal_exe():
    return "C:\Program Files (x86)\RenderPal V2\CmdRC\RpRcCmd.exe"
