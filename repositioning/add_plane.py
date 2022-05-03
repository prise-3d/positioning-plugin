import bpy


def set_plane(p_size=0, p_name="Floor", x_location=0, y_location=0, z_location=0, x_rotation=0, y_rotation=0, z_rotation=0):
    bpy.ops.mesh.primitive_plane_add(size=p_size, enter_editmode=False, align='WORLD', location=(
        x_location, y_location, z_location), rotation=(x_rotation, y_rotation, z_rotation))
    plane = bpy.context.active_object
    plane.name = p_name

    return(plane)


class OBJECT_OT_manage_plane(bpy.types.Operator):

    bl_idname = "object.manage_plane"
    bl_label = "Place a plane with material to cast shadows on "
    bl_description = "This operator permits the addition of a plane to cast shadows on"
    bl_options = {'REGISTER', 'UNDO'}

    p_size: bpy.props.FloatProperty(name="Size", default=10)

    p_name: bpy.props.StringProperty(name="Name", default="Floor")

    x_location: bpy.props.FloatProperty(name="location X", default=0)
    y_location: bpy.props.FloatProperty(name="Y", default=0)
    z_location: bpy.props.FloatProperty(name="Z", default=0)

    x_rotation: bpy.props.FloatProperty(name="rotation X", default=0)
    y_rotation: bpy.props.FloatProperty(name="Y", default=0)
    z_rotation: bpy.props.FloatProperty(name="Z", default=0)

    action: bpy.props.EnumProperty(
        items=[
            ('Set_plane', 'Add a plane',
             'generate a plane'),
        ], name="Plane management")

    def execute(self, context):

        if self.action == 'Set_plane':
            set_plane(self.p_size,
                      self.p_name,
                      self.x_location,
                      self.y_location,
                      self.z_location,
                      self.x_rotation,
                      self.y_rotation,
                      self.z_rotation)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_manage_plane)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_manage_plane)


if __name__ == "__main__":
    register()
