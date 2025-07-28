from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import camera as camera
import player_old as player_module
import scene_old
import math
import time
from simple_shadow import simple_shadow_system, display_with_simple_shadows
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18


player = player_module.Player()
camera_state = camera.CameraState()
modo_camera = 0

posicoes_camera = [
    None,
    [50, 40, 0, 0, 0, 0, 0, 1, 0],
    [-52, 30, -100, 0, 0, 0, 0, 1, 0]
]


show_door_msg = False
door_msg_time = 0    # Armazena timestamp de quando a mensagem foi acionada
DOOR_MSG_DURATION = 3000  # milissegundos (3 s)

show_car_msg = False
car_msg_time = 0    # Armazena timestamp de quando a mensagem foi acionada
CAR_MSG_DURATION = 3000  # milissegundos (3 s)


window_width = 1080
window_height = 1920

vaga_inicial = -25.0
espacamento  = 8.0
slot_w       = 4.0
slot_d       = 8.0
z_slot       = 13.0

# constantes
CAM_DISTANCE = 5.0
CAM_HEIGHT   = 2.0
TOPDOWN_HEIGHT = 100.0




collision_objects = [
    # Prédio principal
    {'type': 'rectangle', 'coords': (-40, 40, 20, 40)},
    # Muros externos
    {'type': 'rectangle', 'coords': (-70, -50, -50, 70)},
    {'type': 'rectangle', 'coords': (50, 70, -40, 70)},
    {'type': 'rectangle', 'coords': (-70, 70, -50, -65)},
    {'type': 'rectangle', 'coords': (-50, 50, 50, 50)},
    # Guarita
    {'type': 'rectangle', 'coords': (44, 48, 12, 16)},
    # Pilares retangulares da área de lazer (5 pilares)
    {'type': 'rectangle', 'coords': (-49.7, -49.3, -49.7, -49.3)},
    {'type': 'rectangle', 'coords': (-49.7, -49.3, -35.7, -35.3)},
    {'type': 'rectangle', 'coords': (-35.7, -35.3, -49.7, -49.3)},
    {'type': 'rectangle', 'coords': (-35.7, -35.3, -35.7, -35.3)},
    # Pilares do portão
    {'type': 'rectangle', 'coords': (49.5, 50.5, -10.5, -9.5)},
    {'type': 'rectangle', 'coords': (49.5, 50.5, 9.5, 10.5)},
    # Árvores 
    *[{'type': 'circle', 'coords': (x, -15, 0.8)} for x in range(-45, 40, 15)],
    # Carros 
    *[
        {
            'type': 'rectangle',
            'coords': (
                x - (slot_w * 0.9) / 2,
                x + (slot_w * 0.9) / 2,
                (z_slot - slot_d / 2) - (slot_d * 0.8) / 2,
                (z_slot - slot_d / 2) + (slot_d * 0.8) / 2
            )
        }
        for x in [vaga_inicial + i * espacamento for i in range(6)]
    ],
    # Exceção 
    {'type': 'rectangle', 'coords': (0.8, 1.2, 1.8, 2.2), 'no_collide': True}
]






def cam_first_person(player):
    rad = math.radians(player.rot)
    fx = math.sin(rad)
    fz = math.cos(rad)
    eye = (player.x, player.y + 1.2, player.z)
    center = (eye[0] + fx, eye[1], eye[2] + fz)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, 0,1,0)


def cam_third_person(player):
    rad = math.radians(player.rot)
    bx = math.sin(rad) * CAM_DISTANCE
    bz = math.cos(rad) * CAM_DISTANCE
    eye = (player.x - bx, player.y + CAM_HEIGHT, player.z - bz)
    center = (player.x, player.y + 1.0, player.z)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, 0,1,0)

def cam_top_down(player):
    eye = (player.x, player.y + TOPDOWN_HEIGHT, player.z)
    center = (player.x, player.y, player.z)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, 0,0,-1)

def cam_security(player):
    # posição fixa de "câmera de segurança"
    eye = (100.0, 60.0, -45.0)
    center = (0.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, 0,1,0)


def draw_text_centered(text, font=GLUT_BITMAP_HELVETICA_18):
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    pixel_width = sum(glutBitmapWidth(font, ord(c)) for c in text)
    x_px = (w - pixel_width) // 2
    y_px = h // 2

    # Configura projeção ortográfica em pixels
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Desliga depth/lighting pra garantir visibilidade
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glRasterPos2i(x_px, y_px)
    for c in text:
        glutBitmapCharacter(font, ord(c))

    # Restaura estados
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def on_key_down(key, x, y):
    global show_door_msg, door_msg_time
    global show_car_msg, car_msg_time

    player.key_down(key)

    # só dispara se estiver perto da porta
    if key in (b'f', b'F'):
        
        


        if is_near_door(player):
            show_door_msg = True
            door_msg_time = glutGet(GLUT_ELAPSED_TIME)
        elif is_near_car(player):
            show_car_msg = True
            car_msg_time = glutGet(GLUT_ELAPSED_TIME)



    # troca de câmera permanece igual
    elif key in (b'c', b'C'):
        player.camera_mode = (player.camera_mode + 1) % 4

def on_key_up(key, x, y):
    player.key_up(key)

def on_special_down(key, x, y):
    if key == GLUT_KEY_LEFT:
        player.key_down(b'a')
    elif key == GLUT_KEY_RIGHT:
        player.key_down(b'd')

def on_special_up(key, x, y):
    if key == GLUT_KEY_LEFT:
        player.key_up(b'a')
    elif key == GLUT_KEY_RIGHT:
        player.key_up(b'd')





DOOR_X_MIN, DOOR_X_MAX = 4.0, -4
DOOR_Z_CENTER = 18.0
DOOR_Z_RADIUS = 2




def debug_draw_door_area():
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   
    glColor4f(1.0, 0.0, 0.0, 0.3)

    z0 = DOOR_Z_CENTER - DOOR_Z_RADIUS
    z1 = DOOR_Z_CENTER + DOOR_Z_RADIUS
    y = 0.01  

    glBegin(GL_QUADS)
    glVertex3f(DOOR_X_MIN, y, z0)
    glVertex3f(DOOR_X_MAX, y, z0)
    glVertex3f(DOOR_X_MAX, y, z1)
    glVertex3f(DOOR_X_MIN, y, z1)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def is_near_door(player):
    
    return -4.0 <= player.x <= 4.0 and abs(player.z - 18.0) < 2




vaga_inicial = -25.0
espacamento  = 8.0
slot_w       = 4.0
slot_d       = 8.0
z_slot       = 13.0




def is_near_car(player):
   
    for i in range(6):
         
        x = vaga_inicial + i * espacamento
        x0 = x - (slot_w * 0.6) 
        x1 = x + (slot_w * 0.6) 
        zc = z_slot - slot_d 
        z0 = zc - (slot_d * - 0.2) 
        z1 = zc + (slot_d * 0.8) 
        if x0 <= player.x <= x1 and z0 <= player.z <= z1:
            return True
    return False


def debug_draw_car_area():
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0, 1, 0, 0.3)
    y = 0.01
    # seis vagas de carro
    for i in range(6):
        x = vaga_inicial + i * espacamento
        x0 = x - (slot_w * 0.6) 
        x1 = x + (slot_w * 0.6) 
        zc = z_slot - slot_d 
        z0 = zc - (slot_d * - 0.2) 
        z1 = zc + (slot_d * 0.8) 
        glBegin(GL_QUADS)
        glVertex3f(x0, y, z0)
        glVertex3f(x1, y, z0)
        glVertex3f(x1, y, z1)
        glVertex3f(x0, y, z1)
        glEnd()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)



def lerp(start, end, t):
    return start + (end - start) * t

def init():
    scene_old.init_textures()
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    # Ativando iluminação
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Luz principal (suave)
    glLightfv(GL_LIGHT0, GL_POSITION,  [50.0, 100.0,  50.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,   [0.10, 0.10, 0.10, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   [0.60, 0.60, 0.60, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR,  [0.30, 0.30, 0.30, 1.0])

    # Luz de preenchimento
    glLightfv(GL_LIGHT1, GL_POSITION,  [-30.0, 50.0, -30.0, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT,   [0.05, 0.05, 0.08, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,   [0.20, 0.20, 0.25, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR,  [0.10, 0.10, 0.10, 1.0])

    # Ambiente global
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.05, 0.05, 0.05, 1.0])

    # Material por cor
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

 



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Atualiza personagem
    player.update(collision_objects)

    # Seleciona câmera
    mode = player.camera_mode
    if   mode == 0: cam_first_person(player)
    elif mode == 1: cam_third_person(player)
    elif mode == 2: cam_top_down(player)
    else:           cam_security(player)

    # Desenha a cena
    glDisable(GL_LIGHTING)
    scene_old.draw_skybox()
    glEnable(GL_LIGHTING)

    scene_old.draw_ground()
    scene_old.draw_walls()
    scene_old.draw_gate()
    scene_old.draw_guardhouse()
    scene_old.draw_building()
    scene_old.draw_garage()
    scene_old.draw_leisure_area()
    for t in scene_old.LIST_TREES:
        t.draw()


    debug_draw_door_area()
    debug_draw_car_area()
    
    player.draw()



    
    glDisable(GL_LIGHTING)
    scene_old.draw_collision_debug(player, collision_objects)
    glEnable(GL_LIGHTING)

    #  Mensagem de Porta 
    global show_door_msg
    if show_door_msg:
        elapsed = glutGet(GLUT_ELAPSED_TIME) - door_msg_time
        if elapsed < DOOR_MSG_DURATION:
            draw_text_centered("Desculpe, está fechado")
        else:
            show_door_msg = False


  #  Mensagem de carro 
    global show_car_msg
    if show_car_msg:
        if glutGet(GLUT_ELAPSED_TIME) - car_msg_time < CAR_MSG_DURATION:
           draw_text_centered("Desde quando Universitario tem carro?")
        else:
            show_car_msg = False

    glutSwapBuffers()

def idle():
    glutPostRedisplay()



def reset_material():
    """Restaura material padrão"""
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)



def setup_tree_material():
    """Configura material específico para árvores"""
    glDisable(GL_COLOR_MATERIAL)
    # Material para madeira/vegetação
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1, 0.15, 0.08, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.3, 0.6, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.02, 0.05, 0.02, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 2.0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / float(h), 1.0, 2000.0)


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
        player.camera_mode = (player.camera_mode + 1) % 4

   
    if key == b'f' or key == b'F':
        global show_door_msg, door_msg_time  
        if is_near_door(player):
            show_door_msg = True
            door_msg_time = glutGet(GLUT_ELAPSED_TIME)



def cleanup():
    """Limpa recursos ao fechar o programa"""
    simple_shadow_system.cleanup()


def display_wrapper():
    def cam_wrapper():
        if player.camera_mode == 0:
            cam_first_person(player)
        elif player.camera_mode == 1:
            cam_third_person(player)
        elif player.camera_mode == 2:
            cam_top_down(player)
        elif player.camera_mode == 3:
            cam_security(player)
    display_with_simple_shadows(cam_wrapper, scene_old, player, collision_objects)



    


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH |  GLUT_STENCIL | GLUT_MULTISAMPLE)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Dia Ensolarado - CG 2025.1")

    # Inicializações da cena
    glEnable(GL_DEPTH_TEST)
    scene_old.init_textures()
    init()
    # Callbacks
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(on_key_down)
    glutKeyboardUpFunc(on_key_up)
    glutSpecialFunc(on_special_down)
    glutSpecialUpFunc(on_special_up)
    glutIgnoreKeyRepeat(True)

    glutMainLoop()

if __name__ == "__main__":
    main()