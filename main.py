from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import camera
import player as player_module
import scene
import math
import time

player = player_module.Player()
camera_state = camera.CameraState()
modo_camera = 0

posicoes_camera = [
    None,
    [50, 40, 0, 0, 0, 0, 0, 1, 0],
    [-52, 30, -100, 0, 0, 0, 0, 1, 0]
]

window_width = 1080
window_height = 1920

collision_boxes = [
    (-25, 15, 0, 40),
    (-21, -19, -9, -1),
    (-11, -9, -9, -1),
    (-1, 1, -9, -1)
]

def lerp(start, end, t):
    return start + (end - start) * t

def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, -1, 0.0, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.6, 0.6, 0.6, 1.0])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam()
    scene.draw_skybox()
    scene.draw_ground()
    scene.draw_walls()
    scene.draw_guardhouse()   # Guarita após o muro para não ser sobreposta
    scene.draw_building()
    scene.draw_garage()
    scene.draw_leisure_area()

    player.draw()

    player.draw()

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / float(h), 1.0, 200.0)

def keyboard(key, x, y):
    if key == b'\x1b':
        glutLeaveMainLoop()
    elif key == b'w':
        player.move_forward(collision_boxes)
    elif key == b's':
        player.move_backward(collision_boxes)
    elif key == b'a':
        player.rotate_left()
    elif key == b'd':
        player.rotate_right()
    elif key == b'c':
        global modo_camera
        modo_camera = (modo_camera + 1) % 3

def cam():
    if modo_camera == 0:
        d = 1.0
        h = 2
        rad = math.radians(player.rot)
        cam_x = player.x - math.sin(rad) * d
        cam_z = player.z - math.cos(rad) * d
        cam_y = h
        look_x = player.x + math.sin(rad)
        look_z = player.z + math.cos(rad)
        look_y = h * 0.7
        target = [cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0]
    else:
        target = posicoes_camera[modo_camera]

    if camera_state.target_cam_pos != target:
        camera_state.start_cam_pos = camera_state.current_cam_pos or target
        camera_state.target_cam_pos = target
        camera_state.transition_start_time = time.time()
        camera_state.is_transitioning = True

    if camera_state.is_transitioning:
        t = min((time.time() - camera_state.transition_start_time) / camera_state.transition_duration, 1)
        t_ease = t * t * (3 - 2 * t)
        cam_pos = [
            lerp(camera_state.start_cam_pos[i], camera_state.target_cam_pos[i], t_ease)
            for i in range(9)
        ]
        if t >= 1:
            camera_state.is_transitioning = False
        camera_state.current_cam_pos = cam_pos
    else:
        cam_pos = camera_state.target_cam_pos

    gluLookAt(*cam_pos[:3], *cam_pos[3:6], *cam_pos[6:9])

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Dia Ensolarado")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
