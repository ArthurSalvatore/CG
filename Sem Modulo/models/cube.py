from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

class Cube:
    """
    Representa um cubo com transformações, textura opcional e colisão básica na base.

    collision_shape: 'box' para colisão retangular ou 'sphere' para colisão esférica.
    """
    def __init__(self, position, scale=(1,1,1), rotation=(0,0,0), texture=None, collision_shape='box'):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.texture = texture
        self.collision_shape = collision_shape

    def draw(self):
        glPushMatrix()
        # Transformações: translação, rotação e escala
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

        # Ativar textura ou cor padrão
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.8, 0.8, 0.8)

        glutSolidCube(1.0)

        if self.texture:
            glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def get_base_aabb(self):
        """Retorna tupla (min_x, max_x, min_z, max_z) do AABB na base do cubo."""
        x, y, z = self.position
        sx, sy, sz = self.scale
        half_x = sx / 2.0
        half_z = sz / 2.0
        return (x - half_x, x + half_x, z - half_z, z + half_z)

    def aabb_collision(self, point):
        """Verifica colisão com ponto (px, pz) na base usando AABB."""
        px, pz = point
        min_x, max_x, min_z, max_z = self.get_base_aabb()
        return (min_x <= px <= max_x) and (min_z <= pz <= max_z)

    def get_base_sphere(self):
        """Retorna tupla (cx, cz, radius) da colisão esférica na base."""
        x, y, z = self.position
        sx, sy, sz = self.scale
        radius = max(sx, sz) / 2.0
        return (x, z, radius)

    def sphere_collision(self, point):
        """Verifica colisão com ponto (px, pz) na base usando esfera."""
        px, pz = point
        cx, cz, r = self.get_base_sphere()
        return (px - cx)**2 + (pz - cz)**2 <= r*r

    def collides(self, point):
        """
        Checa colisão básica na base contra ponto (px, pz).
        Retorna True se colisão ocorrer.
        """
        if self.collision_shape == 'box':
            return self.aabb_collision(point)
        else:
            return self.sphere_collision(point)
        



