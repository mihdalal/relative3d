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
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    #remove previous settings for material
    mat.node_tree.links.clear()
    mat.node_tree.nodes.clear()

    mixshader = nodes.new(type='ShaderNodeMixShader')
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    transparent_bsdf = nodes.new(type='ShaderNodeBsdfTransparent')

    #adds mixed shader to surface option for material
    link = links.new( mixshader.outputs[0], output.inputs['Surface'] )

    #adds back the bsdf and makes it transparent
    link = links.new( principled_bsdf.outputs['BSDF'], mixshader.inputs[1])
    link = links.new( transparent_bsdf.outputs['BSDF'], mixshader.inputs[2])

    camObj = bpy.data.objects["Camera"]

    if camera_view == 1:
        # top down
        camObj.location[0] = 18.9166
        camObj.location[1] = 238.95
        camObj.location[2] = 800
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = .482
        camObj.rotation_quaternion[1] = 0.0001
        camObj.rotation_quaternion[2] = -0.0001
        camObj.rotation_quaternion[3] = -0.876

    elif camera_view == 2:
        #left view
        camObj.location[0] = -389.988
        camObj.location[1] = 506.106
        camObj.location[2] = 800
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = 0.435469
        camObj.rotation_quaternion[1] = 0.192065
        camObj.rotation_quaternion[2] = -0.354908
        camObj.rotation_quaternion[3] = -0.804685
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
        scene.render.resolution_x = 4320
        scene.render.resolution_y = 4320
    bpy.context.scene.cycles.samples = 512

    #bpy.context.scene.cycles.device = 'GPU'
    #bpy.context.user_preferences.addon['cycles'].preferences.compute_device_type = 'CUDA'
    #bpy.context.user_preferences.addon['cycles'].preferences.compute_device = 'CUDA_1'
