import bpy

reference_image = None
baked_image = None


def add_object_material():
    object = bpy.context.active_object
    if object.name_full not in bpy.data.materials:
        object_material = bpy.data.materials.new(object.name_full)
        object_material.use_nodes = True  # Mandatory for texture manipulation
        object.data.materials.append(object_material)

        mix_node = object_material.node_tree.nodes.new('ShaderNodeMixRGB')

        bsdf = object_material.node_tree.nodes["Principled BSDF"]
        object_material.node_tree.links.new(
            bsdf.inputs['Base Color'], mix_node.outputs['Color'])

        # A mix node to see both the baked texture and the drawn shadow at the same time
        bpy.data.materials[object.name_full].node_tree.nodes["Mix"].inputs[0].default_value = 0.8

        # Enable texture visibility in the ViewPort
        if bpy.context.space_data.shading.type != 'MATERIAL':
            bpy.context.space_data.shading.type = 'MATERIAL'

    else:
        object_material = bpy.data.materials[object.name_full]
        object.data.materials.append(object_material)


def new_blank_image(img_name="tex_image"):

    object = bpy.context.active_object
    name = object.name_full+"_"+img_name

    object_material = bpy.data.materials[object.name_full]

    if name not in object_material.node_tree.nodes:
        image = object_material.node_tree.nodes.new('ShaderNodeTexImage')
        image.name = name
        image.image = bpy.data.images.new(
            name=name, width=1024, height=1024, alpha=True)

    else:
        print("Node already exist")
        image = object_material.node_tree.nodes[name]

    image.image.generated_color = (1, 1, 1, 1)  # turn image white
    return(image)


# Image on which targeted shadow can be drawn
def new_reference_image(name="ref_image"):
    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name_full]

    reference_image = new_blank_image(name)

    # Link image texture node to color of BSDF node through a Mix node
    mix_images = object_material.node_tree.nodes["Mix"]

    object_material.node_tree.links.new(
        mix_images.inputs['Color1'], reference_image.outputs['Color'])
    print("Reference image created and linked")
    return(reference_image)


# Save image from a node in temp directory of Blender
def save_image(node):
    bpy.data.images[node.image.name_full].filepath_raw = bpy.app.tempdir + \
        node.image.name_full+".png"
    bpy.data.images[node.image.name_full].file_format = 'PNG'
    bpy.data.images[node.image.name_full].save()


def bake_shadow():

    global baked_image

    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name_full]

    blank_base = new_blank_image("blank")

    bsdf = object_material.node_tree.nodes["Principled BSDF"]
    object_material.node_tree.links.new(
        bsdf.inputs['Base Color'], blank_base.outputs['Color'])

    baked_image = new_blank_image("shadow_image")
    object_material.node_tree.nodes.active = object_material.node_tree.nodes[
        baked_image.name]
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.preview_samples = 1
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.cycles.bake_type = 'SHADOW'
    bpy.ops.object.bake()

    mix_images = object_material.node_tree.nodes["Mix"]
    mix_images.blend_type = "DARKEN"

    object_material.node_tree.links.new(
        mix_images.inputs['Color2'], baked_image.outputs['Color'])

    object_material.node_tree.links.new(
        bsdf.inputs['Base Color'], mix_images.outputs['Color'])

    return (baked_image)


def draw_on_ref():
    object = bpy.context.active_object
    object_material = bpy.data.materials[object.name_full]

    bpy.context.window.workspace = bpy.data.workspaces['Texture Paint']

    # Image dedicated to reference drawing automatically selected back so that the baking texture won't be drawn on
    object_material.node_tree.nodes.active = object_material.node_tree.nodes[
        object.name_full+"_ref_image"]


class OBJECT_OT_manage_textures(bpy.types.Operator):

    bl_idname = "object.manage_textures"
    bl_label = "Add materials and textures to a mesh"
    bl_description = "This operator permits the addition of textures enabling to retrieve shadows"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(
        items=[
            ('Add_material', 'Add a material to the selected mesh',
             'generate a new material dedicated to baking'),
            ('Reference_texture', 'Add an image texture to draw on',
             'generate a texture to draw on'),
            ('Baking_texture', 'Add an image texture to bake on',
             'generate a texture and bake shadow on it'),
            ('Save_reference', 'Save shadow reference texture',
             'save texture on which on shadow was drawn'),
            ('Save_baked', 'Save Baked Texture',
             'save texture on which shadow was baked'),
            ('Draw_reference', 'Draw on Reference',
             'draw targeted shadow on reference')

        ], name="Baking material management")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Managing textures")

    def execute(self, context):

        global reference_image
        global baked_image

        if self.action == 'Add_material':
            add_object_material()
        elif self.action == 'Reference_texture':
            reference_image = new_reference_image()
        elif self.action == 'Baking_texture':
            bake_shadow()
        elif self.action == 'Save_reference':
            save_image(reference_image)
        elif self.action == 'Save_baked':
            save_image(baked_image)
        elif self.action == 'Draw_reference':
            draw_on_ref()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_manage_textures)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_manage_textures)


if __name__ == "__main__":
    register()
