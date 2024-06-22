import os
import logging
import subprocess
from blender_scene_io import scene_utils
from blender_scene_io import ui
from string import Template
import bpy

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Render Submission")


def submit_render(dry_run=False):
    scene_path = scene_utils.get_scene_file_path()
    nice_name = assemble_render_set_name(scene_path)
    project_name, shot, version, user = nice_name.split("_")
    ffmpeg_cmd = "deprecated"
    ffmpeg_rset = assemble_ffmpeg_rset(scene_path, shot, version)

    render_set = create_render_set(
        scene_path, ffmpeg_cmd, shot.split("-")[0], shot.split("-")[-1], version
    )

    cmd = assemble_render_cmd(
        nice_name,
        create_import_set(scene_path),
        scene_path,
        render_set
    )

    LOGGER.info(f"Submitting to Renderpal with: \n{cmd}")

    if dry_run:
        return

    scene_utils.save_scenefile()
    run_wake_up_bats()
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    streamdata = child.communicate()[0]
    rc = child.returncode

    print(f"Return Code: {rc}")

    ffmpeg_cmd = assemble_ffmpeg_cmd(f"CONVERT_{nice_name}", ffmpeg_rset, rc)
    print(ffmpeg_cmd)
    subprocess.Popen(ffmpeg_cmd)

    ui.ShowMessageBox(
        message=f"Succesfully submitted {nice_name} to Renderpal. Job ID: {rc}",
        title="Renderpal Submission"
    )

def assemble_render_set_name(scene_path):
    path_elem = scene_path.split(os.sep)
    naming_elem = path_elem[-1].split("_")
    nice_name = "_".join(
        ["Frogging-Hell", path_elem[4], naming_elem[-3], naming_elem[-2]]
    )
    return nice_name


def assemble_render_cmd(render_name, import_set, scene_path, nj_preset, chunk_size=15):
    return " ".join(
        [
            f'"{get_renderpal_exe()}"',
            '-login="ca-user:polytopixel"',
            f'-nj_preset="{nj_preset}"',
            '-nj_renderer="Blender/Frog Render"',
            f'-nj_splitmode="2,{chunk_size}"',
            "-retnjid ",
            f'-nj_name="{render_name}"',
            '-nj_project="Frogging Hell"',
            f'-importset="{import_set}"',
            f'"{scene_path}"',
        ]
    )


def assemble_ffmpeg_cmd(render_name, import_set, dep_id):
    return " ".join(
        [
            f'"{get_renderpal_exe()}"',
            '-login="ca-user:polytopixel"',
            '-nj_renderer="Frog FFmpeg/Default version"',
            "-retnjid",
            f"-nj_dependency {dep_id}",
            "-nj_deptype 0",
            f'-nj_name="{render_name}"',
            '-nj_project="Frogging Hell"',
            f'-importset="{import_set}"',
            "FFMPEG"
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


def create_render_set(scene_path, ffmpeg_cmd, sequence_name, shot_name, version):
    parent_path = os.path.dirname(scene_path)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(root_dir, "resources", "post_render_event_preset.txt")

    d = {
        "FFMPEG_CMD": ffmpeg_cmd,
        "SHOT_NAME":shot_name,
        "VERSION":version,
        "SEQUENCE_NAME":sequence_name
    }

    with open(file, "r") as f:
        src = Template(f.read())
        result = src.substitute(d)

    r_set_file = os.path.join(parent_path, "render_set.rnjprs")

    with open(r_set_file, "w") as r_set:
        r_set.write(result)

    return r_set_file


def run_wake_up_bats():
    LOGGER.info("Waking up computers :)")
    subprocess.Popen(
        "K:/wake_042.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    subprocess.Popen(
        "K:/wake_043.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def assemble_ffmpeg_rset(scene_path, shot, version):
    scn = bpy.context.scene
    search_path = scn.node_tree.nodes["File Output"].base_path.replace("####", "%04d").replace(os.sep, "/")
    path_elem = search_path.split("/")
    playblast_path = os.path.join(
        "M:/",
        *path_elem[1:5],
        "Playblasts",
        "Animation"
    )
    v_f = path_elem[-3]
    for version_folder in os.listdir(playblast_path):
        if version_folder.startswith(path_elem[-3]):
            v_f = version_folder

    os.makedirs(v_f, exist_ok=True)

    parent_path = os.path.dirname(scene_path)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(root_dir, "resources", "ffmpeg_rset_template.txt")

    d = {
        "input": search_path,
        "out_dir":os.path.join(playblast_path, v_f).replace(os.sep, "/"),
        "out_file": f"Shot_{shot}_{version}_qc_render.mp4",
        "start_frame":int(scn.frame_start)
    }

    with open(file, "r") as f:
        src = Template(f.read())
        result = src.substitute(d)

    r_set_file = os.path.join(parent_path, f"ffmpeg_render_set_{version}.rnjprs")

    with open(r_set_file, "w") as r_set:
        r_set.write(result)

    return r_set_file


def get_renderpal_exe():
    return r"C:\Program Files (x86)\RenderPal V2\CmdRC\RpRcCmd.exe"


def get_ffmpeg_exe():
    return r"M:\frogging_hell_prism\00_Pipeline\Packages\FFmpeg\bin\ffmpeg.exe"
