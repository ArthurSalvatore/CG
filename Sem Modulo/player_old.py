from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Player:
    def __init__(self):
        self.x = 10.0
        self.y = 0.0
        self.z = 10.0
        self.rot = 180.0
        self.move_speed = 0.2   # movimento mais suave
        self.rot_speed = 3    # rotação mais suave
        self.camera_mode = 0
        self.collision_radius = 0.5
        self.walk_phase =  0.1  # fase para animação de caminhada
        # Controle de teclas para movimento e rotação simultâneos
        self.keys_pressed = set()

    def draw(self):
        """Renderiza o jogador com aparência humanoide e animação de caminhar"""
        glPushMatrix()
        # bobbing (leve sobe e desce ao andar)
        bob_offset = math.sin(self.walk_phase) * 0.05
        glTranslatef(self.x, self.y + 0.5 + bob_offset, self.z)
        glRotatef(self.rot, 0, 1, 0)

        # Torso aumentado
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glScalef(0.7, 2, 0.4)   # largura, altura e profundidade
        glutSolidCube(1.0)
        glPopMatrix()

        # Head
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.6)
        glTranslatef(0.0, 1.4, 0.0)
        glutSolidSphere(0.3, 16, 16)
        glPopMatrix()

        # Arms
        glColor3f(0.0, 0.0, 1.0)
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(side * 0.55, 1.0, 0.0)
            glRotatef(90, 0, 0, 1)
            glutSolidCylinder(0.08, 0.8, 12, 4)
            glPopMatrix()

        # Legs
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(side * 0.25, 0.0, 0.0)
            glRotatef(90, 1, 0, 0)
            glutSolidCylinder(0.1, 1.0, 12, 4)
            glPopMatrix()

        glPopMatrix()

    def key_down(self, key):
        self.keys_pressed.add(key)

    def key_up(self, key):
        self.keys_pressed.discard(key)

    def update(self, collision_objects):
        """Chamar a cada frame antes do draw para processar movimento/rotação simultâneos"""
        if b'w' in self.keys_pressed:
            self.move_forward(collision_objects)
        if b's' in self.keys_pressed:
            self.move_backward(collision_objects)
        if b'a' in self.keys_pressed:
            self.rotate_left()
        if b'd' in self.keys_pressed:
            self.rotate_right()

    def check_collision(self, x, z, collision_objects):
        from math import sqrt
        for obj in collision_objects:
            if obj['type'] == 'rectangle':
                x_min, x_max, z_min, z_max = obj['coords']
                closest_x = max(x_min, min(x, x_max))
                closest_z = max(z_min, min(z, z_max))
                if sqrt((x - closest_x)**2 + (z - closest_z)**2) < self.collision_radius:
                    return True
            else:  # circle
                cx, cz, radius = obj['coords']
                if sqrt((x - cx)**2 + (z - cz)**2) < (self.collision_radius + radius):
                    return True
        return False

    def move_forward(self, collision_objects):
        rad = math.radians(self.rot)
        dx = math.sin(rad) * self.move_speed
        dz = math.cos(rad) * self.move_speed
        new_x = self.x + dx
        new_z = self.z + dz
        if not self.check_collision(new_x, new_z, collision_objects):
            self.x = new_x
            self.z = new_z
            self.walk_phase += 0.2

    def move_backward(self, collision_objects):
        rad = math.radians(self.rot)
        dx = -math.sin(rad) * self.move_speed
        dz = -math.cos(rad) * self.move_speed
        new_x = self.x + dx
        new_z = self.z + dz
        if not self.check_collision(new_x, new_z, collision_objects):
            self.x = new_x
            self.z = new_z
            self.walk_phase += 0.2

    def rotate_left(self):
        self.rot = (self.rot + self.rot_speed) % 360

    def rotate_right(self):
        self.rot = (self.rot - self.rot_speed) % 360

    def keyboard(self, key, x, y):
        # chamada para pressionar tecla
        if key == b'\x1b':  # ESC
            glutLeaveMainLoop()
        else:
            self.key_down(key)

    def keyboard_up(self, key, x, y):
        # chamada para soltar tecla
        self.key_up(key)
