from . import manage_plane, panel_manage_plane
import bpy

bl_info = {
    "name": "Set a shadow baking environment",
    "author": "Florence Constans",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Side Bar",
    "description": "Adds a plane on which surrounding objects' shadows are baked and compared to a reference",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def register():
    panel_manage_plane.register()
    manage_plane.register()


def unregister():
    panel_manage_plane.unregister()
    manage_plane.unregister()


if __name__ == "__main__":
    register()
