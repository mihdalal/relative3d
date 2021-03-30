import argparse
import os
import sys

import bpy

#since blender ignores all arguments after -- we need to use environment variables to pass arguments to the python script

if __name__ == '__main__':
    obj_file = os.getenv('obj_file')
    camera_view = int(os.getenv('camera_view'))
    print(obj_file)
    bpy.ops.import_scene.obj(filepath=obj_file)
    selected = bpy.context.selected_objects[0]

    bpy.ops.object.light_add(type="SUN", location=selected.location)
    bpy.data.objects["Sun"].data.energy = 2.5

    camObj = bpy.data.objects["Camera"]


    if camera_view == 1:
        # view 1
        camObj.location[0] = -94.1033
        camObj.location[1] = -67.0645
        camObj.location[2] = 240.717
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = 0.674143
        camObj.rotation_quaternion[1] = -0.229633
        camObj.rotation_quaternion[2] = -0.221883
        camObj.rotation_quaternion[3] = 0.666009
    else:
        camObj.location[0] = -184.358
        camObj.location[1] = -138.247
        camObj.location[2] = 178.097
        camObj.rotation_mode = "QUATERNION"
        camObj.rotation_quaternion[0] = 0.819345
        camObj.rotation_quaternion[1] = 0.17949
        camObj.rotation_quaternion[2] = -0.542787
        camObj.rotation_quaternion[3] = 0.042891

    camera = bpy.context.scene.camera
    camera.data.clip_start = 100
    camera.data.clip_end = 10000
