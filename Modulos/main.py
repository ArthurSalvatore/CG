from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from scene import SceneBuilder
from player import Player
from camera import Camera
import time
from lightning import configurar_luz
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

# Configurações
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 1920

# Instâncias globais
scene_builder = SceneBuilder()
player = Player()
camera = Camera()
last_time = time.time()
SHOW_COLLISION_DEBUG = False
gate = None

SHOW_INTERACTION_AREAS = False  
show_door_msg = False          
door_msg_time = 0               
DOOR_MSG_DURATION = 3000        
show_car_msg = False            
car_msg_time = 0                
CAR_MSG_DURATION = 3000         

def init():
    """Inicializa o OpenGL e a cena"""
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    # Luz ambiente alaranjada (GL_LIGHT0)
    configurar_luz(GL_LIGHT0, [0.0, 10.0, 0.0], [0.8, 0.5, 0.2], 1.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.8, 0.5, 0.2, 1.0])

    # Spot light (GL_LIGHT1)
    configurar_luz(GL_LIGHT1, [0.0, 10.0, 10.0], [1.0, 1.0, 0.8], 1.0)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0.0, -1.0, -1.0])
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 30.0)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 10.0)
    
    build_scene()

def build_scene():
    global gate

    # Skybox
    scene_builder.add_skybox(texture_path="textures/skybox.png", size=1000.0)
    
    # Muros externos
    # Direita
    wall1 = scene_builder.add_wall(pos=(-50, 1, 0), scale=(0.5, 5, 100), frag_qtd=100, uv_scale=(0.2, 0.2))
    # Esquerda (com abertura para o portão)
    wall2a = scene_builder.add_wall(pos=(50, -0.2, 30), scale=(0.5, 5, 40), frag_qtd=100, uv_scale=(0.2, 0.2))
    wall2b = scene_builder.add_wall(pos=(50, -0.2, -30), scale=(0.5, 5, 40), frag_qtd=100, uv_scale=(0.2, 0.2))
    # Trás
    wall3 = scene_builder.add_wall(pos=(0, 1, -50), scale=(100, 5, 0.5), frag_qtd=100, uv_scale=(0.2, 0.2))
    # Frente
    wall4 = scene_builder.add_wall(pos=(0, 1, 50), scale=(100, 5, 0.5), frag_qtd=100, uv_scale=(0.2, 0.2))
    
    # Portão no muro direito (onde há a abertura)
    gate = scene_builder.add_gate(pos=(50, -1.5, 0), gate_width=20, gate_height=5)

    # Prédio principal
    building_wall = scene_builder.add_wall(
        pos=(0, 10, 39), 
        scale=(80, 30, 20), 
        frag_qtd=100, 
        texture_path="textures/brick_wall_diffuse.jpg", 
        uv_scale=(0.25, 0.25)
    )

    # porta do prédio
    door = scene_builder.add_wall(
        pos=(0, 1.5, 29), 
        scale=(8, 5, 0.1), 
        frag_qtd=10, 
        texture_path="textures/wood.jpg", 
        uv_scale=(0.5, 0.5)
    )
    
    # Varandas
    for i in range(8):  
        varanda_x = -35 + i * 10  
        for floor_level in [1, 2, 3]:  
            varanda_y = -1 + floor_level * 6  
            scene_builder.add_balcony(
                pos=(varanda_x, varanda_y, 28.8),  
                width=5.0,
                height=1.0,
                depth=0.4
            )

    # Árvores
    arvores = []
    for i in range(-45, 40, 15):
        arvore = scene_builder.add_obj(
            obj_path="objs/Arboreobj.obj", 
            scale=(0.05, 0.05, 0.05), 
            pos=(i, -1, -15), 
            rotation=(-90, 0, 0)
        )
        arvores.append(arvore)

    # Garagem
    garage = scene_builder.add_garage(
        pos=(-40, -0.85, 24),
        garage_width=70.0,
        garage_depth=8.0,
        num_slots=8
    )

    # Guarita
    guardhouse = scene_builder.add_guardhouse(
        pos=(44, -0.85, 12),
        width=4.0,
        height=4.0,
        depth=4.0,
        texture_path="textures/brick_wall_diffuse.jpg"
    )

    # Área de lazer 
    leisure_area = scene_builder.add_leisure_area(
        pos=(-43, -1, -50),  
        area_width=15.0,
        area_depth=15.0,
        pillar_height=3.0
    )

    # Chão
    scene_builder.add_floor(pos=(0, -1, 0), scale=(100, 0.1, 100), frag_qtd=20)
    scene_builder.add_floor(pos=(0, 25.2, 39), scale=(80, 0.1, 20), frag_qtd=10)
    
    # Configurar colisões no player
    all_walls = [wall1, wall2a, wall2b, wall3, wall4, building_wall, door]
    player.set_spheres(arvores)
    player.set_walls(all_walls)
    player.set_complexes([gate, guardhouse, leisure_area, garage])

def is_near_door(player):
    door_pos = (0, 1.5, 29)
    door_scale = (8, 5, 0.1)
    
   
    if abs(player.position[2] - door_pos[2]) > 2:
        return False
        
    
    return (door_pos[0] - door_scale[0]/2 - 1 <= player.position[0] <= door_pos[0] + door_scale[0]/2 + 1)

def is_near_car(player):
    for garage in scene_builder.components['garages']:
        for vehicle in garage.vehicles:
            car_pos = vehicle.position
            car_scale = (vehicle.car_width, vehicle.car_height, vehicle.car_length)
            
            
            if (abs(player.position[0] - car_pos[0]) < car_scale[0] and \
               (abs(player.position[2] - car_pos[2]) < car_scale[2])):
                return True
    return False

def draw_interaction_areas():
    if not SHOW_INTERACTION_AREAS:
        return
        
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Área da porta
    door_pos = (0, 1.5, 29)
    door_scale = (8, 5, 0.1)
    
    glColor4f(1.0, 0.0, 0.0, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(door_pos[0] - door_scale[0]/2, -0.99, door_pos[2] - 2)
    glVertex3f(door_pos[0] + door_scale[0]/2, -0.99, door_pos[2] - 2)
    glVertex3f(door_pos[0] + door_scale[0]/2, -0.99, door_pos[2] + 2)
    glVertex3f(door_pos[0] - door_scale[0]/2, -0.99, door_pos[2] + 2)
    glEnd()
    
    # Áreas dos carros
    glColor4f(0.0, 1.0, 0.0, 0.3)
    for garage in scene_builder.components['garages']:
        for vehicle in garage.vehicles:
            car_pos = vehicle.position
            car_scale = (vehicle.car_width, vehicle.car_height, vehicle.car_length)
            
            glBegin(GL_QUADS)
            glVertex3f(car_pos[0] - car_scale[0]/2, -0.9, car_pos[2] - car_scale[2]/2)
            glVertex3f(car_pos[0] + car_scale[0]/2, -0.9, car_pos[2] - car_scale[2]/2)
            glVertex3f(car_pos[0] + car_scale[0]/2, -0.9, car_pos[2] + car_scale[2]/2)
            glVertex3f(car_pos[0] - car_scale[0]/2, -0.9, car_pos[2] + car_scale[2]/2)
            glEnd()
    
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def draw_text_centered(text, font=GLUT_BITMAP_HELVETICA_18):
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    
    pixel_width = sum(glutBitmapWidth(font, ord(c)) for c in text)
    x = (w - pixel_width) // 2
    y = h // 2
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2i(x, y)
    for c in text:
        glutBitmapCharacter(font, ord(c))
    
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    global last_time, show_door_msg, show_car_msg

    import math
    
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    player.update()

    # Configuração da luz spot
    player_pos = player.position
    player_rot = player.rotation  
    angle_rad = math.radians(player_rot)
    
    light_x = player_pos[0]
    light_y = player_pos[1] + 1.5  
    light_z = player_pos[2]
    
    dir_x = math.sin(angle_rad)
    dir_y = -0.2  
    dir_z = math.cos(angle_rad)
    
    glLightfv(GL_LIGHT1, GL_POSITION, [light_x, light_y, light_z, 1.0])
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [dir_x, dir_y, dir_z])
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 45.0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 15.0)

    camera.update(player, delta_time)
    scene_builder.update(delta_time)
    scene_builder.draw()
    player.draw(SHOW_COLLISION_DEBUG, camera.current_mode)
    
    draw_interaction_areas()
    

    # Desenha mensagens
    if show_door_msg:
        elapsed = glutGet(GLUT_ELAPSED_TIME) - door_msg_time
        if elapsed < DOOR_MSG_DURATION:
            draw_text_centered("Desculpe, está fechado")
        else:
            show_door_msg = False
    
    if show_car_msg:
        elapsed = glutGet(GLUT_ELAPSED_TIME) - car_msg_time
        if elapsed < CAR_MSG_DURATION:
            draw_text_centered("Desde quando Universitario tem carro?")
        else:
            show_car_msg = False
    
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / float(h), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

def on_key_down(key, x, y):
    global SHOW_COLLISION_DEBUG, gate, SHOW_INTERACTION_AREAS, show_car_msg, show_door_msg,door_msg_time,car_msg_time

    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()
    elif key in (b'c', b'C'):
        camera.toggle_mode()
        print(f"Modo de câmera: {camera.modes[camera.current_mode]}")
    elif key == b'v':
        SHOW_COLLISION_DEBUG = not SHOW_COLLISION_DEBUG
        SHOW_INTERACTION_AREAS = not SHOW_INTERACTION_AREAS
        print(f"Debug de colisão: {'ON' if SHOW_COLLISION_DEBUG else 'OFF'}")
    elif key == b'.':
        if gate:
            gate.toggle_gate()
            if gate.is_opening:
                status = "Abrindo"
            elif gate.is_closing:
                status = "Fechando"
            elif gate.gate_offset >= gate.max_opening - 0.1:
                status = "Aberto"
            elif gate.gate_offset <= 0.1:
                status = "Fechado"
            else:
                status = "Em movimento"
            print(f"Portão: {status} (offset: {gate.gate_offset:.2f})")
    elif key in (b'f', b'F'):
        near_door = is_near_door(player)
        near_car = is_near_car(player)
        
        if near_door and not near_car:
            show_door_msg = True
            door_msg_time = glutGet(GLUT_ELAPSED_TIME)
            print("Interagindo com a porta")
        elif near_car and not near_door:
            show_car_msg = True
            car_msg_time = glutGet(GLUT_ELAPSED_TIME)
            print("Interagindo com o carro")
    else:
        player.key_down(key)
    
    glutPostRedisplay()

#buffering de movimentação

def on_key_up(key, x, y):
    player.key_up(key)
    glutPostRedisplay()

def on_special_down(key, x, y):
    if key == GLUT_KEY_LEFT:
        player.key_down(b'a')
    elif key == GLUT_KEY_RIGHT:
        player.key_down(b'd')
    glutPostRedisplay()

def on_special_up(key, x, y):
    if key == GLUT_KEY_LEFT:
        player.key_up(b'a')
    elif key == GLUT_KEY_RIGHT:
        player.key_up(b'd')
    glutPostRedisplay()

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Dia Ensolarado - Movimento Suave")
    
    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(on_key_down)
    glutKeyboardUpFunc(on_key_up)
    glutSpecialFunc(on_special_down)
    glutSpecialUpFunc(on_special_up)
    glutIdleFunc(idle)
    
    glutIgnoreKeyRepeat(True)
    
    print("Controles:")
    print("WASD - Movimento e rotação")
    print("C - Alternar modo de câmera")
    print("V - Debug de colisão")
    print(". - Abrir/fechar portão")
    print("F - Interagir com objetos")
    print("ESC - Sair")
    
    glutMainLoop()

if __name__ == "__main__":
    main()