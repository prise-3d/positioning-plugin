import bpy


class OBJECT_PT_shadow_comparator_panel (bpy.types.Panel):
    bl_idname = 'OBJECT_PT_shadow_comparator'
    bl_label = 'Manage elements of scene'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Manage shadow cast on a plane"

    def draw(self, context):

        obj = bpy.context.active_object

        layout = self.layout

        layout.operator('object.manage_plane',
                        text='Set Floor').action = 'Set_plane'

        if obj.type == 'MESH':
            layout.operator('object.manage_plane',
                            text='Add material to selection').action = 'Add_material'
            layout.operator('object.manage_plane',
                            text='Add texture to draw on').action = 'Reference_texture'
            layout.operator('object.manage_plane',
                            text='Bake shadows on object').action = 'Baking_texture'
            layout.operator('object.manage_plane',
                            text='Save drawn shadow').action = 'Save_baked'
            layout.operator('object.manage_plane',
                            text='Save baked shadow').action = 'Save_reference'


def register():
    bpy.utils.register_class(OBJECT_PT_shadow_comparator_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_shadow_comparator_panel)


if __name__ == "__main__":
    register()
