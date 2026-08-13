import raylib as R1 # Need this for GetRandomValue and Fade?
import pyray as R

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


# Rotates the camera around its up vector
# Yaw is "looking left and right"
# If rotateAroundTarget is false, the camera rotates around its position
# Note: angle must be provided in radians
def CameraYaw(camera, angle, rotateAroundTarget):

    # Rotation axis
    up = R.GetCameraUp(camera);

    # View vector
    targetPosition = R.Vector3Subtract(camera.target, camera.position)

    # Rotate view vector around up axis
    targetPosition = R.Vector3RotateByAxisAngle(targetPosition, up, angle)

    if (rotateAroundTarget):
        # Move position relative to target
        camera.position = R.Vector3Subtract(camera.target, targetPosition)
    else: # rotate around camera.position
        # Move target relative to position
        camera.target = R.Vector3Add(camera.position, targetPosition)

# Rotates the camera around its right vector, pitch is "looking up and down"
#  - lockView prevents camera overrotation (aka "somersaults")
#  - rotateAroundTarget defines if rotation is around target or around its position
#  - rotateUp rotates the up direction as well (typically only useful in CAMERA_FREE)
# NOTE: [angle] must be provided in radians
def CameraPitch(camera, angle, lockView, rotateAroundTarget, rotateUp):

    # Rotation axis
    up = R.GetCameraUp(camera);

    # View vector
    targetPosition = R.Vector3Subtract(camera.target, camera.position)

    if(lockView):
        # In these camera modes, clamp the Pitch angle
        # to allow only viewing straight up or down

        # Clamp view up
        maxAngleUp = R.Vector3Angle(up, targetPosition);
        maxAngleUp -= 0.001; # avoid numerical errors
        if (angle > maxAngleUp):
            angle = maxAngleUp;

        # Clamp view down
        maxAngleDown = R.Vector3Angle(R.Vector3Negate(up), targetPosition);
        maxAngleDown *= -1.0; # downwards angle is negative
        maxAngleDown += 0.001; # avoid numerical errors
        if (angle < maxAngleDown):
            angle = maxAngleDown;

    # Rotation axis
    right = R.GetCameraRight(camera);

    # Rotate view vector around right axis
    targetPosition = R.Vector3RotateByAxisAngle(targetPosition, right, angle);

    if (rotateAroundTarget):
        # Move position relative to target
        camera.position = R.Vector3Subtract(camera.target, targetPosition);
    else: # Rotate around camera.position
        # Move target relative to position
        camera.target = R.Vector3Add(camera.position, targetPosition);

    if (rotateUp):
        # Rotate up direction around right axis
        camera.up = R.Vector3RotateByAxisAngle(camera.up, right, angle);

def main():
    MAX_COLUMNS=20
    screenWidth = 800;
    screenHeight = 450;
    # R.set_config_flags(R.FLAG_WINDOW_UNDECORATED) # Windowless
    R.init_window(screenWidth, screenHeight, b"raylib [core] example - 3d camera first person");

    camera = R.Camera()
    camera.position = R.Vector3(0,20,40)                    # Camera position
    camera.target = R.Vector3(0,2,0) # Camera looking at point
    camera.up = R.Vector3(0,1,0)# Camera up vector (rotation towards target)
    camera.fovy = 60;                                # Camera field-of-view Y
    camera.projection = R.CAMERA_PERSPECTIVE;             # Camera projection type

    cameraMode = R.CAMERA_FIRST_PERSON;

    # Generates some random columns
    heights = []
    positions = []
    colors = []

    for i in range(MAX_COLUMNS):
        heights.append(R1.GetRandomValue(1, 12))
        positions.append(R.Vector3(R1.GetRandomValue(-15, 15), (heights[i]/2.0), R1.GetRandomValue(-15, 15)))
        colors.append(R.Color(R1.GetRandomValue(20, 255), R1.GetRandomValue(10, 55), 30, 255 ))

    # Don't love this?
    # R.disable_cursor();                    # Limit cursor to relative movement inside the window

    R.set_target_fps(60);                   # Set our game to run at 60 frames-per-second
    while not R.window_should_close():

        if move := R.get_mouse_wheel_move(): #  GetMouseWheelMove(void);                          // Get mouse wheel movement for X or Y, whichever is larger
            print(f"MOVE {move=}")
        # elif move1 := R.get_mouse_wheel_move_v(): # GetMouseWheelMoveV(void);                       // Get mouse wheel movement for both X and Y
        #     if move1 != move:
        #         move = move1
        #     print(f"MOVE_V {move=}")


        # Update
        #----------------------------------------------------------------------------------
        # Switch camera mode
        if (R.is_key_pressed(R.KEY_ONE)):
            cameraMode = R.CAMERA_FREE;
            camera.up = R.Vector3(0,1,0)

        if (R.is_key_pressed(R.KEY_TWO)):
            cameraMode = R.CAMERA_FIRST_PERSON;
            camera.up = R.Vector3(0,1,0)

        if (R.is_key_pressed(R.KEY_THREE)):
            # Rotates camera about a fixed point - very similar to the other gds viewer
            cameraMode = R.CAMERA_THIRD_PERSON;
            camera.up = R.Vector3(0,1,0)

        if (R.is_key_pressed(R.KEY_FOUR)):
            # Slowly rotates?
            cameraMode = R.CAMERA_ORBITAL;
            camera.up = R.Vector3(0,1,0)
        if (R.is_key_pressed(R.KEY_P)):
            if (camera.projection == R.CAMERA_PERSPECTIVE):
                # Create isometric view
                cameraMode = R.CAMERA_THIRD_PERSON;
                # Note: The target distance is related to the render distance in the orthographic projection
                camera.position = R.Vector3(0,2,-100)
                camera.target = R.Vector3(0,2,0)
                camera.up = R.Vector3(0,1,0)
                camera.projection = R.CAMERA_ORTHOGRAPHIC;
                camera.fovy = 20.0; # near plane width in R.CAMERA_ORTHOGRAPHIC
                CameraYaw(camera, -135*R.DEG2RAD, rotate_around_target=True) # TODO: Maybe we don't want yaw?
                CameraPitch(camera, -45*R.DEG2RAD, lock_view=True, rotate_around_target=True, rotate_up=False)
            elif (camera.projection == R.CAMERA_ORTHOGRAPHIC):
                # Reset to default view
                cameraMode = R.CAMERA_THIRD_PERSON;
                camera.position = R.Vector3(0,2,10)
                camera.target = R.Vector3(0,2,0)
                camera.up = R.Vector3(0,1,0)
                camera.projection = R.CAMERA_PERSPECTIVE;
                camera.fovy = 60.0;

        # Update camera computes movement internally depending on the camera mode
        # Some default standard keyboard/mouse inputs are hardcoded to simplify use
        # For advanced camera controls, it's recommended to compute camera movement manually
        R.update_camera(camera, cameraMode);                  # Update camera


        if R.begin_drawing() or True: # Allow us to use indenting
            R.clear_background(R.WHITE)
            R.draw_text(b"Hello world", 190, 200, 20, R.VIOLET)



            if R.begin_mode_3d(camera) or True: # Allow us to use indenting
                R.draw_plane(R.Vector3(0.0, 0.0, 0.0 ), R.Vector2( 32.0, 32.0 ), R.LIGHTGRAY); # Draw ground
                R.draw_cube(R.Vector3( -16.0, 2.5, 0.0 ), 1.0, 5.0, 32.0, R.BLUE);     # Draw a blue wall
                R.draw_cube(R.Vector3( 16.0, 2.5, 0.0 ), 1.0, 5.0, 32.0, R.LIME);      # Draw a green wall
                R.draw_cube(R.Vector3( 0.0, 2.5, 16.0 ), 32.0, 5.0, 1.0, R.GOLD);      # Draw a yellow wall

                # # Draw some cubes around
                for i in range(MAX_COLUMNS):
                    R.draw_cube(positions[i], 2.0, heights[i], 2.0, colors[i]);
                    R.draw_cube_wires(positions[i], 2.0, heights[i], 2.0, R.MAROON);

                if (cameraMode == R.CAMERA_THIRD_PERSON):
                    R.draw_cube(camera.target, 0.5, 0.5, 0.5, R.PURPLE);
                    R.draw_cube_wires(camera.target, 0.5, 0.5, 0.5, R.DARKPURPLE);

            R.end_mode_3d();



            # Draw info boxes
            R.draw_rectangle(5, 5, 330, 100, R1.Fade(R.SKYBLUE, 0.5));
            R.draw_rectangle_lines(5, 5, 330, 100, R.BLUE);

            R.draw_text(b"Camera controls:", 15, 15, 10, R.BLACK);
            R.draw_text(b"- Move keys: W, A, S, D, Space, Left-Ctrl", 15, 30, 10, R.BLACK);
            R.draw_text(b"- Look around: arrow keys or mouse", 15, 45, 10, R.BLACK);
            R.draw_text(b"- Camera mode keys: 1, 2, 3, 4", 15, 60, 10, R.BLACK);
            R.draw_text(b"- Zoom keys: num-plus, num-minus or mouse scroll", 15, 75, 10, R.BLACK);
            R.draw_text(b"- Camera projection key: P", 15, 90, 10, R.BLACK);

            R.draw_rectangle(600, 5, 195, 100, R1.Fade(R.SKYBLUE, 0.5));
            R.draw_rectangle_lines(600, 5, 195, 100, R.BLUE);

            R.draw_text(b"Camera status:", 610, 15, 10, R.BLACK);
            mode = {
                R.CAMERA_FREE: "FREE",
                R.CAMERA_FIRST_PERSON: "FIRST_PERSON",
                R.CAMERA_THIRD_PERSON: "THIRD_PERSON",
                R.CAMERA_ORBITAL: "ORBITAL",
            }.get(cameraMode, "CUSTOM")

            R.draw_text(f"- Mode: {mode}", 610, 30, 10, R.BLACK);
            proj = {
                R.CAMERA_PERSPECTIVE: "PERSPECTIVE",
                R.CAMERA_ORTHOGRAPHIC: "ORTHOGRAPHIC"
            }.get(camera.projection, "CUSTOM")
            R.draw_text(f"- Projection: {proj}", 610, 45, 10, R.BLACK);
            R.draw_text(f"- Position: ({camera.position.x:.03f}, {camera.position.y:.03f}, {camera.position.z:.03f})", 610, 60, 10, R.BLACK);
            R.draw_text(f"- Target: ({camera.target.x:.03f}, {camera.target.y:.03f}, {camera.target.z:.03f})", 610, 75, 10, R.BLACK);
            R.draw_text(f"- Up: ({camera.up.x:.03f}, {camera.up.y:.03f}, {camera.up.z:.03f})", 610, 90, 10, R.BLACK);

        R.end_drawing()

    R.close_window()


if __name__ == '__main__':
    main()
