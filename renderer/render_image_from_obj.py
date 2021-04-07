import argparse
import os
import sys

import bpy

#since blender ignores all arguments after -- we need to use environment variables to pass arguments to the python script

if __name__ == '__main__':
    obj_file = os.getenv('obj_file')
    camera_view = int(os.getenv('camera_view'))
    bpy.ops.import_scene.obj(filepath=obj_file)
    selected = bpy.context.selected_objects[0]

    camObj = bpy.data.objects["Camera"]

    # view 1
    camObj.location[0] = 112.389
    camObj.location[1] = 107.188
    camObj.location[2] = 155.243
    camObj.rotation_mode = "QUATERNION"
    camObj.rotation_quaternion[0] = 0.043111
    camObj.rotation_quaternion[1] = 0.036924
    camObj.rotation_quaternion[2] = 0.649456
    camObj.rotation_quaternion[3] = 0.758277

    world = bpy.data.worlds["World"]
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 7.5

    camera = bpy.context.scene.camera
    camera.data.clip_start = 0.01
    camera.data.clip_end = 1000000
    bpy.context.scene.cycles.use_denoising = True
    for scene in bpy.data.scenes:
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1080
    bpy.context.scene.cycles.samples = 512
