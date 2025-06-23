from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_ground():
    glColor3f(0.4, 0.4, 0.4)  # Cor do chão
    size = 70  # Aumentado ainda mais para cobrir toda a área visível
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(size, 0, -size)
    glVertex3f(size, 0, size)
    glVertex3f(-size, 0, size)
    glEnd()


def draw_building():
    glPushMatrix()
    glTranslatef(-25.0, 0.0, 20.0)  # Move o prédio mais para trás no cenário

    # Corpo principal do prédio
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    # Fundo
    glVertex3f(0, 0, 20)
    glVertex3f(40, 0, 20)
    glVertex3f(40, 30, 20)
    glVertex3f(0, 30, 20)

    # Lado esquerdo
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 20)
    glVertex3f(0, 30, 20)
    glVertex3f(0, 30, 0)

    # Lado direito
    glVertex3f(40, 0, 0)
    glVertex3f(40, 0, 20)
    glVertex3f(40, 30, 20)
    glVertex3f(40, 30, 0)

    # Topo
    glVertex3f(0, 30, 0)
    glVertex3f(40, 30, 0)
    glVertex3f(40, 30, 20)
    glVertex3f(0, 30, 20)
    glEnd()

    # Frente (desenhada atrás para portas/janelas aparecerem)
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(40, 0, 0)
    glVertex3f(40, 30, 0)
    glVertex3f(0, 30, 0)
    glEnd()

    # Porta — bem à frente
    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(18, 0, -0.1)
    glVertex3f(22, 0, -0.1)
    glVertex3f(22, 6, -0.1)
    glVertex3f(18, 6, -0.1)
    glEnd()

    # Janelas
    glColor3f(0.2, 0.5, 0.8)
    for row in range(3):
        for col in range(4):
            x0 = 5 + col * 8
            y0 = 10 + row * 6
            glBegin(GL_QUADS)
            glVertex3f(x0, y0, -0.1)
            glVertex3f(x0 + 4, y0, -0.1)
            glVertex3f(x0 + 4, y0 + 4, -0.1)
            glVertex3f(x0, y0 + 4, -0.1)
            glEnd()

    glPopMatrix()

def draw_garage():
    glPushMatrix()
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_QUADS)
    glVertex3f(-25, 0.01, -50)
    glVertex3f(25, 0.01, -50)
    glVertex3f(25, 0.01, 0)
    glVertex3f(-25, 0.01, 0)
    glEnd()
    
    # Vagas com e sem veículos
    glColor3f(0.2, 0.2, 0.2)
    vaga_inicial = -30
    espacamento = 5
    for i in range(10):  # Criando 8 vagas, 5 com carro e 3 sem carro
        x = vaga_inicial + i * espacamento
        glPushMatrix()
        glTranslatef(x, 0, 15)
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.02, 0)
        glVertex3f(1, 0.02, 0)
        glVertex3f(1, 0.02, -5)
        glVertex3f(-1, 0.02, -5)
        glEnd()
        glPopMatrix()
    
    # Árvores centralizadas na linha
    glColor3f(0.5, 1, 0.05)
    for x in range(-25, 26, 5):
        glPushMatrix()
        glTranslatef(x, 0, -25)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0, -0.5)
        glVertex3f(0.5, 0, -0.5)
        glVertex3f(0.5, 3, -0.5)
        glVertex3f(-0.5, 3, -0.5)
        glEnd()
        glPopMatrix()
    
    draw_vehicles_aligned(vaga_inicial, espacamento)
    glPopMatrix()

def draw_vehicles_aligned(vaga_inicial, espacamento):
    car_colors = [
        (1.0, 0.0, 0.0),  # Vermelho
        (0.0, 0.0, 1.0),  # Azul
        (1.0, 1.0, 0.0),  # Amarelo
        (0.0, 1.0, 0.0),  # Verde
        (1.0, 0.5, 0.0)   # Laranja
    ]
    for i in range(5):  # Somente 5 veículos
        x = vaga_inicial + i * espacamento
        r, g, b = car_colors[i % len(car_colors)]
        glPushMatrix()
        glTranslatef(x, 0.3, 12.5)
        
        # Carroceria
        glPushMatrix()
        glScalef(2, 0.6, 4)
        glColor3f(r, g, b)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Cabine
        glPushMatrix()
        glTranslatef(0, 0.4, 0)
        glScalef(1.2, 0.5, 2)
        glColor3f(r * 0.7, g * 0.7, b * 0.7)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Rodas
        glColor3f(0.1, 0.1, 0.1)
        wheel_positions = [
            (0.9, -0.2, 1.8),
            (-0.9, -0.2, 1.8),
            (0.9, -0.2, -1.8),
            (-0.9, -0.2, -1.8)
        ]
        for wx, wy, wz in wheel_positions:
            glPushMatrix()
            glTranslatef(wx, wy, wz)
            glutSolidSphere(0.2, 10, 10)
            glPopMatrix()
        
        glPopMatrix()



def draw_leisure_area():
    """Área de lazer no canto superior direito com piso, telhado separado e colunas"""
    glPushMatrix()
    glTranslatef(-25, 0, -25)

    # Base (25x25 unidades)
    glColor3f(0.8, 0.9, 0.7)  # Verde claro (grama)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, -25)
    glVertex3f(25, 0, -25)
    glVertex3f(25, 0, 0)
    glVertex3f(0, 0, 0)
    glEnd()

    # Piso da estrutura (15x15 unidades)
    glColor3f(0.6, 0.4, 0.2)  # Cor de madeira mais escura
    glBegin(GL_QUADS)
    glVertex3f(5, 0.05, -20)
    glVertex3f(20, 0.05, -20)
    glVertex3f(20, 0.05, -5)
    glVertex3f(5, 0.05, -5)
    glEnd()

    # Colunas (cilindros para mais realismo)
    glColor3f(0.4, 0.2, 0.1)
    for x in [5.5, 19.5]:
        for z in [-19.5, -5.5]:
            glPushMatrix()
            glTranslatef(x, 0, z)
            glRotatef(-90, 1, 0, 0)  # Cilindro em pé
            glutSolidCylinder(0.2, 3, 12, 12)
            glPopMatrix()

    # Telhado separado (para efeito de cobertura)
    glColor3f(0.5, 0.3, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(4.5, 3, -20.5)
    glVertex3f(20.5, 3, -20.5)
    glVertex3f(20.5, 3, -4.5)
    glVertex3f(4.5, 3, -4.5)
    glEnd()

    glPopMatrix()



def draw_skybox():
    glPushMatrix()
    glDepthMask(GL_FALSE)

    glColor3f(0.5, 0.7, 1.0)  # Azul céu

    size = 500

    glBegin(GL_QUADS)
    # Frente
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)

    # Fundo
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Esquerda
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)

    # Direita
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)

    # Topo
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Base
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)
    glEnd()

    glDepthMask(GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()


def draw_walls():
    glColor3f(0.6, 0.6, 0.6)  # Cor do muro
    wall_height = 3
    size = 50

    glBegin(GL_QUADS)
    # Fundo
    glVertex3f(-size, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(size, wall_height, size)
    glVertex3f(-size, wall_height, size)

    # Esquerda
    glVertex3f(-size, 0, -size)
    glVertex3f(-size, 0, size)
    glVertex3f(-size, wall_height, size)
    glVertex3f(-size, wall_height, -size)

    # Frente
    glVertex3f(-size, 0, -size)
    glVertex3f(size, 0, -size)
    glVertex3f(size, wall_height, -size)
    glVertex3f(-size, wall_height, -size)

    # Direita - lado inferior ao portão
    glVertex3f(size, 0, -size)
    glVertex3f(size, 0, -10)
    glVertex3f(size, wall_height, -10)
    glVertex3f(size, wall_height, -size)

    # Direita - lado superior ao portão
    glVertex3f(size, 0, 10)
    glVertex3f(size, 0, size)
    glVertex3f(size, wall_height, size)
    glVertex3f(size, wall_height, 10)
    glEnd()

    # Portão prateado na direita (muro da direita)
    glColor3f(0.75, 0.75, 0.75)
    glBegin(GL_QUADS)
    glVertex3f(size + 0.01, 0, -10)
    glVertex3f(size + 0.01, 0, 10)
    glVertex3f(size + 0.01, wall_height, 10)
    glVertex3f(size + 0.01, wall_height, -10)
    glEnd()

def draw_sun():
    glPushMatrix()
    glTranslatef(80, 40, -30)  # Posição no céu
    glColor3f(1.0, 1.0, 0.0)  # Amarelo
    glutSolidSphere(3, 20, 20)
    glPopMatrix()

def draw_guardhouse():
    glPushMatrix()
    # Ajuste a posição para dentro do cenário no lado do portão
    glTranslatef(46, 0, 12)  # Próximo ao portão no muro direito

    glColor3f(0.5, 0.3, 0.1)  # Cor marrom da guarita
    glBegin(GL_QUADS)
    # Base
    glVertex3f(0, 0, 0)
    glVertex3f(4, 0, 0)
    glVertex3f(4, 0, 4)
    glVertex3f(0, 0, 4)

    # Frente
    glVertex3f(0, 0, 0)
    glVertex3f(4, 0, 0)
    glVertex3f(4, 4, 0)
    glVertex3f(0, 4, 0)

    # Fundo
    glVertex3f(0, 0, 4)
    glVertex3f(4, 0, 4)
    glVertex3f(4, 4, 4)
    glVertex3f(0, 4, 4)

    # Lado esquerdo
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 3)
    glVertex3f(0, 4, 4)
    glVertex3f(0, 4, 0)

    # Lado direito
    glVertex3f(4, 0, 0)
    glVertex3f(4, 0, 4)
    glVertex3f(4, 4, 4)
    glVertex3f(4, 4, 0)

    # Topo
    glVertex3f(0, 4, 0)
    glVertex3f(4, 4, 0)
    glVertex3f(4, 4, 4)
    glVertex3f(0, 4, 4)
    glEnd()

    glPopMatrix()
