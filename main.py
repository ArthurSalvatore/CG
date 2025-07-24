from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import camera as camera
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

collision_objects = [
    # Prédio principal
    {'type': 'rectangle', 'coords': (-25, 15, 20, 40)},
        
    # Muros externos
    {'type': 'rectangle', 'coords': (-70, -50, -50, 70)},
    {'type': 'rectangle', 'coords': (50, 70, -40, 70)},
    {'type': 'rectangle', 'coords': (-70, 70, -50, -65)},
    {'type': 'rectangle', 'coords': (-50, 50, 50, 50)},
    
    # Guarita
    {'type': 'rectangle', 'coords': (46, 50, 12, 16)},

    # Pilares do portão
    {'type': 'rectangle', 'coords': (49.5, 50.5, -10.5, -9.5)},  # Pilar esquerdo
    {'type': 'rectangle', 'coords': (49.5, 50.5, 9.5, 10.5)},    # Pilar direito
    # Árvores 
    *[{'type': 'circle', 'coords': (x, -25, 0.8)} for x in range(-25, 26, 5)],
    
    # Carros 
    *[{'type': 'rectangle', 'coords': (x-1.5, x+1.5, 10, 15)} for x in range(-30, -5, 5)],
    
    # Exceção 
    {'type': 'rectangle', 'coords': (0.8, 1.2, 1.8, 2.2), 'no_collide': True}
]
def lerp(start, end, t):
    return start + (end - start) * t


def keyboard(key, x, y):
    player.keyboard(key, collision_objects)


def init():
    scene.init_textures()  # Adicione esta linha antes de outras inicializações
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST) 
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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam()
    scene.draw_skybox()
    scene.draw_ground()
    scene.draw_walls()
    scene.draw_gate()
    scene.draw_guardhouse()  
    scene.draw_building()
    scene.draw_garage()
    scene.draw_leisure_area()



    player.draw()
    scene.draw_collision_debug(player, collision_objects)  # comente essa linha para desativar o debug
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
        player.move_forward(collision_objects)
    elif key == b's':
        player.move_backward(collision_objects)
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
