from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import camera
import time 
import player
import math
import scene

# Inicializa o player
player = player.Player()

# Configurações iniciais
camera_state = camera.CameraState()
modo_camera = 0  # 0 = dinâmica, 1 = fixa 1, 2 = fixa 2

# Posições das câmeras fixas (posição, alvo, vetor up)
posicoes_camera = [
    # Câmera dinâmica (será calculada em tempo real)
    None,
    
    # Câmera fixa 1
    [5, 3, 5,  0, 0, 0,  0, 1, 0],
    
    # Câmera fixa 2
    [-5, 2, -5,  0, 0, 0,  0, 1, 0]
]

# Configurações da janela
window_width = 1080
window_height = 1920

def init():
    """Configurações iniciais do OpenGL"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
    glEnable(GL_DEPTH_TEST)          # Habilita profundidade

def draw_ground():
    """Desenha o chão da garagem"""
    glColor3f(0.5, 0.5, 0.5)  # Cinza
    glBegin(GL_QUADS)
    glVertex3f(-50, -0.01, -50)
    glVertex3f(-50, -0.01, 50)
    glVertex3f(50, -0.01, 50)
    glVertex3f(50, -0.01, -50)

    glEnd()


def display():
    """Renderiza a cena"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Configura a câmera
    cam()

    draw_ground() 
    scene.draw_building()  # Desenhando o prédio
    #scene.draw_corridor()  # Desenhando o corredor
    scene.draw_garage()    # Desenhando a garagem
    scene.draw_leisure_area()  # Desenhando a área de lazer
    player.draw()
    scene.draw_vehicles()


    glutSwapBuffers()

def reshape(width, height):
    """Função chamada ao redimensionar a janela"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height), 0.1, 100.0)

def lerp(start, end, t):
    """Interpolação linear entre dois valores"""
    return start + (end - start) * t

def keyboard(key, x, y):
    """Callback do teclado"""
    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()
    elif key == b'w':
        player.move_forward()
    elif key == b's':
        player.move_backward()
    elif key == b'a':
        player.rotate_left()
    elif key == b'd':
        player.rotate_right()
    elif key == b'c':  # Tecla para alternar câmeras
        global modo_camera
        modo_camera = (modo_camera + 1) % 3
        print(f"Modo câmera: {['Dinâmica', 'Fixa 1', 'Fixa 2'][modo_camera]}")

def cam():
    global modo_camera
    
    # Calcular posição da câmera dinâmica (terceira pessoa)      
    if modo_camera == 0:
        distancia = 3  # Distância atrás do jogador
        altura = 2  # Altura da câmera
        
        # Converter ângulo para radianos
        rot_rad = math.radians(player.rot)
        
        # Calcular posição atrás do jogador
        cam_x = player.x - math.sin(rot_rad) * distancia
        cam_z = player.z - math.cos(rot_rad) * distancia
        cam_y = altura
        
        # Posição alvo (ligeiramente à frente do jogador)
        look_x = player.x + math.sin(rot_rad) * 1
        look_z = player.z + math.cos(rot_rad) * 1
        look_y = altura * 0.7
        
        target_cam_pos = [cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0]
    else:
        target_cam_pos = posicoes_camera[modo_camera]
    
    # Iniciar nova transição se a câmera mudar
    if camera_state.target_cam_pos != target_cam_pos:
        camera_state.start_cam_pos = camera_state.current_cam_pos or target_cam_pos
        camera_state.target_cam_pos = target_cam_pos
        camera_state.transition_start_time = time.time()
        camera_state.is_transitioning = True

    # Calcular progresso da animação
    if camera_state.is_transitioning:
        elapsed = time.time() - camera_state.transition_start_time
        t = min(elapsed / camera_state.transition_duration, 1.0)
        
        # Suavização (ease in-out)
        t_ease = t * t * (3 - 2 * t)
        
        # Interpolar todos os componentes da câmera
        cam_pos = [
            lerp(camera_state.start_cam_pos[i], camera_state.target_cam_pos[i], t_ease)
            for i in range(9)
        ]
        
        if t >= 1.0:
            camera_state.is_transitioning = False
        camera_state.current_cam_pos = cam_pos
    else:
        cam_pos = camera_state.target_cam_pos

    # Aplicar a visualização da câmera
    gluLookAt(
        cam_pos[0], cam_pos[1], cam_pos[2],  # Posição da câmera
        cam_pos[3], cam_pos[4], cam_pos[5],  # Ponto de interesse
        cam_pos[6], cam_pos[7], cam_pos[8]   # Vetor "up"
    )





def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Garagem - OpenGL")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()