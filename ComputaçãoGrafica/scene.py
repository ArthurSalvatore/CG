from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_building():
    """Desenha um grande prédio retangular no canto esquerdo da cena"""
    glPushMatrix()
    glTranslatef(-25.0, 0.0, 0.0)  # Posiciona no canto esquerdo
    
    # Corpo principal do prédio (20x30 unidades de tamanho)
    glColor3f(0.7, 0.7, 0.7)  # Cinza claro
    glBegin(GL_QUADS)
    # Frente (virada para a garagem)
    glVertex3f(0, 0, 0)
    glVertex3f(40, 0, 0)
    glVertex3f(40, 0, 30)
    glVertex3f(0, 0, 30)
    


    # Frente (Z = 0)
    glVertex3f(0, 0, 0.5)
    glVertex3f(40, 0, 0.5)
    glVertex3f(40, 30, 0.5)
    glVertex3f(0, 30, 0.5)

    # Topo
    glVertex3f(0, 30, 0)
    glVertex3f(40, 30, 0)
    glVertex3f(40, 30, 40)
    glVertex3f(0, 30, 40)
    
    # Laterais e fundo (completando o cubo)
     # Fundo (Z = 50)
    glVertex3f(0, 0, 40)
    glVertex3f(40, 0, 40)
    glVertex3f(40, 30, 40)
    glVertex3f(0, 30, 40)

    # Lado esquerdo (X = 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 40)
    glVertex3f(0, 30, 40)
    glVertex3f(0, 30, 0)

    # Lado direito (X = 50)
    glVertex3f(40, 0, 0)
    glVertex3f(40, 0, 50)
    glVertex3f(40, 30, 50)
    glVertex3f(40, 30, 0)
    glEnd()

    # Porta centralizada (2x4 unidades)
    glColor3f(0.4, 0.2, 0.0)  # Marrom
    glBegin(GL_QUADS)
    glVertex3f(25, 0, 0.1)  # Levemente à frente da parede
    glVertex3f(30, 0, 0.1)
    glVertex3f(30, 4, 0.1)
    glVertex3f(25, 4, 0.1)
    glEnd()

    glPopMatrix()

def draw_garage():
    """Desenha a garagem com vagas e árvores"""
    glPushMatrix()
    
    # Chão principal da garagem (50x50 unidades)
    glColor3f(0.4, 0.4, 0.4)  # Cinza médio
    glBegin(GL_QUADS)
    glVertex3f(-25, 0.01, -50)
    glVertex3f(25, 0.01, -50)
    glVertex3f(25, 0.01, 0)
    glVertex3f(-25, 0.01, 0)
    glEnd()

    # Vagas de estacionamento (2x5 unidades cada)
    glColor3f(0.2, 0.2, 0.2)  # Cinza escuro
    for i in range(5):
        glPushMatrix()
        glTranslatef(-20 + i*10, 0, -5)  # Alinhadas em frente ao prédio
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.02, 0)
        glVertex3f(1, 0.02, 0)
        glVertex3f(1, 0.02, -5)
        glVertex3f(-1, 0.02, -5)
        glEnd()
        glPopMatrix()

    # Árvores no centro (1x3 unidades cada)
    glColor3f(0.0, 0.8, 0.0)  # Verde
    for i in range(7):
        glPushMatrix()
        glTranslatef(-10 + i*5, 0, -25)  # Centro da garagem
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0, -0.5)
        glVertex3f(0.5, 0, -0.5)
        glVertex3f(0.5, 3, -0.5)
        glVertex3f(-0.5, 3, -0.5)
        glEnd()
        glPopMatrix()

    glPopMatrix()

def draw_leisure_area():

    """Área de lazer no canto superior direito"""
    glPushMatrix()
    glTranslatef(-25, 0, -25)  # Metade superior direita
    
    # Base (25x25 unidades)
    glColor3f(0.8, 0.9, 0.7)  # Verde claro
    glBegin(GL_QUADS)
    glVertex3f(0, 0, -25)
    glVertex3f(25, 0, -25)
    glVertex3f(25, 0, 0)
    glVertex3f(0, 0, 0)
    glEnd()

    # Estrutura principal (15x15 unidades)
    glColor3f(0.7, 0.5, 0.3)  # Madeira
    glBegin(GL_QUADS)
    # Piso elevado
    glVertex3f(5, 0, -20)
    glVertex3f(20, 0, -20)
    glVertex3f(20, 0, -5)
    glVertex3f(5, 0, -5)
    
    # Telhado
    glVertex3f(5, 3, -20)
    glVertex3f(20, 3, -20)
    glVertex3f(20, 3, -5)
    glVertex3f(5, 3, -5)
    
    # Colunas
    for x in [5, 20]:
        for z in [-20, -5]:
            glVertex3f(x, 0, z)
            glVertex3f(x, 3, z)
            glVertex3f(x+0.5, 3, z+0.5)
            glVertex3f(x+0.5, 0, z+0.5)
    glEnd()

    glPopMatrix()




def draw_vehicles():
    """Desenha 3 veículos nas vagas de estacionamento"""
    car_colors = [
        (1.0, 0.0, 0.0),  # Vermelho
        (0.0, 0.0, 1.0),  # Azul
        (1.0, 1.0, 0.0)   # Amarelo
    ]

    car_positions = [
        (-20, -5),  # Vaga 1
        (-10, -5),  # Vaga 2
        (0, -5)     # Vaga 3
    ]

    for i in range(3):
        x, z = car_positions[i]
        r, g, b = car_colors[i]
        
        glPushMatrix()
        glTranslatef(x, 0.15, z - 2.5)  # Posição central da vaga
        glScalef(2, 1, 4)              # Forma achatada do carro
        glColor3f(r, g, b)
        glutSolidCube(1.0)
        glPopMatrix()
