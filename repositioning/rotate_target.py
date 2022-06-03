
import bpy

from math import radians

from . manage_textures import bake_shadow
from . evaluate_shadow import compare_textures, retrieve_reference, rmse, select_target_object

global target
target = None

# This operator enable the user to chose an object as a target, then go back to select the object on which the target's shadow should be baked.
# It then gives an option to rotate the target object on the Z axis, accordingly to the shadow we expect to cast


# This version uses compare_textures(), which means everytime we evaluate, the reference is saved and opened again, even though it doesn't change.


def rotate_object(target, degree=1, count=0, res=64):
    if abs(degree) > 0.02:
        initial_diff = compare_textures(res)
        degree_1 = degree/2
        degree_2 = -degree_1
        target.rotation_euler[2] += radians(degree_1)
        diff_1 = compare_textures(res)

        target.rotation_euler[2] -= radians(degree_1)

        target.rotation_euler[2] += radians(degree_2)
        diff_2 = compare_textures(res)

        target.rotation_euler[2] -= radians(degree_2)

        if res < 1024:
            next_res = res*2
        else:
            next_res = res

        if initial_diff < diff_1 and initial_diff < diff_2:

            if diff_1 < diff_2:
                return(rotate_object(target, degree_1, count+3, next_res))
            else:
                return(rotate_object(target, degree_2, count+3, next_res))

        elif diff_1 <= diff_2:
            target.rotation_euler[2] += radians(degree_1)
            return(rotate_object(target, degree_1, count+3, next_res))
        else:
            target.rotation_euler[2] += radians(degree_2)
            return(rotate_object(target, degree_2, count+3, next_res))
    else:
        bpy.app.driver_namespace["iterations"] = str(count)
        return(str(compare_textures(res)))


def full_rotation(target):
    scores = []
    min = 255
    min_position = target.rotation_euler[2]

    for degree in range(360):
        target.rotation_euler[2] = radians(degree)
        scores.append(compare_textures(32))

    for position in range(len(scores)):
        if scores[position] <= min:
            min = scores[position]
            min_position = position

    target.rotation_euler[2] = radians(min_position)
    bpy.app.driver_namespace["iterations"] = "360"
    return(str(compare_textures(32)))


class OBJECT_OT_rotate_target(bpy.types.Operator):
    bl_idname = "object.rotate_target"
    bl_label = "Add materials and textures to a mesh"
    bl_description = "This operator rotates a selected object in accordance with its expected casted shadow"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(items=[
        ('Select_target', 'Select object as target',
         'Set active object as target of positionning'),
        ('Rotate_object', 'Target rotation', 'Launch target object rotation '),
        ('Fast_Rotate_object', 'Fast Target rotation',
         'Launch target object rotation ')
    ], name="Target rotation")

    def execute(self, context):

        global target

        if self.action == 'Select_target':
            target = select_target_object()
        elif self.action == 'Rotate_object':
            if target != None:
                retrieve_reference()
                bpy.app.driver_namespace["shad_comparison"] = full_rotation(
                    target)
                bpy.app.driver_namespace["shad_comparison"] = rotate_object(
                    target)
        elif self.action == 'Fast_Rotate_object':
            if target != None:
                retrieve_reference()
                bpy.app.driver_namespace["shad_comparison"] = full_rotation(
                    target)
                bake_shadow()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_rotate_target)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rotate_target)


if __name__ == "__main__":
    register()
