from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class Player:
    def __init__(self):
        self.x = 10    # Posição X inicial
        self.y = 0.0      # Altura base do jogador
        self.z = -10      # Posição Z inicial  
        self.rot = 10   # Rotação inicial (0° = olhando para -Z)
        self.move_speed = 0.1
        self.rot_speed = 5.0
        self.camera_mode = 0  # Modo de câmera

    def draw(self):
        """Renderiza o jogador na cena"""
        glPushMatrix()
        glTranslatef(self.x, self.y + 0.5, self.z)  # Ajuste para centralizar
        glRotatef(self.rot, 0, 1, 0)  # Rotação no eixo Y
        
        # Corpo (cubo)
        glColor3f(0.0, 0.0, 1.0)  # Azul
        glutSolidCube(1.0)
        
        # Olhos (indicam direção frontal)
        glColor3f(1.0, 1.0, 1.0)  # Branco
        glPushMatrix()
        glTranslatef(-0.2, 0.2, 0.51)
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.2, 0.2, 0.51)
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()
        
        glPopMatrix()

    def move_forward(self):
        """Move na direção atual da visão"""
        rad = math.radians(self.rot)
        self.x += math.sin(rad) * self.move_speed
        self.z += math.cos(rad) * self.move_speed
        
   


    def move_backward(self):
        """Move na direção oposta à visão"""
        rad = math.radians(self.rot)
        self.x -= math.sin(rad) * self.move_speed
        self.z -= math.cos(rad) * self.move_speed
        
   
    def rotate_left(self):
        """Gira para esquerda (anti-horário)"""
        self.rot = (self.rot + self.rot_speed) % 360

    def rotate_right(self):
        """Gira para direita (horário)"""
        self.rot = (self.rot - self.rot_speed) % 360

    def keyboard(self, key):
        """Processa entradas do teclado"""
        if key == b'\x1b':  # ESC
            glutLeaveMainLoop()
        elif key == b'w':
            self.move_forward()
        elif key == b's':
            self.move_backward()
        elif key == b'a':
            self.rotate_left()
        elif key == b'd':
            self.rotate_right()
        elif key == b'c':
            self.camera_mode = (self.camera_mode + 1) % 3
            print(f"Modo câmera: {['Dinâmica', 'Fixa 1', 'Fixa 2'][self.camera_mode]}")