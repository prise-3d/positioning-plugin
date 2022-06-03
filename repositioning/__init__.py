
import bpy
import subprocess
import os
import sys
from pathlib import Path
import importlib


# Pillow, that we need to convert images into arrays, will be installed into Blender's folder dedicated to modules if it is not already accessible
# This installation requires to run Blender as administrator the first time the module is imported and activated

if not importlib.util.find_spec("PIL"):
    py_exec = str(sys.executable)
    dir = os.path.dirname(Path(importlib.util.find_spec("bpy").origin).parent)

    subprocess.check_call(
        [py_exec, '-m', 'pip', 'install', 'Pillow', '--target', dir])

else:
    print("Pillow already installed : ", importlib.util.find_spec("PIL").origin)

from . import add_plane, main_panel, manage_textures, evaluate_shadow, rotate_target

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "Set a repositioning environment",
    "author": "Florence Constans",
    "version": (0, 0, 6),
    "blender": (2, 80, 0),
    "location": "View3D > Side Bar",
    "description": "Adds a plane to bake on, or add material and textures on already existing objects to bake shadows on ",
    "warning": "",
    "doc_url": "",
    "category": "All",
}
# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------


def register():

    main_panel.register()
    add_plane.register()
    manage_textures.register()
    evaluate_shadow.register()
    rotate_target.register()


def unregister():
    main_panel.unregister()
    add_plane.unregister()
    manage_textures.unregister()
    evaluate_shadow.unregister()
    rotate_target.unregister()


if __name__ == "__main__":
    register()
