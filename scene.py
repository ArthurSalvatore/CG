from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

textures = {}

def load_png_as_texture(filepath):
    from PIL import Image
    import numpy as np
    try:
        img = Image.open(filepath)
        img = img.convert('RGB')  # Garante que a imagem esteja em RGB
        img_data = np.array(img)  # Converte para um array numpy
        size = img.size  # Tamanho da imagem (largura e altura)

        print(f"Carregando textura: {filepath}, tamanho: {size}")

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size[0], size[1], 0,
                    GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return tex_id
    except Exception as e:
        print(f"Erro ao carregar a textura : {str(e)}")
        return None


def init_textures():
    global textures
    from PIL import Image
    import numpy as np
    
    
    # Carrega a textura do chão
    try:
        img = Image.open("textures/ground_texture.jpg")
        img_data = np.array(list(img.getdata()), np.uint8)
        
        textures['ground'] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textures['ground'])
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.width, img.height,
                         GL_RGB, GL_UNSIGNED_BYTE, img_data)
    except Exception as e:
        print(f"Erro ao carregar textura: {str(e)}")
        textures['ground'] = None
    try:
        img = Image.open("textures/brick_wall_diffuse.jpg")
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # Corrige a orientação
        img_data = np.array(img)
        
        textures['building'] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.width, img.height,
                         GL_RGB, GL_UNSIGNED_BYTE, img_data)
    except Exception as e:
        print(f"Erro ao carregar textura do prédio: {str(e)}")
        textures['building'] = None
    try:
        img = Image.open("textures/wall_texture.jpg")  # Substitua pelo seu arquivo de textura
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(img)
        
        textures['wall'] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textures['wall'])
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.width, img.height,
                         GL_RGB, GL_UNSIGNED_BYTE, img_data)
    except Exception as e:
        print(f"Erro ao carregar textura dos muros: {str(e)}")
        textures['wall'] = None

    # Textura da skybox (existente)
    textures['skybox'] = load_png_as_texture("textures/skybox.png")

def draw_ground():
    """Desenha o chão do cenário com textura."""
    if 'ground' not in textures or textures['ground'] is None:
        # Fallback se a textura não carregar
        glColor3f(0.4, 0.4, 0.4)
        size = 70
        glBegin(GL_QUADS)
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glEnd()
        return
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures['ground'])
    
    glColor3f(1, 1, 1)  # Cor branca para textura pura
    size = 70
    repeat_count = 20  # Quantas vezes a textura se repete
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(repeat_count, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(repeat_count, repeat_count); glVertex3f(size, 0, size)
    glTexCoord2f(0, repeat_count); glVertex3f(-size, 0, size)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def draw_building():
    glPushMatrix()
    glTranslatef(-25.0, 0.0, 20.0)
    
    # 1. Primeiro desenha TODAS as faces com textura
    if 'building' in textures and textures['building'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        glColor3f(1, 1, 1)
        
        # Todas as faces (incluindo frente)
        glBegin(GL_QUADS)
        # Frente (com coordenadas de textura)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(8, 0); glVertex3f(40, 0, 0)
        glTexCoord2f(8, 6); glVertex3f(40, 30, 0)
        glTexCoord2f(0, 6); glVertex3f(0, 30, 0)
        
        # Lado direito
        glTexCoord2f(0, 0); glVertex3f(40, 0, 0)
        glTexCoord2f(4, 0); glVertex3f(40, 0, 20)
        glTexCoord2f(4, 6); glVertex3f(40, 30, 20)
        glTexCoord2f(0, 6); glVertex3f(40, 30, 0)
        
        # Lado esquerdo
        glTexCoord2f(0, 0); glVertex3f(0, 0, 20)
        glTexCoord2f(4, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(4, 6); glVertex3f(0, 30, 0)
        glTexCoord2f(0, 6); glVertex3f(0, 30, 20)
        
        # Fundo
        glTexCoord2f(0, 0); glVertex3f(0, 0, 20)
        glTexCoord2f(8, 0); glVertex3f(40, 0, 20)
        glTexCoord2f(8, 6); glVertex3f(40, 30, 20)
        glTexCoord2f(0, 6); glVertex3f(0, 30, 20)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
    
    # 2. Usa stencil buffer para "recortar" áreas das janelas/porta
    glEnable(GL_STENCIL_TEST)
    
    # Configura stencil buffer para marcar áreas a serem mantidas
    glStencilFunc(GL_ALWAYS, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
    glStencilMask(0xFF)
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
    glDepthMask(GL_FALSE)
    
    # Desenha formas das janelas/porta (apenas no stencil buffer)
    draw_window_shapes()
    
    # Configura para desenhar apenas onde stencil != 1
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glDepthMask(GL_TRUE)
    glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
    glStencilMask(0x00)
    
    # 3. Redesenha a fachada com textura apenas nas áreas não marcadas
    if 'building' in textures and textures['building'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        glColor3f(1, 1, 1)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, -0.05)  # Ligeiramente atrás
        glTexCoord2f(8, 0); glVertex3f(40, 0, -0.05)
        glTexCoord2f(8, 6); glVertex3f(40, 30, -0.05)
        glTexCoord2f(0, 6); glVertex3f(0, 30, -0.05)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
    
    glDisable(GL_STENCIL_TEST)
    
    # 4. Desenha as janelas e porta normalmente (sobre a textura)
    draw_windows_and_door()
    
    # 5. Telhado (sem textura)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(0, 30, 0)
    glVertex3f(40, 30, 0)
    glVertex3f(40, 30, 20)
    glVertex3f(0, 30, 20)
    glEnd()
    
    glPopMatrix()

def draw_window_shapes():
    """Desenha formas das janelas/porta apenas no stencil buffer"""
    glColor3f(1, 1, 1)  # Cor não importa (não renderiza cor)
    
    # Porta
    glBegin(GL_QUADS)
    glVertex3f(18, 0, 0)
    glVertex3f(22, 0, 0)
    glVertex3f(22, 6, 0)
    glVertex3f(18, 6, 0)
    glEnd()
    
    # Janelas
    for row in range(3):
        for col in range(4):
            x0 = 5 + col * 8
            y0 = 10 + row * 6
            glBegin(GL_QUADS)
            glVertex3f(x0, y0, 0)
            glVertex3f(x0 + 4, y0, 0)
            glVertex3f(x0 + 4, y0 + 4, 0)
            glVertex3f(x0, y0 + 4, 0)
            glEnd()

def draw_windows_and_door():
    """Desenha janelas e porta visíveis"""
    # Porta
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


def draw_garage():
    glPushMatrix()
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_QUADS)
    glVertex3f(-25, -0.1, -50)
    glVertex3f(25, -0.1, -50)
    glVertex3f(25, -0.1, 0)
    glVertex3f(-25, -0.1, 0)
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

    

    # Piso da estrutura (15x15 unidades)
    glColor3f(0.6, 0.4, 0.2)  # Cor de madeira mais escura
    glBegin(GL_QUADS)
    glVertex3f(5, 0.05, -20)
    glVertex3f(20, 0.05, -20)
    glVertex3f(20, 0.05, -5)
    glVertex3f(5, 0.05, -5)
    glEnd()

    # Colunas 
    glColor3f(0.4, 0.2, 0.1)
    for x in [5.5, 19.5]:
        for z in [-19.5, -5.5]:
            glPushMatrix()
            glTranslatef(x, 0, z)
            glRotatef(-90, 1, 0, 0)  # Cilindro em pé
            glutSolidCylinder(0.2, 3, 12, 12)
            glPopMatrix()

    # Telhado 
    glColor3f(0.5, 0.3, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(4.5, 3, -20.5)
    glVertex3f(20.5, 3, -20.5)
    glVertex3f(20.5, 3, -4.5)
    glVertex3f(4.5, 3, -4.5)
    glEnd()

    glPopMatrix()
def draw_skybox():
    size = 1000  # Aumente o tamanho da skybox
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDepthMask(GL_FALSE)

    if 'skybox' in textures and textures['skybox'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['skybox'])
        glColor3f(1, 1, 1)  # Cor branca para textura pura
    else:
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.5, 0.7, 1.0)  # Fallback para cor azul

    glBegin(GL_QUADS)
    # Frente
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, -size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
    # Fundo
    glTexCoord2f(0, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    # Esquerda
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(-size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(-size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
    # Direita
    glTexCoord2f(0, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(size, size, -size)
    # Topo
    glTexCoord2f(0, 0); glVertex3f(-size, size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, size, size)
    # Base (normalmente não visível)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
    glTexCoord2f(1, 1); glVertex3f(size, -size, size)
    glTexCoord2f(0, 1); glVertex3f(-size, -size, size)
    glEnd()

    if 'skybox' in textures and textures['skybox'] is not None:
        glDisable(GL_TEXTURE_2D)

    glDepthMask(GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
   
    glPopMatrix()
def draw_walls():
    # Verifica se a textura dos muros está carregada
    if 'wall' not in textures or textures['wall'] is None:
        # Fallback: usa textura do prédio se disponível
        if 'building' in textures and textures['building'] is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textures['building'])
            glColor3f(1, 1, 1)
        else:
            # Fallback final: cor sólida
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.6, 0.6, 0.6)
    else:
        # Usa a textura específica dos muros
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['wall'])
        glColor3f(1, 1, 1)

    wall_height = 3
    size = 50
    gate_width = 20  # Largura do portão
    texture_repeat_horizontal = 10
    texture_repeat_vertical = 1

    glBegin(GL_QUADS)
    # Fundo
    glTexCoord2f(0, 0); glVertex3f(-size, 0, size)
    glTexCoord2f(texture_repeat_horizontal, 0); glVertex3f(size, 0, size)
    glTexCoord2f(texture_repeat_horizontal, texture_repeat_vertical); glVertex3f(size, wall_height, size)
    glTexCoord2f(0, texture_repeat_vertical); glVertex3f(-size, wall_height, size)

    # Esquerda
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(texture_repeat_horizontal, 0); glVertex3f(-size, 0, size)
    glTexCoord2f(texture_repeat_horizontal, texture_repeat_vertical); glVertex3f(-size, wall_height, size)
    glTexCoord2f(0, texture_repeat_vertical); glVertex3f(-size, wall_height, -size)

    # Frente
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(texture_repeat_horizontal, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(texture_repeat_horizontal, texture_repeat_vertical); glVertex3f(size, wall_height, -size)
    glTexCoord2f(0, texture_repeat_vertical); glVertex3f(-size, wall_height, -size)

    # Direita - parte inferior (antes do portão)
    glTexCoord2f(0, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(texture_repeat_horizontal/4, 0); glVertex3f(size, 0, -gate_width/2)
    glTexCoord2f(texture_repeat_horizontal/4, texture_repeat_vertical); glVertex3f(size, wall_height, -gate_width/2)
    glTexCoord2f(0, texture_repeat_vertical); glVertex3f(size, wall_height, -size)

    # Direita - parte superior (após o portão)
    glTexCoord2f(0, 0); glVertex3f(size, 0, gate_width/2)
    glTexCoord2f(texture_repeat_horizontal/4, 0); glVertex3f(size, 0, size)
    glTexCoord2f(texture_repeat_horizontal/4, texture_repeat_vertical); glVertex3f(size, wall_height, size)
    glTexCoord2f(0, texture_repeat_vertical); glVertex3f(size, wall_height, gate_width/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_gate():
    glPushMatrix()
    # Posiciona o portão no muro direito
    glTranslatef(50, 0, 0)  # Muro direito está em x=50
    
    gate_width = 20
    gate_height = 4
    
    # Pilares do portão
    glColor3f(0.4, 0.2, 0.1)  # Cor marrom para os pilares
    pillar_width = 0.5
    
    # Pilar esquerdo
    glPushMatrix()
    glTranslatef(0, 0, -gate_width/2)
    glScalef(pillar_width, gate_height, pillar_width)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Pilar direito
    glPushMatrix()
    glTranslatef(0, 0, gate_width/2)
    glScalef(pillar_width, gate_height, pillar_width)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Parte superior do portão
    glPushMatrix()
    glTranslatef(0, gate_height, 0)
    glScalef(pillar_width, 0.2, gate_width)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Grades do portão (opcional)
    glColor3f(0.7, 0.7, 0.7)  # Cor cinza para as grades
    bar_thickness = 0.1
    num_bars = 5
    
    for i in range(num_bars):
        y_pos = (gate_height * i) / num_bars
        glPushMatrix()
        glTranslatef(0, y_pos, 0)
        glScalef(bar_thickness, bar_thickness, gate_width)
        glutSolidCube(1.0)
        glPopMatrix()
    
    glPopMatrix()



def draw_collision_debug(player, collision_objects):
    glDisable(GL_LIGHTING)
    
    # Desenha o raio de colisão do jogador
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glPushMatrix()
    glTranslatef(player.x, 0.1, player.z)
    glutWireSphere(player.collision_radius, 12, 12)
    glPopMatrix()
    
    # Desenha os objetos de colisão
    for obj in collision_objects:
        if obj.get('no_collide', False):
            continue
            
        glColor3f(1.0, 0.0, 0.0)  # Vermelho
        if obj['type'] == 'rectangle':
            x_min, x_max, z_min, z_max = obj['coords']
            glBegin(GL_LINE_LOOP)
            glVertex3f(x_min, 0.1, z_min)
            glVertex3f(x_max, 0.1, z_min)
            glVertex3f(x_max, 0.1, z_max)
            glVertex3f(x_min, 0.1, z_max)
            glEnd()
        elif obj['type'] == 'circle':
            cx, cz, radius = obj['coords']
            glPushMatrix()
            glTranslatef(cx, 0.1, cz)
            glutWireSphere(radius, 12, 12)
            glPopMatrix()
    
    glEnable(GL_LIGHTING)
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
