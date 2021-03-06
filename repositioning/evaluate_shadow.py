
import bpy

import numpy as np
from PIL import Image

from . manage_textures import bake_shadow, save_image


def rmse(prediction, target):
    return np.sqrt(((prediction.astype(np.float64)-target.astype(np.float64))**2).mean())


def retrieve_reference():
    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name_full]
    ref_name = object.name_full+"_"+"ref_image"
    save_image(object_material.node_tree.nodes[ref_name])


def select_target_object():
    return (bpy.context.active_object)


def compare_textures(res=1024):
    object = bpy.context.active_object
    ref_name = object.name_full+"_"+"ref_image"
    shad_name = object.name_full+"_"+"shadow_image"

    if ref_name in bpy.data.materials[object.name_full].node_tree.nodes:

        ref_image_name = bpy.data.materials[object.name_full].node_tree.nodes[ref_name].image.name

        save_image(bake_shadow(res))

        shad_image_name = bpy.data.materials[object.name_full].node_tree.nodes[shad_name].image.name

        ref_image = np.asarray(Image.open(
            bpy.app.tempdir + ref_image_name+".png").resize((res, res)))
        shad_image = np.asarray(Image.open(
            bpy.app.tempdir + shad_image_name+".png"))

        result = rmse(ref_image, shad_image)
        return(result)
    else:
        return("Please, set a reference")


class OBJECT_OT_evaluate_shadow(bpy.types.Operator):
    bl_idname = "object.evaluate_shadow"
    bl_label = "Result of targeted and computed shadow comparison"
    bl_description = "Give a score indicating whether objects are correctly placed in the scene"
    bl_options = {'REGISTER', 'UNDO'}

    evaluation_result = "No evaluation yet"

    action: bpy.props.EnumProperty(items=[(
        'Compare', 'Compare shadows', 'Compare drawn and generated shadows'), ], name="Texture comparisons")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=self.evaluation_result)

    def execute(self, context):
        if self.action == 'Compare':
            retrieve_reference()
            self.evaluation_result = str(compare_textures())

            # Result of RMSE operation is put in Blender's global dictionnary driver_namespace so that we can access it in any other operator

            bpy.app.driver_namespace["shad_comparison"] = self.evaluation_result
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_evaluate_shadow)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_evaluate_shadow)


if __name__ == "__main__":
    register()
