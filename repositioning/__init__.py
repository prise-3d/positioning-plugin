
import bpy

from . import add_plane, main_panel, manage_textures, evaluate_shadow, rotate_target

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
