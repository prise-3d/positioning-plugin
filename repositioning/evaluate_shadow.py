
import bpy


import sewar
import numpy
import PIL

from . manage_textures import bake_shadow, save_image


def compare_textures():
    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name]

    ref_name = object.name+"_"+"ref_image"
    shad_name = object.name+"_"+"shadow_image"

    if ref_name in bpy.data.materials[object.name].node_tree.nodes:

        save_image(object_material.node_tree.nodes[ref_name])
        save_image(bake_shadow())

        ref_image = numpy.asarray(PIL.Image.open(
            bpy.app.tempdir + ref_name+".png"))
        shad_image = numpy.asarray(PIL.Image.open(
            bpy.app.tempdir + shad_name+".png"))

        result = sewar.full_ref.rmse(ref_image, shad_image)
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
