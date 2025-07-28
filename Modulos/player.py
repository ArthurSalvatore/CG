from OpenGL.GL import *
from OpenGL.GLUT import *
import math


class Player:
    def __init__(self):
        self.position = [10.0, -1.5, -10.0]
        self.rotation = 10.0
        self.speed = 0.2
        self.rotation_speed = 3.0
        self.collision_radius = 0.5
        self.walk_phase = 0.1
        self.camera_mode = 0
        
        self.keys_pressed = set()
        
        self.walls = [] 
        self.spheres = []  
        self.complexes =[]
        
    def set_walls(self, walls):
        self.walls = walls
    
    def set_spheres(self, spheres):
        self.spheres = []
        for obj in spheres:
            pos = obj.position
            scale = obj.scale
            radius = max(scale) * 1 
            self.spheres.append({'pos': pos, 'radius': radius})
    
    def set_complexes(self, complexes):
        self.complexes = complexes
    

    def key_down(self, key):
        
        self.keys_pressed.add(key)

    def key_up(self, key):
        
        self.keys_pressed.discard(key)

    def update(self):
        
        if b'w' in self.keys_pressed:
            self.move_forward()
        if b's' in self.keys_pressed:
            self.move_backward()
        if b'a' in self.keys_pressed:
            self.rotate_left()
        if b'd' in self.keys_pressed:
            self.rotate_right()

    def move_forward(self):
       
        rad = math.radians(self.rotation)
        new_x = self.position[0] + math.sin(rad) * self.speed
        new_z = self.position[2] + math.cos(rad) * self.speed
        new_pos = [new_x, self.position[1], new_z]
        
        if not self.check_collision(new_pos):
            self.position = new_pos
            self.walk_phase += 0.2  # animação de caminhada
    
    def move_backward(self):
        
        rad = math.radians(self.rotation)
        new_x = self.position[0] - math.sin(rad) * self.speed
        new_z = self.position[2] - math.cos(rad) * self.speed
        new_pos = [new_x, self.position[1], new_z]
        
        if not self.check_collision(new_pos):
            self.position = new_pos
            self.walk_phase += 0.2  # animação de caminhada

    def rotate_left(self):
        
        self.rotation = (self.rotation + self.rotation_speed) % 360
    
    def rotate_right(self):
        
        self.rotation = (self.rotation - self.rotation_speed) % 360

    def check_collision(self, new_pos):
        player_x, player_y, player_z = new_pos
        
        # Colisão com paredes (AABB)
        for wall in self.walls:
            wall_pos = wall.base_fragment.position
            wall_scale = wall.base_fragment.scale
            min_x = wall_pos[0] - wall_scale[0] / 2
            max_x = wall_pos[0] + wall_scale[0] / 2
            min_z = wall_pos[2] - wall_scale[2] / 2
            max_z = wall_pos[2] + wall_scale[2] / 2
            closest_x = max(min_x, min(player_x, max_x))
            closest_z = max(min_z, min(player_z, max_z))
            dist_x = player_x - closest_x
            dist_z = player_z - closest_z
            distance_squared = dist_x * dist_x + dist_z * dist_z
            if distance_squared < (self.collision_radius * self.collision_radius):
                return True

        # colisão com complexos
        for complex in self.complexes:
            collision_fragments = complex.get_collision_fragments()
            for frag in collision_fragments:
                frag_pos = frag.position
                frag_scale = frag.scale
                min_x = frag_pos[0] - frag_scale[0] / 2
                max_x = frag_pos[0] + frag_scale[0] / 2
                min_z = frag_pos[2] - frag_scale[2] / 2
                max_z = frag_pos[2] + frag_scale[2] / 2
                closest_x = max(min_x, min(player_x, max_x))
                closest_z = max(min_z, min(player_z, max_z))
                dist_x = player_x - closest_x
                dist_z = player_z - closest_z
                distance_squared = dist_x * dist_x + dist_z * dist_z
                if distance_squared < (self.collision_radius * self.collision_radius):
                    return True


        # Colisão com esferas 
        for sphere in self.spheres:
            sx, sy, sz = sphere['pos']
            radius = sphere['radius']
            dist2 = (player_x - sx) ** 2 + (player_z - sz) ** 2
            if dist2 < (self.collision_radius + radius) ** 2:
                return True
        
 
        
        return False
    
    def draw(self, SHOW_COLLISION_DEBUG, current_mode):
        glPushMatrix()
        
        # bobbing (leve sobe e desce ao andar)
        bob_offset = math.sin(self.walk_phase) * 0.05
        glTranslatef(self.position[0], self.position[1] + 1 + bob_offset, self.position[2])
        glRotatef(self.rotation, 0, 1, 0)

        # Torso aumentado
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(0,0.5,0)
        glScalef(0.7, 1, 0.4)   
        glutSolidCube(1.0)
        glPopMatrix()

        # Head (cabeça)
        if current_mode != 0:
            glPushMatrix()
            glColor3f(1.0, 0.8, 0.6)  
            glTranslatef(0.0, 1.4, 0.0)
            glutSolidSphere(0.3, 16, 16)
            glPopMatrix()

        # Arms (braços)
        glColor3f(0.0, 0.0, 1.0)
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(side * 0.55, 1.0, 0.0)
            glRotatef(90, 0, 0, 1)
            glutSolidCylinder(0.08, 0.8, 12, 4)
            glPopMatrix()

        # Legs (pernas)
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(side * 0.25, 0.5, 0.0)
            glRotatef(90, 1, 0, 0)
            glutSolidCylinder(0.1, 1.0, 12, 4)
            glPopMatrix()

        # Debug: desenha collider do player
        if SHOW_COLLISION_DEBUG:
            # Esfera do player
            glColor3f(0.0, 1.0, 0.0)
            glutWireSphere(self.collision_radius, 16, 16)
            
        glPopMatrix()
        
        # Debug: desenha colisores 
        if SHOW_COLLISION_DEBUG:
            # Quadrados das paredes

            for wall in self.walls:

                wall_pos = wall.base_fragment.position
                wall_scale = wall.base_fragment.scale
                glPushMatrix()
                glTranslatef(wall_pos[0], wall_pos[1], wall_pos[2])
                glColor3f(1.0, 0.0, 0.0)
                glScalef(wall_scale[0], 0.1, wall_scale[2])
                glutWireCube(1.0)
                glPopMatrix()
            
            # Esferas das árvores
            for sphere in self.spheres:
                sx, sy, sz = sphere['pos']
                radius = sphere['radius']
                glPushMatrix()
                glTranslatef(sx, sy, sz)
                glColor3f(0.0, 1.0, 0.0)
                glutWireSphere(radius, 16, 16)
                glPopMatrix()
            
            # Colisores complexos
            for complex in self.complexes:
                collision_fragments = complex.get_collision_fragments()
                for frag in collision_fragments:
                    frag_pos = frag.position
                    frag_scale = frag.scale
                    glPushMatrix()
                    glTranslatef(frag_pos[0], frag_pos[1], frag_pos[2])
                    glColor3f(1.0, 1.0, 0.0)  # Amarelo para portões
                    glScalef(frag_scale[0], frag_scale[1], frag_scale[2])
                    glutWireCube(1.0)
                    glPopMatrix()
            
