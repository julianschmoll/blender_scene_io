import os
import logging
import subprocess
from blender_scene_io import scene_utils
from blender_scene_io import ui

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Render Submission")


def submit_render(dry_run=False):
    scene_path = scene_utils.get_scene_file_path()
    nice_name = assemble_render_set_name(scene_path)
    cmd = assemble_cmd(
        nice_name,
        create_import_set(scene_path),
        scene_path
    )

    LOGGER.info(f"Submitting to Renderpal with: \n{cmd}")

    if dry_run:
        return

    scene_utils.save_scenefile()
    run_wake_up_bats()
    subprocess.Popen(cmd)

    ui.ShowMessageBox(
        message=f"Succesfully submitted {nice_name} to Renderpal.",
        title="Renderpal Submission"
    )

def assemble_render_set_name(scene_path):
    path_elem = scene_path.split(os.sep)
    naming_elem = path_elem[-1].split("_")
    nice_name = "_".join(
        ["Frogging-Hell", path_elem[4], naming_elem[-3], naming_elem[-2]]
    )
    return nice_name


def assemble_cmd(render_name, import_set, scene_path, chunk_size=15):
    return " ".join(
        [
            f'"{get_renderpal_exe()}"',
            '-login="ca-user:polytopixel" '
            '-nj_renderer="Blender/Frog Render"',
            f'-nj_splitmode="2,{chunk_size}"',
            f'-nj_name="{render_name}"',
            '-nj_project="Frogging Hell"',
            f'-importset="{import_set}"',
            f'"{scene_path}"'
        ]
    )


def create_import_set(scene_path):
    parent_path = os.path.dirname(scene_path)
    content = """
    <RenderSet>
        <Values>
            <frames>
                <Value>{0}-{1}</Value>
            </frames>
        </Values>
    </RenderSet>
    """.format(*scene_utils.get_frame_ramge())
    r_set_file = os.path.join(parent_path, "renderpal.rset")

    with open(r_set_file, "w") as r_set:
        r_set.write(content)

    return r_set_file


def run_wake_up_bats():
    LOGGER.info("Waking up computers :)")
    subprocess.Popen(
        "K:/wake_042.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    subprocess.Popen(
        "K:/wake_043.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def get_renderpal_exe():
    return "C:\Program Files (x86)\RenderPal V2\CmdRC\RpRcCmd.exe"
