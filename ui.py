import bpy
import logging

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    if bpy.app.background:
        logger = logging.getLogger(title)
        logger.info(message)
        return
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
