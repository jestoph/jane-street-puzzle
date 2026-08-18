import raylib as R1 # Need this for GetRandomValue and Fade?
import pyray as R
import gdstk

"""
Bravely stolen from the 3d raylib examples and roughly ported to python
https://www.raylib.com/examples/core/loader.html?name=core_3d_camera_first_person

My understanding of the zlib/libpng license is that the copyright notice must be attached,
so here it is -

/*******************************************************************************************
*
*   raylib [core] example - 3d camera first person
*
*   Example complexity rating: [★★☆☆] 2/4
*
*   Example originally created with raylib 1.3, last time updated with raylib 1.3
*
*   Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
*   BSD-like license that allows static linking with closed source software
*
*   Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)
*
********************************************************************************************/


I intend to heavily modify this, so maybe it's not needed.

"""



def CameraMoveUp(camera, distance):
    up = GetCameraUp(camera)
    up = R.vector3_scale(up, distance)
    camera.position = R.vector3_add(camera.position, up)
    camera.target = R.vector3_add(camera.target, up)


def CameraMoveRight(camera, distance, moveInWorldPlane):
    right = GetCameraRight(camera)
    if moveInWorldPlane:
        if (abs(camera.up.z) > 0.7071): right.z = 0
        elif (abs(camera.up.x) > 0.7071): right.x = 0
        else: right.y = 0
        right = R.vector3_normalize(right)

    right = R.vector3_scale(right, distance)
    camera.position = R.vector3_add(camera.position, right)
    camera.target = R.vector3_add(camera.target, right)

def CameraMoveToTarget(camera, delta):
    distance = R.vector3_distance(camera.position, camera.target)
    distance += delta
    if (distance <= 0): distance = 0.001
    forward = GetCameraForward(camera)
    camera.position = R.vector3_add(camera.target, R.vector3_scale(forward, -distance))

def GetCameraForward(camera):
    return R.vector3_normalize(R.vector3_subtract(camera.target, camera.position))

def GetCameraUp(camera):
    return R.vector3_normalize(camera.up)

def GetCameraRight(camera):
    forward = GetCameraForward(camera)
    up = GetCameraUp(camera)

    return R.vector3_normalize(R.vector3_cross_product(forward, up))

def UpdateCamera(camera):

    camera_mouse_move_rotate_sensitivity =0.003
    camera_mouse_move_pan_sensitivity=0.1

    mousePositionDelta = R.get_mouse_delta()
    mouseWheelMoveDelta = R.get_mouse_wheel_move()

    rotateAroundTarget = True
    lockView = True
    rotateUp = False

    KEY_LEFT_SHIFT      = 340
    KEY_RIGHT_SHIFT     = 344

    if R.is_mouse_button_down(R.MOUSE_BUTTON_LEFT) and (R.is_key_down(KEY_LEFT_SHIFT) or R.is_key_down(KEY_RIGHT_SHIFT)):
        # CAMERA PAN
        CameraMoveRight(camera, -mousePositionDelta.x * camera_mouse_move_pan_sensitivity, True)
        CameraMoveUp(camera, mousePositionDelta.y * camera_mouse_move_pan_sensitivity)

    elif R.is_mouse_button_down(R.MOUSE_BUTTON_LEFT):
        # CAMERA ROTATE
        CameraYaw(camera, -mousePositionDelta.x*camera_mouse_move_rotate_sensitivity, rotateAroundTarget)
        CameraPitch(camera, -mousePositionDelta.y*camera_mouse_move_rotate_sensitivity, lockView, rotateAroundTarget, rotateUp)

    if mouseWheelMoveDelta != 0.0:
        # CAMERA ZOOM
        CameraMoveToTarget(camera, -mouseWheelMoveDelta)


def CameraYaw(camera, angle, rotateAroundTarget):

    # Rotation axis
    up = GetCameraUp(camera)

    # View vector
    targetPosition = R.vector3_subtract(camera.target, camera.position)

    # Rotate view vector around up axis
    targetPosition = R.vector3_rotate_by_axis_angle(targetPosition, up, angle)

    if (rotateAroundTarget):
        # Move position relative to target
        camera.position = R.vector3_subtract(camera.target, targetPosition)
    else: # rotate around camera.position
        # Move target relative to position
        camera.target = R.vector3_add(camera.position, targetPosition)

def CameraPitch(camera, angle, lockView, rotateAroundTarget, rotateUp):

    # Rotation axis
    up = GetCameraUp(camera)

    # View vector
    targetPosition = R.vector3_subtract(camera.target, camera.position)

    if(lockView):
        # In these camera modes, clamp the Pitch angle
        # to allow only viewing straight up or down

        # Clamp view up
        maxAngleUp = R.vector3_angle(up, targetPosition)
        maxAngleUp -= 0.001 # avoid numerical errors
        if (angle > maxAngleUp):
            angle = maxAngleUp

        # Clamp view down
        maxAngleDown = R.vector3_angle(R.vector3_negate(up), targetPosition)
        maxAngleDown *= -1.0 # downwards angle is negative
        maxAngleDown += 0.001 # avoid numerical errors
        if (angle < maxAngleDown):
            angle = maxAngleDown

    # Rotation axis
    right = GetCameraRight(camera)

    # Rotate view vector around right axis
    targetPosition = R.vector3_rotate_by_axis_angle(targetPosition, right, angle)

    if (rotateAroundTarget):
        # Move position relative to target
        camera.position = R.vector3_subtract(camera.target, targetPosition)
    else: # Rotate around camera.position
        # Move target relative to position
        camera.target = R.vector3_add(camera.position, targetPosition)

    if (rotateUp):
        # Rotate up direction around right axis
        camera.up = R.vector3_rotate_by_axis_angle(camera.up, right, angle)


def draw_info(camera):
    # Draw info boxes
    R.draw_rectangle(5, 5, 330, 100, R1.Fade(R.SKYBLUE, 0.5))
    R.draw_rectangle_lines(5, 5, 330, 100, R.BLUE)

    R.draw_text(b"Camera controls:", 15, 15, 10, R.BLACK)
    R.draw_text(b"- Move keys: W, A, S, D, Space, Left-Ctrl", 15, 30, 10, R.BLACK)
    R.draw_text(b"- Look around: arrow keys or mouse", 15, 45, 10, R.BLACK)
    R.draw_text(b"- Camera mode keys: 1, 2, 3, 4", 15, 60, 10, R.BLACK)
    R.draw_text(b"- Zoom keys: num-plus, num-minus or mouse scroll", 15, 75, 10, R.BLACK)
    R.draw_text(b"- Camera projection key: P", 15, 90, 10, R.BLACK)

    R.draw_rectangle(600, 5, 195, 100, R1.Fade(R.SKYBLUE, 0.5))
    R.draw_rectangle_lines(600, 5, 195, 100, R.BLUE)

    R.draw_text(b"Camera status:", 610, 15, 10, R.BLACK)
    proj = {
        R.CAMERA_PERSPECTIVE: "PERSPECTIVE",
        R.CAMERA_ORTHOGRAPHIC: "ORTHOGRAPHIC"
    }.get(camera.projection, "CUSTOM")
    R.draw_text(f"- Projection: {proj}", 610, 45, 10, R.BLACK)
    R.draw_text(f"- Position: ({camera.position.x:.03f}, {camera.position.y:.03f}, {camera.position.z:.03f})", 610, 60, 10, R.BLACK)
    R.draw_text(f"- Target: ({camera.target.x:.03f}, {camera.target.y:.03f}, {camera.target.z:.03f})", 610, 75, 10, R.BLACK)
    R.draw_text(f"- Up: ({camera.up.x:.03f}, {camera.up.y:.03f}, {camera.up.z:.03f})", 610, 90, 10, R.BLACK)

def build_world():


    library = gdstk.read_gds("warmup/04_final.gds")

    c = R.Color(R1.GetRandomValue(20, 255), R1.GetRandomValue(10, 55), 30, 255 )

    ret = []
    for cell in library.cells:
        name = cell.name
        if 'mux' not in name: continue

        for poly in cell.polygons:

            # TODO: Project correctly on to pixels
            # RLAPI void DrawCube(Vector3 position, float width, float height, float length, Color color);             // Draw cube
            (minx, miny), (maxx, maxy) = poly.bounding_box()
            (minz, maxz) = (0, 1)

            px, pz, py = (minx + maxx)/2, -(miny + maxy)/2, (minz+maxz)/2
            sx, sz, sy = maxx - minx, maxy-miny, maxz-maxz

            position = R.Vector3(px, py, pz)
            size = R.Vector3(sx, sy, sz)
            colour = c

            ret.append((position, size, colour))

    return ret





def main():
    screenWidth = 800
    screenHeight = 450
    # R.set_config_flags(R.FLAG_WINDOW_UNDECORATED) # Windowless
    R.init_window(screenWidth, screenHeight, b"raylib [core] example - 3d camera first person")

    camera = R.Camera()
    camera.position = R.Vector3(0,20,40)                    # Camera position
    camera.target = R.Vector3(0,2,0) # Camera looking at point
    camera.up = R.Vector3(0,1,0)# Camera up vector (rotation towards target)
    camera.fovy = 60                                # Camera field-of-view Y
    camera.projection = R.CAMERA_PERSPECTIVE             # Camera projection type

    world =  build_world()


    # Don't love this?
    # R.disable_cursor()                    # Limit cursor to relative movement inside the window

    R.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    SHOW_TARGET=False
    while not R.window_should_close():

        # Update
        #----------------------------------------------------------------------------------
        if (R.is_key_pressed(R.KEY_ONE)):
            SHOW_TARGET = not SHOW_TARGET


        # Update camera computes movement internally depending on the camera mode
        # Some default standard keyboard/mouse inputs are hardcoded to simplify use
        # For advanced camera controls, it's recommended to compute camera movement manually
        UpdateCamera(camera)


        if R.begin_drawing() or True: # Allow us to use indenting
            R.clear_background(R.WHITE)
            R.draw_text(b"Hello world", 190, 200, 20, R.VIOLET)



            if R.begin_mode_3d(camera) or True: # Allow us to use indenting

                # R.draw_plane(R.Vector3(0.0, 0.0, 0.0 ), R.Vector2( 100.0, 100.0 ), R.LIGHTGRAY) # Draw ground

                R.draw_grid(100, 1) # count, spacing

                # DrawCube(Vector3 position, float width, float height, float length, Color color)
                R.draw_cube(R.Vector3( -16.0, 2.5, 0.0 ), 1.0, 0.1, 32.0, R.BLUE)     # Draw a blue wall
                R.draw_cube(R.Vector3( 16.0, 2.5, 0.0 ), 1.0, 0.1, 32.0, R.LIME)      # Draw a green wall
                R.draw_cube(R.Vector3( 0.0, 2.5, 16.0 ), 32.0, 0.1, 1.0, R.GOLD)      # Draw a yellow wall

                # # Draw some cubes around
                for position, size, colour in world:
                    R.draw_cube_v(position, size, colour)
                    R.draw_cube_wires_v(position, size, R.MAROON)

                if SHOW_TARGET:
                    R.draw_cube(camera.target, 0.5, 0.5, 0.5, R.PURPLE)
                    R.draw_cube_wires(camera.target, 0.5, 0.5, 0.5, R.DARKPURPLE)

            R.end_mode_3d()



            draw_info(camera)

        R.end_drawing()

    R.close_window()


if __name__ == '__main__':
    main()
