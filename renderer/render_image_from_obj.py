import argparse
import os
import sys

import bpy

#since blender ignores all arguments after -- we need to use environment variables to pass arguments to the python script
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()
if __name__ == '__main__':
    obj_file = os.getenv('obj_file')
    camera_view = int(os.getenv('camera_view'))
    wall_material = os.getenv('wall_material')
    bpy.ops.import_scene.obj(filepath=obj_file)
    selected = bpy.context.selected_objects[0]
    bpy.ops.object.location_clear()
    bpy.ops.object.rotation_clear()
    bpy.ops.object.scale_clear()

    mat = bpy.data.materials[wall_material]
    print(bpy.data.materials.keys())
    clear_material(mat)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    diffuse = nodes.new( type = 'ShaderNodeBsdfPrincipled' )

    link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
    camObj = bpy.data.objects["Camera"]

    if camera_view == 1:
        # top down
        camObj.location[0] = 11.31883
        camObj.location[1] = 124.68112
        camObj.location[2] = 395.59085
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = .481
        camObj.rotation_quaternion[1] = .007
        camObj.rotation_quaternion[2] = -0.012
        camObj.rotation_quaternion[3] = -0.877
    elif camera_view == 2:
        #left view
        camObj.location[0] = 240.244
        camObj.location[1] = 89.0999
        camObj.location[2] = 70.8328
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = 0.147761
        camObj.rotation_quaternion[1] = 0.166308
        camObj.rotation_quaternion[2] = 0.728829
        camObj.rotation_quaternion[3] = 0.647547
    else:
        #right view
        camObj.location[0] = 59.5978
        camObj.location[1] = -7.64276
        camObj.location[2] = -76.8625
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = 0.017829
        camObj.rotation_quaternion[1] = 0.036848
        camObj.rotation_quaternion[2] = -0.89941
        camObj.rotation_quaternion[3] = -0.435185

    world = bpy.data.worlds["World"]
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 25

    camera = bpy.context.scene.camera
    camera.data.clip_start = 0.01
    camera.data.clip_end = 1000000
    bpy.context.scene.cycles.use_denoising = True
    for scene in bpy.data.scenes:
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1080
    bpy.context.scene.cycles.samples = 512
