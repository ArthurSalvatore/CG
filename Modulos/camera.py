from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math

class Camera:
    def __init__(self):
        self.modes = [
            "first_person",    # 0 - Primeira pessoa
            "third_person",    # 1 - Terceira pessoa 
            "top_down",        # 2 - Vista de cima
            "security"         # 3 - Câmera de segurança fixa
        ]
        self.current_mode = 0

        
        self.position = [0, 2, 0]
        self.target = [0, 0, 0]
        self.up = [0, 1, 0]

        
        self.target_pos = [0, 2, 0]
        self.target_look = [0, 0, 0]

        # Transições suaves:

        # self.transition_time = 0.5
        # self.transition_start = 0

        
        # self.follow_speed = 4.0  

        self.CAM_DISTANCE = 5.0
        self.CAM_HEIGHT = 2.0
        self.TOPDOWN_HEIGHT = 70.0

    def toggle_mode(self):
        
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        self.transition_start = time.time()

    def cam_first_person(self, player):
        
        rad = math.radians(player.rotation)
        fx = math.sin(rad)
        fz = math.cos(rad)
        eye = (player.position[0], player.position[1] + 2.4, player.position[2])
        center = (eye[0] + fx, eye[1], eye[2] + fz)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*eye, *center, 0, 1, 0)

    def cam_third_person(self, player):
        
        rad = math.radians(player.rotation)
        bx = math.sin(rad) * self.CAM_DISTANCE
        bz = math.cos(rad) * self.CAM_DISTANCE
        eye = (player.position[0] - bx, player.position[1] + self.CAM_HEIGHT, player.position[2] - bz)
        center = (player.position[0], player.position[1] + 1.0, player.position[2])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*eye, *center, 0, 1, 0)

    def cam_top_down(self, player):
        
        eye = (player.position[0], player.position[1] + self.TOPDOWN_HEIGHT, player.position[2])
        center = (player.position[0], player.position[1], player.position[2])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*eye, *center, 0, 0, -1)

    def cam_security(self, player):
        
        eye = (100.0, 60.0, -45.0)
        center = (0.0, 0.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*eye, *center, 0, 1, 0)

    def update(self, player, delta_time):
        
        mode = self.current_mode
        
        # Aplica a câmera baseada no modo atual
        if mode == 0:
            self.cam_first_person(player)
        elif mode == 1:
            self.cam_third_person(player)
        elif mode == 2:
            self.cam_top_down(player)
        else:
            self.cam_security(player)

    @staticmethod
    def lerp(a, b, t):
        """Interpolação linear com clamp"""
        return a + (b - a) * max(0.0, min(1.0, t))