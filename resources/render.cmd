@echo off
echo
echo               _         _
echo   __   ___.--'_`.     .'_`--.___   __
echo  ( _`.'. -   'o` )   ( 'o`   - .`.'_ )
echo  _\.'_'      _.-'     `-._      `_`./_
echo ( \`. )    //\`Frogging'/\\    ( .'/ )
echo  \_`-'`---'\\__, Hell ,__//`---'`-'_/
echo   \`        `-\Rendering/-'        '/
echo    `                               '      
echo
echo Preparing Blender Renderer...

set blend_file=%~2
set "blend_file=%blend_file:/=\%"

echo Copying original File "%blend_file%" to "%TEMP%/"

copy "%blend_file%" "%TEMP%\" /y  > nul
for /F "delims=" %%i in ("%blend_file%") do set filename=%TEMP%\%%~nxi

echo Copied File: %filename%
echo Running Command: "blender -E BLENDER_EEVEE %~1 %filename% %~3 %~4 %~5 %~6 %~7 %~8"

set PYTHONPATH=""

"%~dp0\blender" -E BLENDER_EEVEE %~1 %filename% %~3 %~4 %~5 %~6 %~7 %~8 > nul

echo "                         RENDERING FINISHED                                  "
echo "                             .-----.                                         "
echo "                           /7  .  (                                          "
echo "                            /   .-.  \                                       "
echo "                           /   /   \  \                                      "
echo "                          / `  )   (   )                                     "
echo "                         / `   |   |.  \                                     "
echo "                       .'  _.   \_/  . |                                     "
echo "      .--.           .' _.' |`.        |                                     "
echo "     (    `---...._.'   `---.'_)    ..  \                                    "
echo "      \            `----....___    `. \  |                                   "
echo "       `.           _ ----- _   `._  |/  |                                   "
echo "         `.       /"  \   /"  \`.  `._   |                                   "
echo "           `.    ((O)` ) ((O)` ) `.   `._\                                   "
echo "             `-- '`---'   `---' |  `.    `-.                                 "
echo "                /                  ` \      `-.                              "
echo "              .'                      `.       `.                            "
echo "             /                     `  ` `.       `-.                         "
echo "      .--.   \ ===._____.======. `    `   `. .___.--`     .''''.             "
echo "     ' .` `-. `.                |`. `   ` ` \          .' . '  8|            "
echo "    (8  .  ` `-.`.               ( .  ` `  .`\      .'  '    ' /             "
echo "     \  `. `    `-.               ) ` .   ` ` \  .'   ' .  '  /              "
echo "      \ ` `.  ` . \`.    .--.     |  ` ) `   .``/   '  // .  /               "
echo "       `.  ``. .   \ \   .-- `.  (  ` /_   ` . / ' .  '/   .'                "
echo "         `. ` \  `  \ \  '-.   `-'  .'  `-.  `   .  .'/  .'                  "
echo "           \ `.`.  ` \ \    ) /`._.`       `.  ` .  .'  /                    "
echo "            |  `.`. . \ \  (.'               `.   .'  .'                     "
echo "         __/  .. \ \ ` ) \                     \.' .. \__                    "
echo "  .-._.-'     '"  ) .-'   `.                   (  '"     `-._.--.            "
echo " (_________.-====' / .' /\_)`--..__________..-- `====-. _________|           "
echo " 
