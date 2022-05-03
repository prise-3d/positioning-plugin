from . import add_plane, main_panel, manage_textures, evaluate_shadow
import bpy

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
# We will be using RMSE coming from the Sewar package, to evaluate the obtained renders
# Because the version of python that bpy use is "isolated" in Blender, we have to make sure the package is installed inside of Blender:

import subprocess
import sys
import os
from pathlib import Path

py_exec = str(sys.executable)
# Get lib directory
lib = os.path.join(Path(py_exec).parent.parent, "lib")
# Ensure pip is installed
subprocess.call([py_exec, "-m", "ensurepip", "--user"])
# Update pip (not mandatory)
subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip"])
# Install packages
subprocess.call([py_exec, "-m", "pip", "install",
                f"--target={str(lib)}", "sewar"])

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
bl_info = {
    "name": "Set a shadow baking environment",
    "author": "Florence Constans",
    "version": (0, 0, 3),
    "blender": (2, 80, 0),
    "location": "View3D > Side Bar",
    "description": "Adds a plane to bake on, or add material and textures on already existing objects to bake shadows on ",
    "warning": "",
    "doc_url": "",
    "category": "All",
}


def register():
    main_panel.register()
    add_plane.register()
    manage_textures.register()
    evaluate_shadow.register()


def unregister():
    main_panel.unregister()
    add_plane.unregister()
    manage_textures.unregister()
    evaluate_shadow.unregister()


if __name__ == "__main__":
    register()
