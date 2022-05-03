import bpy


class OBJECT_PT_shadow_comparator_panel (bpy.types.Panel):
    bl_idname = 'OBJECT_PT_shadow_comparator'
    bl_label = 'Manage elements of scene'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Repositioning"

    def draw(self, context):

        obj = bpy.context.active_object

        layout = self.layout

        layout.operator('object.manage_plane',
                        text='Set Floor').action = 'Set_plane'

        if obj != None and obj.type == 'MESH':

            box = layout.box()
            box.label(text="Manage textures")

            ref_node = obj.name+"_"+"ref_image"
            shad_node = obj.name+"_"+"shadow_image"

            if obj.name not in bpy.data.materials:
                box.operator('object.manage_textures',
                             text='Add baking dedicated material').action = 'Add_material'
            else:
                tex_box = box.box()
                tex_box.operator('object.manage_textures',
                                 text='Set texture to draw on').action = 'Reference_texture'
                save_box = box.box()
                save_box.label(text="Save textures in temp")

                if ref_node in bpy.data.materials[obj.name].node_tree.nodes:
                    tex_box.operator('object.manage_textures',
                                     text='Draw on reference').action = 'Draw_reference'
                    save_box.operator('object.manage_textures',
                                      text='Save drawn shadow').action = 'Save_reference'

                if shad_node in bpy.data.materials[obj.name].node_tree.nodes:
                    save_box.operator('object.manage_textures',
                                      text='Save baked shadow').action = 'Save_baked'
                result_box = layout.box()
                result_box.label(text="Compare")
                result_box.operator('object.evaluate_shadow',
                                    text='Compare shadows').action = 'Compare'
                result_box.label(text="Comparison result")
                score = result_box.box()
                score.label(text=bpy.app.driver_namespace["shad_comparison"])


def register():
    bpy.utils.register_class(OBJECT_PT_shadow_comparator_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_shadow_comparator_panel)


if __name__ == "__main__":
    register()