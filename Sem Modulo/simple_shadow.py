# simple_shadows.py - Sistema de sombras simplificado usando stencil buffer

from OpenGL.GL import *
from OpenGL.GLU import *
import math
from OpenGL.GLUT import glutSwapBuffers

class SimpleShadowSystem:
    def __init__(self):
        self.light_pos = [50.0, 100.0, 50.0]
        self.ground_level = 0.0
        self.shadow_alpha = 0.4  # Transparência das sombras
        
    def calculate_shadow_matrix(self, light_pos, ground_plane):
        """Calcula matriz de projeção de sombra no chão"""
        lx, ly, lz = light_pos
        a, b, c, d = ground_plane  # ax + by + cz + d = 0
        
        # Produto escalar: light . normal + d
        dot = a * lx + b * ly + c * lz + d
        
        # Matriz de projeção planar
        shadow_matrix = [
            [dot - a * lx, -a * ly,     -a * lz,     -a * d],
            [-b * lx,      dot - b * ly, -b * lz,     -b * d],
            [-c * lx,      -c * ly,      dot - c * lz, -c * d],
            [-lx,          -ly,          -lz,          dot - d]
        ]
        
        return shadow_matrix
    
    def draw_planar_shadows(self, render_objects_func):
        """Desenha sombras projetadas no chão usando stencil buffer"""
        
        # Define plano do chão (y = 0)
        ground_plane = [0.0, 1.0, 0.0, 0.0]  # normal (0,1,0), d = 0
        
        # Calcula matriz de sombra
        shadow_matrix = self.calculate_shadow_matrix(self.light_pos, ground_plane)
        
        # ===== PASSO 1: MARCAR ÁREA DO CHÃO NO STENCIL =====
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 1, 0xFFFFFFFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        
        # Desabilita escrita de cor e profundidade temporariamente
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        glDepthMask(GL_FALSE)
        
        # Desenha o chão no stencil buffer
        self.draw_ground_plane()
        
        # Reabilita escrita de cor e profundidade
        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glDepthMask(GL_TRUE)
        
        # ===== PASSO 2: DESENHAR SOMBRAS APENAS NO CHÃO =====
        glStencilFunc(GL_EQUAL, 1, 0xFFFFFFFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
        
        # Configurações para sombras
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Cor da sombra (cinza escuro transparente)
        glColor4f(0.0, 0.0, 0.0, self.shadow_alpha)
        
        # Aplica matriz de projeção de sombra
        glPushMatrix()
        glMultMatrixf(self.flatten_matrix(shadow_matrix))
        
        # Desenha objetos como sombras
        render_objects_func(shadow_mode=True)
        
        glPopMatrix()
        
        # ===== RESTAURAR CONFIGURAÇÕES =====
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glDisable(GL_STENCIL_TEST)
        glColor3f(1.0, 1.0, 1.0)
    
    def draw_ground_plane(self):
        """Desenha o plano do chão para marcar no stencil"""
        size = 70
        glBegin(GL_QUADS)
        glVertex3f(-size, self.ground_level, -size)
        glVertex3f(size, self.ground_level, -size)
        glVertex3f(size, self.ground_level, size)
        glVertex3f(-size, self.ground_level, size)
        glEnd()
    
    def flatten_matrix(self, matrix):
        """Converte matriz 4x4 para formato OpenGL (coluna-major)"""
        flat = []
        for col in range(4):
            for row in range(4):
                flat.append(matrix[row][col])
        return flat
    
    def draw_shadow_volumes(self, objects):
        """Método alternativo usando shadow volumes (mais complexo)"""
        # Implementação futura se necessário
        pass

# Função para renderizar objetos que fazem sombra
def render_shadow_casters(scene, player, shadow_mode=False):
    """Renderiza apenas objetos que devem projetar sombras"""
    
    if shadow_mode:
        # No modo sombra, renderiza formas simplificadas
        glDisable(GL_TEXTURE_2D)
    
    # Prédio principal
    glPushMatrix()
    glTranslatef(-5, 15, 30)
    glScalef(40, 30, 20)
    render_simple_building_shadow()
    glPopMatrix()
    
    # Árvores (versão simplificada para sombras)
    if shadow_mode:
        render_tree_shadows(scene)
    
    # Player
    glPushMatrix()
    glTranslatef(player.x, player.y + 0.5, player.z)
    glRotatef(player.rot, 0, 1, 0)
    if shadow_mode:
        render_simple_cube_shadow(1.0)
    glPopMatrix()
    
    # Veículos
    render_vehicle_shadows(shadow_mode)

def render_simple_building_shadow():
    """Renderiza cubo simples para sombra do prédio"""
    glBegin(GL_QUADS)
    # Apenas faces superiores e laterais (que projetam sombra significativa)
    
    # Face superior
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    
    # Faces laterais
    # Frente
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    
    # Direita
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    
    # Esquerda
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    
    # Traseira
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    
    glEnd()

def render_simple_cube_shadow(size):
    """Renderiza cubo simples para sombras"""
    s = size / 2.0
    glBegin(GL_QUADS)
    
    # 6 faces do cubo
    faces = [
        # Frente
        [[-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]],
        # Traseira
        [[s, -s, -s], [-s, -s, -s], [-s, s, -s], [s, s, -s]],
        # Esquerda
        [[-s, -s, -s], [-s, -s, s], [-s, s, s], [-s, s, -s]],
        # Direita
        [[s, -s, s], [s, -s, -s], [s, s, -s], [s, s, s]],
        # Superior
        [[-s, s, s], [s, s, s], [s, s, -s], [-s, s, -s]],
        # Inferior
        [[-s, -s, -s], [s, -s, -s], [s, -s, s], [-s, -s, s]]
    ]
    
    for face in faces:
        for vertex in face:
            glVertex3f(*vertex)
    
    glEnd()

def render_tree_shadows(scene):
    """Renderiza sombras simplificadas das árvores"""
    for i, arvore in enumerate(scene.LIST_TREES):
        glPushMatrix()
        glTranslatef(arvore.position[0], arvore.position[1] + 2, arvore.position[2])
        glScalef(2, 4, 2)  # Forma simplificada da árvore
        render_simple_cube_shadow(1.0)
        glPopMatrix()

def render_vehicle_shadows(shadow_mode):
    """Renderiza sombras dos veículos"""
    if not shadow_mode:
        return
        
    # Posições dos carros (baseado no código original)
    vaga_inicial = -30
    espacamento = 5
    
    for i in range(5):
        x = vaga_inicial + i * espacamento
        glPushMatrix()
        glTranslatef(x, 1.0, 12.5)  # Posição dos carros
        
        # Carroceria simplificada
        glScalef(2, 0.6, 4)
        render_simple_cube_shadow(1.0)
        
        glPopMatrix()

# Instância global do sistema simples
simple_shadow_system = SimpleShadowSystem()

# Função para integrar no main.py (versão simplificada)
def render_scene_with_simple_shadows(scene, player):
    """Renderiza cena com sombras simples"""
    
    # Renderiza cena normal primeiro
    scene.draw_ground()
    scene.draw_walls()
    scene.draw_gate()
    scene.draw_guardhouse()  
    scene.draw_building()
    scene.draw_garage()
    scene.draw_leisure_area()
    
    # Árvores
    for arvore in scene.LIST_TREES:
        arvore.draw()
    
    player.draw()
    
    # Depois adiciona as sombras
    simple_shadow_system.draw_planar_shadows(lambda shadow_mode: render_shadow_casters(scene, player, shadow_mode))

# Função display() alternativa usando sombras simples
def display_with_simple_shadows(cam, scene, player, collision_objects):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam()
    
    # Skybox sem iluminação
    glDisable(GL_LIGHTING)
    scene.draw_skybox()
    glEnable(GL_LIGHTING)
    
    # Cena com sombras simples
    render_scene_with_simple_shadows(scene, player)
    
    # Debug
    glDisable(GL_LIGHTING)
    scene.draw_collision_debug(player, collision_objects)
    glEnable(GL_LIGHTING)
    
    glutSwapBuffers()

# Para usar o sistema simples, modifique glutInitDisplayMode() para incluir stencil:
# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_STENCIL | GLUT_MULTISAMPLE)