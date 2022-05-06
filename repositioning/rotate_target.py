
import bpy

from math import radians
from sewar.full_ref import rmse
from numpy import asarray
from PIL import Image

from . manage_textures import bake_shadow, save_image
from . evaluate_shadow import compare_textures

global target
target = None

# This operator enable the user to chose an object as a target, then go back to select the object on which the target's shadow should be baked.
# It then gives an option to rotate the target object on the Z axis, accordingly to the shadow we expect to cast


def select_target_object():
    return (bpy.context.active_object)


def rotate_object(target):
    target.rotation_euler[2] += radians(10)
    return("Rotation of target")


class OBJECT_OT_rotate_target(bpy.types.Operator):
    bl_idname = "object.rotate_target"
    bl_label = "Add materials and textures to a mesh"
    bl_description = "This operator rotates a selected object in accordance with its expected casted shadow"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(items=[
        ('Select_target', 'Select object as target',
         'Set active object as target of positionning'),
        ('Rotate_object', 'Launch rotation', 'Launch target object rotation ')
    ], name="Target rotation")

    def execute(self, context):

        global target

        if self.action == 'Select_target':
            target = select_target_object()
        elif self.action == 'Rotate_object':
            if target != None:
                bpy.app.driver_namespace["shad_comparison"] = rotate_object(
                    target)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_rotate_target)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rotate_target)


if __name__ == "__main__":
    register()
