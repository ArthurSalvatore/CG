from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Player:
    def __init__(self):
        self.x = 10
        self.y = 0.0
        self.z = -10
        self.rot = 10
        self.move_speed = 1.05
        self.rot_speed = 5.0
        self.camera_mode = 0
        self.collision_radius = 0.6  # Raio de colisão circular

    def draw(self):
        """Renderiza o jogador na cena"""
        glPushMatrix()
        glTranslatef(self.x, self.y + 0.5, self.z)
        glRotatef(self.rot, 0, 1, 0)
        
        glColor3f(0.0, 0.0, 1.0)
        glutSolidCube(1.0)
        
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(-0.2, 0.2, 0.51)
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.2, 0.2, 0.51)
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()
        
        glPopMatrix()

    def check_collision(self, x, z, collision_objects):
        """Nova verificação de colisão com sistema circular"""
        for obj in collision_objects:
            obj_type = obj['type']
            
            if obj_type == 'rectangle':
                # Verificação retangular
                x_min, x_max, z_min, z_max = obj['coords']
                closest_x = max(x_min, min(x, x_max))
                closest_z = max(z_min, min(z, z_max))
                
                distance = math.sqrt((x - closest_x)**2 + (z - closest_z)**2)
                
                if distance < self.collision_radius:
                    return True
                    
            elif obj_type == 'circle':
                # Verificação circular
                cx, cz, radius = obj['coords']
                distance = math.sqrt((x - cx)**2 + (z - cz)**2)
                
                if distance < (self.collision_radius + radius):
                    return True
        
        return False

    def move_forward(self, collision_objects):
        rad = math.radians(self.rot)
        new_x = self.x + math.sin(rad) * self.move_speed
        new_z = self.z + math.cos(rad) * self.move_speed
        
        if not self.check_collision(new_x, new_z, collision_objects):
            self.x = new_x
            self.z = new_z
        else:
            # Tentativa de deslize ao longo do obstáculo
            if not self.check_collision(new_x, self.z, collision_objects):
                self.x = new_x
            elif not self.check_collision(self.x, new_z, collision_objects):
                self.z = new_z

    def move_backward(self, collision_objects):
        rad = math.radians(self.rot)
        new_x = self.x - math.sin(rad) * self.move_speed
        new_z = self.z - math.cos(rad) * self.move_speed
        
        if not self.check_collision(new_x, new_z, collision_objects):
            self.x = new_x
            self.z = new_z
        else:
            if not self.check_collision(new_x, self.z, collision_objects):
                self.x = new_x
            elif not self.check_collision(self.x, new_z, collision_objects):
                self.z = new_z

    def rotate_left(self):
        self.rot = (self.rot + self.rot_speed) % 360

    def rotate_right(self):
        self.rot = (self.rot - self.rot_speed) % 360

    def keyboard(self, key, collision_objects):
        if key == b'\x1b':
            glutLeaveMainLoop()
        elif key == b'w':
            self.move_forward(collision_objects)
        elif key == b's':
            self.move_backward(collision_objects)
        elif key == b'a':
            self.rotate_left()
        elif key == b'd':
            self.rotate_right()
        elif key == b'c':
            self.camera_mode = (self.camera_mode + 1) % 3