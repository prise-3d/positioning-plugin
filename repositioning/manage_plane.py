import bpy

reference_image = None
baked_image = None


def set_plane(p_size=0, p_name="Floor", x_location=0, y_location=0, z_location=0, x_rotation=0, y_rotation=0, z_rotation=0):
    bpy.ops.mesh.primitive_plane_add(size=p_size, enter_editmode=False, align='WORLD', location=(
        x_location, y_location, z_location), rotation=(x_rotation, y_rotation, z_rotation))
    plane = bpy.context.active_object
    plane.name = p_name

    return(plane)


def add_object_material():
    object = bpy.context.active_object
    if object.name not in bpy.data.materials:
        object_material = bpy.data.materials.new(object.name)
        object_material.use_nodes = True  # Mandatory for texture manipulation
        object.data.materials.append(object_material)

    else:
        object_material = bpy.data.materials[object.name]
        object.data.materials.append(object_material)
    print(object_material)


def new_blank_image(img_name="tex_image"):

    object = bpy.context.active_object
    name = object.name+"_"+img_name

    object_material = bpy.data.materials[object.name]

    if name not in object_material.node_tree.nodes:
        image = object_material.node_tree.nodes.new('ShaderNodeTexImage')
        image.name = name
        image.image = bpy.data.images.new(
            name=name, width=1024, height=1024, alpha=True)

    else:
        print("node already exist")
        image = object_material.node_tree.nodes[name]

    image.image.generated_color = (1, 1, 1, 1)  # turn image white
    return(image)


# Image on which targeted shadow can be drawn
def new_reference_image(name="ref_image"):
    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name]

    reference_image = new_blank_image(name)

    print("label : ", reference_image.name)
    # Link image texture node to color of BSDF node
    bsdf = object_material.node_tree.nodes["Principled BSDF"]

    object_material.node_tree.links.new(
        bsdf.inputs['Base Color'], reference_image.outputs['Color'])
    print("Reference image created and linked")
    return(reference_image)


# Not working right now
def save_image(node):
    bpy.data.images[node.image.name].filepath_raw = "//"+node.image.name+".png"
    bpy.data.images[node.image.name].file_format = 'PNG'
    bpy.data.images[node.image.name].save()


def bake_shadow():

    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name]

    blank_base = new_reference_image("blank")

    baked_image = new_blank_image("shadow_image")
    object_material.node_tree.nodes.active = object_material.node_tree.nodes[baked_image.name]
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.preview_samples = 1
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.cycles.bake_type = 'SHADOW'
    bpy.ops.object.bake()

    return (baked_image)


class OBJECT_OT_manage_plane(bpy.types.Operator):

    bl_idname = "object.manage_plane"
    bl_label = "Place a plane with material to cast shadows on "
    bl_description = "This operator permits the addition of a plane which permitts to retrieve shadows"
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
            ('Add_material', 'Add a material to the selected mesh',
             'generate a new material dedicated to baking'),
            ('Reference_texture', 'Add an image texture to draw on',
             'generate a texture to draw on'),
            ('Baking_texture', 'Add an image texture to bake on',
             'generate a texture and bake shadow on it'),
            ('Save_reference', 'Save shadow reference texture',
             'save texture on which on sahdow was drawn'),
            ('Save_baked', 'Save Baked Texture',
             'save texture on which shadow was baked')

        ], name="Plane management")

    def execute(self, context):

        global reference_image
        global baked_image

        if self.action == 'Set_plane':
            set_plane(self.p_size,
                      self.p_name,
                      self.x_location,
                      self.y_location,
                      self.z_location,
                      self.x_rotation,
                      self.y_rotation,
                      self.z_rotation)

        elif self.action == 'Add_material':
            add_object_material()
        elif self.action == 'Reference_texture':
            reference_image = new_reference_image()
        elif self.action == 'Baking_texture':
            baked_image = bake_shadow()
        elif self.action == 'Save_reference':
            save_image(reference_image)
        elif self.action == 'Save_baked':
            save_image(baked_image)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_manage_plane)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_manage_plane)


if __name__ == "__main__":
    register()
