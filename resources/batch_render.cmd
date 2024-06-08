set PYTHONPATH=

set SHOT_NAME=%1
echo %SHOT_NAME%
call "M:\frogging_hell_prism\00_Pipeline\Programs\blender\blender_4_1_1\blender.exe" --background --python-expr "import sys;sys.path.append(r'M:\frogging_hell_prism\00_Pipeline\Packages');from blender_scene_io import startup;startup.run_startup_scripts();startup.assemble_and_submit_shot('%SHOT_NAME%')"