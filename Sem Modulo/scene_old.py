from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from loadObjs import LoadObjs
import numpy as np
# from PIL import Image
# from OpenGL.GL.shaders import compileProgram, compileShader
# import glm
# from OpenGL.GLUT import glutSolidCube


textures = {}


# #def init_skybox_equi(path):
#     global hdr_tex, skybox_shader
#     skybox_shader = compileProgram(
#       compileShader(open("shaders/skybox.vert").read(), GL_VERTEX_SHADER),
#       compileShader(open("shaders/skybox.frag").read(), GL_FRAGMENT_SHADER),
#     )
#     img = Image.open(path)
#     data = np.array(img, dtype=np.float32)
#     if data.max()>1.0: data /= 255.0
#     h,w = data.shape[:2]
#     hdr_tex = glGenTextures(1)
#     glBindTexture(GL_TEXTURE_2D, hdr_tex)
#     glTexImage2D(GL_TEXTURE_2D,0,GL_RGB16F,w,h,0,GL_RGB,GL_FLOAT,data)
#     for p in (GL_TEXTURE_MIN_FILTER,GL_TEXTURE_MAG_FILTER):
#         glTexParameteri(GL_TEXTURE_2D,p,GL_LINEAR)
#     for p in (GL_TEXTURE_WRAP_S,GL_TEXTURE_WRAP_T):
#         glTexParameteri(GL_TEXTURE_2D,p,GL_CLAMP_TO_EDGE)


# #def load_shader(vert_path: str, frag_path: str) -> int:
#     """Compila e linka um par de shaders GLSL."""
#     with open(vert_path, 'r') as f:
#         vert_src = f.read()
#     with open(frag_path, 'r') as f:
#         frag_src = f.read()
#     return compileProgram(
#         compileShader(vert_src, GL_VERTEX_SHADER),
#         compileShader(frag_src, GL_FRAGMENT_SHADER),
#     )


# #def load_hdr_equirectangular(path: str) -> np.ndarray:
#     """
#     Carrega um arquivo Radiance .hdr (32‑bit float) via Pillow e retorna
#     um array float32 shape (H, W, 3), normalizado em [0,∞).
#     """
#     img = Image.open(path)
#     data = np.array(img, dtype=np.float32)
#     # alguns plugins retornam 0..255, então normaliza se precisar:
#     if data.max() > 1.0:
#         data /= 255.0
#     return data


# def renderCube():
#     """Desenha um cubo unitário usando GLUT."""
#     glutSolidCube(1.0)



# def draw_skybox_equi(camera):
#     glDepthFunc(GL_LEQUAL)
#     glUseProgram(skybox_shader)
#     view = glm.mat4(camera.view_matrix)
#     view[3][0]=view[3][1]=view[3][2]=0
#     locp = glGetUniformLocation(skybox_shader,"projection")
#     locv = glGetUniformLocation(skybox_shader,"view")
#     locm = glGetUniformLocation(skybox_shader,"equirectangularMap")
#     glUniformMatrix4fv(locp,1,GL_FALSE,glm.value_ptr(camera.projection_matrix))
#     glUniformMatrix4fv(locv,1,GL_FALSE,glm.value_ptr(view))
#     glActiveTexture(GL_TEXTURE0)
#     glBindTexture(GL_TEXTURE_2D,hdr_tex)
#     glUniform1i(locm,0)
#     glutSolidCube(1.0)
#     glUseProgram(0)
#     glDepthFunc(GL_LESS)

LIST_TREES = []
    # Árvores centralizadas na linha

for x in range(-45, 40, 15):
    LIST_TREES.append(LoadObjs(obj_path="./objects/tree.obj", scale=(0.5, 0.5, 0.5), position=(x, -1, -15), rotation=(0, 0, 0)))
    




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
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,   GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size[0], size[1], 0,
              GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
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

    # global hdr_tex, skybox_shader
    # # 1) compile shader (depois de criar a janela GL)
    # skybox_shader = load_shader(
    #     "shaders/skybox.vert",
    #     "shaders/skybox.frag"
    # )
    # # 2) load HDR texture
   

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
    """Chão com normal corrigida"""
    if textures.get('ground'):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['ground'])
        glColor3f(1.0, 1.0, 1.0)  # Branco para não afetar a textura
    else:
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.4, 0.4, 0.4)
    
    size = 53
    repeat = 20
    
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # Normal correta apontando para cima
    glTexCoord2f(0, 0)
    glVertex3f(-size, 0, -size)
    glTexCoord2f(repeat, 0)
    glVertex3f(size, 0, -size)
    glTexCoord2f(repeat, repeat)
    glVertex3f(size, 0, size)
    glTexCoord2f(0, repeat)
    glVertex3f(-size, 0, size)
    glEnd()
    
    if textures.get('ground'):
        glDisable(GL_TEXTURE_2D)

def draw_building():
    glPushMatrix()
    # Posiciona o prédio de x=-40 a x=40
    glTranslatef(-40.0, 0.0, 20.0)

    width = 80.0
    height = 35.0   # Altura aumentada para prédios maiores
    depth = 20.0

    # 1) Fachada texturizada
    if 'building' in textures and textures['building'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        # Frente
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(width/10, 0); glVertex3f(width, 0, 0)
        glTexCoord2f(width/10, height/10); glVertex3f(width, height, 0)
        glTexCoord2f(0, height/10); glVertex3f(0, height, 0)
        # Laterais e fundo
        glTexCoord2f(0, 0); glVertex3f(width, 0, 0)
        glTexCoord2f(depth/10, 0); glVertex3f(width, 0, depth)
        glTexCoord2f(depth/10, height/10); glVertex3f(width, height, depth)
        glTexCoord2f(0, height/10); glVertex3f(width, height, 0)
        glTexCoord2f(0, 0); glVertex3f(0, 0, depth)
        glTexCoord2f(depth/10, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(depth/10, height/10); glVertex3f(0, height, 0)
        glTexCoord2f(0, height/10); glVertex3f(0, height, depth)
        glTexCoord2f(0, 0); glVertex3f(0, 0, depth)
        glTexCoord2f(width/10, 0); glVertex3f(width, 0, depth)
        glTexCoord2f(width/10, height/10); glVertex3f(width, height, depth)
        glTexCoord2f(0, height/10); glVertex3f(0, height, depth)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    # 2) Stencil para recorte de janelas/porta frontal
    glEnable(GL_STENCIL_TEST)
    glStencilFunc(GL_ALWAYS, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
    glStencilMask(0xFF)
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
    glDepthMask(GL_FALSE)
    draw_window_shapes(width, height)
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glDepthMask(GL_TRUE)
    glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
    glStencilMask(0x00)
    if 'building' in textures and textures['building'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, -0.05)
        glTexCoord2f(width/10, 0); glVertex3f(width, 0, -0.05)
        glTexCoord2f(width/10, height/10); glVertex3f(width, height, -0.05)
        glTexCoord2f(0, height/10); glVertex3f(0, height, -0.05)
        glEnd()
        glDisable(GL_TEXTURE_2D)
    glDisable(GL_STENCIL_TEST)

    # 3) Desenha janelas, portas e varandas
    draw_windows_and_door(width, height)

    # 4) Telhado
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(0, height, 0)
    glVertex3f(width, height, 0)
    glVertex3f(width, height, depth)
    glVertex3f(0, height, depth)
    glEnd()
    glPopMatrix()


def draw_window_shapes(width, height):
    glColor3f(1,1,1)
    # Porta frontal
    door_w, door_h = 8,6
    x0,x1 = (width-door_w)/2,(width+door_w)/2
    glBegin(GL_QUADS)
    glVertex3f(x0,0,0); glVertex3f(x1,0,0)
    glVertex3f(x1,door_h,0); glVertex3f(x0,door_h,0)
    glEnd()
    # Porta lateral
    lat_z0,lat_z1 = 8,12
    glBegin(GL_QUADS)
    glVertex3f(width,0,lat_z0); glVertex3f(width,0,lat_z1)
    glVertex3f(width,door_h,lat_z1); glVertex3f(width,door_h,lat_z0)
    glEnd()
    # Janelas 3x8
    rows,cols=3,8
    win_w,win_h=5,3
    spx,spy=5,6
    mx=(width-(cols*win_w+(cols-1)*spx))/2
    by=10
    for r in range(rows):
        y=by+r*(win_h+spy)
        for c in range(cols):
            x=mx+c*(win_w+spx)
            glBegin(GL_QUADS)
            glVertex3f(x,y,0)
            glVertex3f(x+win_w,y,0)
            glVertex3f(x+win_w,y+win_h,0)
            glVertex3f(x,y+win_h,0)
            glEnd()


def draw_windows_and_door(width, height):
    # Parâmetros
    door_w,door_h=8,6
    win_w,win_h=5,3
    spx,spy=5,6
    veranda_offset=0.2  # avança um pouco para frente
    vh=1
    rows,cols=3,8
    mx=(width-(cols*win_w+(cols-1)*spx))/2
    by=10
    # Porta frontal
    glColor3f(0.4,0.2,0)
    x0,x1=(width-door_w)/2,(width+door_w)/2
    glBegin(GL_QUADS)
    glVertex3f(x0,0,-0.1); glVertex3f(x1,0,-0.1)
    glVertex3f(x1,door_h,-0.1); glVertex3f(x0,door_h,-0.1)
    glEnd()
    # Porta lateral
    lz0,lz1=8,12
    glBegin(GL_QUADS)
    glVertex3f(width+0.1,0,lz0); glVertex3f(width+0.1,0,lz1)
    glVertex3f(width+0.1,door_h,lz1); glVertex3f(width+0.1,door_h,lz0)
    glEnd()
    # Janelas visíveis
    glColor3f(0.2,0.5,0.8)
    for r in range(rows):
        y=by+r*(win_h+spy)
        for c in range(cols):
            x=mx+c*(win_w+spx)
            glBegin(GL_QUADS)
            glVertex3f(x,y,-0.1)
            glVertex3f(x+win_w,y,-0.1)
            glVertex3f(x+win_w,y+win_h,-0.1)
            glVertex3f(x,y+win_h,-0.1)
            glEnd()
    # Sacada frontal avançada sob janela
    glColor3f(1,0,0)
    for r in range(rows):
        y=by+r*(win_h+spy)
        for c in range(cols):
            x=mx+c*(win_w+spx)
            glBegin(GL_QUADS)
            glVertex3f(x,y,-veranda_offset)
            glVertex3f(x+win_w,y,-veranda_offset)
            glVertex3f(x+win_w,y-vh,-veranda_offset)
            glVertex3f(x,y-vh,-veranda_offset)
            glEnd()

z_slot = 13.0  # z inicial do topo das vagas

# Parâmetros das vagas
vaga_inicial = -25.0
espacamento  = 8.0    # espaçamento entre vagas
slot_w       = 4.0    # largura da vaga
slot_d       = 8.0    # profundidade da vaga



def draw_garage():
    """Desenha a garagem e as vagas entre prédio e árvores"""
    glPushMatrix()
    # Piso sob as vagas
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_QUADS)
    # faixa de piso desde z_slot até z_slot - slot_d
    glVertex3f(-25, -0.1, z_slot)
    glVertex3f( 25, -0.1, z_slot)
    glVertex3f( 25, -0.1, z_slot - slot_d)
    glVertex3f(-25, -0.1, z_slot - slot_d)
    glEnd()

    # Desenha cada vaga retangular
    glColor3f(0.2, 0.2, 0.2)
    for i in range(8):
        x = vaga_inicial + i * espacamento
        glPushMatrix()
        glTranslatef(x, 0, z_slot)
        glBegin(GL_QUADS)
        glVertex3f(-slot_w/2, 0.02, 0)
        glVertex3f( slot_w/2, 0.02, 0)
        glVertex3f( slot_w/2, 0.02, -slot_d)
        glVertex3f(-slot_w/2, 0.02, -slot_d)
        glEnd()
        glPopMatrix()

    # Desenha os veículos
    draw_vehicles_aligned()
    glPopMatrix()
def draw_vehicles_aligned():
    """Desenha carros com cabine recuada e 4 rodas posicionadas corretamente"""
    car_colors = [
        (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0),
        (0.0, 1.0, 0.0), (1.0, 0.5, 0.0), (1.0, 0.0, 1.0)
    ]
    for i in range(6):  # agora 12 carros, um por vaga  # um carro por vaga
        x = vaga_inicial + i * espacamento
        r, g, b = car_colors[i % len(car_colors)]
        glPushMatrix()
        # posiciona o carro levemente acima do solo e centralizado em X e Z
        glTranslatef(x, 0.35, z_slot - slot_d / 2)

        # Carroceria principal
        glPushMatrix()
        glScalef(slot_w * 0.9, 0.7, slot_d * 0.8)
        glColor3f(r, g, b)
        glutSolidCube(1.0)
        glPopMatrix()

        # Cabine recuada e centralizada
        cabin_height = 0.6
        body_half_height = 0.7 / 2
        cabin_half = cabin_height / 2
        glPushMatrix()
        # Recuo em Z de 10% da profundidade da vaga
        glTranslatef(0, body_half_height + cabin_half, -slot_d * 0.1)
        glScalef(slot_w * 0.6, cabin_height, slot_d * 0.3)
        glColor3f(0.2, 0.2, 0.3)
        glutSolidCube(1.0)
        glPopMatrix()

                # Rodas esféricas (4 rodas), alinhadas à base do corpo
        glColor3f(0.05, 0.05, 0.05)
        wheel_radius = 0.35
        wheel_x = slot_w * 0.45
        wheel_z_offset = slot_d * 0.35
        # corpo metade da altura
        body_half_height = 0.7 / 2
        # deslocamento Y para posicionar o centro da roda no nível do solo + radius
        wheel_y = wheel_radius - body_half_height 
        for wz in (wheel_z_offset, -wheel_z_offset):
            for wx in ( wheel_x, -wheel_x ):
                glPushMatrix()
                glTranslatef(wx, wheel_y, wz)
                glutSolidSphere(wheel_radius, 12, 12)
                glPopMatrix()


        glPopMatrix()

def draw_leisure_area():
    """Área de lazer no canto superior direito com piso elevado, colunas retangulares e telhado mais grosso"""
    glPushMatrix()
    glTranslatef(-55, 0, -30)

    # Piso elevado com degrau
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    # Topo do piso (elevado)
    glVertex3f(5,   0.2, -20)
    glVertex3f(20,  0.2, -20)
    glVertex3f(20,  0.2,  -5)
    glVertex3f(5,   0.2,  -5)
    # Frente do degrau (face nordeste)
    glVertex3f(5,   0.05, -20)
    glVertex3f(20,  0.05, -20)
    glVertex3f(20,  0.2,  -20)
    glVertex3f(5,   0.2,  -20)
    # Traseira
    glVertex3f(5,   0.05,  -5)
    glVertex3f(20,  0.05,  -5)
    glVertex3f(20,  0.2,   -5)
    glVertex3f(5,   0.2,   -5)
    # Lado esquerdo
    glVertex3f(5,   0.05, -20)
    glVertex3f(5,   0.05,  -5)
    glVertex3f(5,   0.2,   -5)
    glVertex3f(5,   0.2,  -20)
    # Lado direito
    glVertex3f(20,  0.05, -20)
    glVertex3f(20,  0.05,  -5)
    glVertex3f(20,  0.2,   -5)
    glVertex3f(20,  0.2,  -20)
    glEnd()

    # Colunas retangulares (espessura maior)
    glColor3f(1.0, 0.5, 0.5)
    # Lado esquerdo: dois pilares originais
    for x_model in [5.5]:
        for z_model in [-19.5, -5.5]:
            glPushMatrix()
            glTranslatef(x_model, 1.5, z_model)
            glScalef(0.6, 3, 0.6)
            glutSolidCube(1)
            glPopMatrix()
    # Lado direito: três pilares (inclui o novo entre os dois originais)
    for x_model in [19.5]:
        for z_model in [-19.5, -12.5, -5.5]:
            glPushMatrix()
            glTranslatef(x_model, 1.5, z_model)
            glScalef(0.6, 3, 0.6)
            glutSolidCube(1)
            glPopMatrix()


    # Telhado mais grosso (caixa de 16x0.5x16)
    glColor3f(0.5, 0.3, 0.1)
    glPushMatrix()
    glTranslatef((4.5 + 20.5) / 2, 3.25, (-20.5 + -4.5) / 2)
    glScalef(16, 0.5, 16)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()

def draw_skybox():
    if 'skybox' not in textures or textures['skybox'] is None:
        return

    s = 1000.0  # half the cube side
    W, H = 4.0, 3.0  # atlas columns and rows
    # mapping of face to (col,row) in cross (row 0 is bottom)
    face_pos = {
        'left':   (0, 1),
        'front':  (1, 1),
        'right':  (2, 1),
        'back':   (3, 1),
        'top':    (1, 2),
        'bottom': (1, 0),
    }
    def uv(col, row):
        u0 = col / W; v0 = row / H
        u1 = (col+1) / W; v1 = (row+1) / H
        return u0, 1-v1, u1, 1-v0  # flip V for OpenGL

    glPushAttrib(GL_ENABLE_BIT | GL_DEPTH_BUFFER_BIT | GL_TEXTURE_BIT)
    glPushMatrix()
    # center on camera
    m = glGetFloatv(GL_MODELVIEW_MATRIX)
    m[3][0] = m[3][1] = m[3][2] = 0.0
    glLoadMatrixf(m)

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDepthMask(GL_FALSE)
    glDisable(GL_CULL_FACE)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures['skybox'])
    glColor3f(1.0,1.0,1.0)
    glBegin(GL_QUADS)
    # left (-X)
    u0,v0,u1,v1 = uv(*face_pos['left'])
    glTexCoord2f(u0,v0); glVertex3f(-s,-s, s)
    glTexCoord2f(u1,v0); glVertex3f(-s,-s,-s)
    glTexCoord2f(u1,v1); glVertex3f(-s, s,-s)
    glTexCoord2f(u0,v1); glVertex3f(-s, s, s)
    # front (+Z)
    u0,v0,u1,v1 = uv(*face_pos['front'])
    glTexCoord2f(u0,v1); glVertex3f(-s,-s, s)
    glTexCoord2f(u0,v0); glVertex3f(-s, s, s)
    glTexCoord2f(u1,v0); glVertex3f( s, s, s)
    glTexCoord2f(u1,v1); glVertex3f( s,-s, s)
    # right (+X)
    u0,v0,u1,v1 = uv(*face_pos['right'])
    glTexCoord2f(u1,v0); glVertex3f( s,-s,-s)
    glTexCoord2f(u0,v0); glVertex3f( s,-s, s)
    glTexCoord2f(u0,v1); glVertex3f( s, s, s)
    glTexCoord2f(u1,v1); glVertex3f( s, s,-s)
    # back (-Z)
    u0,v0,u1,v1 = uv(*face_pos['back'])
    glTexCoord2f(u1,v1); glVertex3f( s,-s,-s)
    glTexCoord2f(u1,v0); glVertex3f( s, s,-s)
    glTexCoord2f(u0,v0); glVertex3f(-s, s,-s)
    glTexCoord2f(u0,v1); glVertex3f(-s,-s,-s)
    # top (+Y)
    u0,v0,u1,v1 = uv(*face_pos['top'])
    glTexCoord2f(u0,v1); glVertex3f(-s, s,-s)
    glTexCoord2f(u1,v1); glVertex3f( s, s,-s)
    glTexCoord2f(u1,v0); glVertex3f( s, s, s)
    glTexCoord2f(u0,v0); glVertex3f(-s, s, s)
    # bottom (-Y)
    u0,v0,u1,v1 = uv(*face_pos['bottom'])
    glTexCoord2f(u0,v0); glVertex3f(-s,-s, s)
    glTexCoord2f(u1,v0); glVertex3f( s,-s, s)
    glTexCoord2f(u1,v1); glVertex3f( s,-s,-s)
    glTexCoord2f(u0,v1); glVertex3f(-s,-s,-s)
    glEnd()

    glDepthMask(GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_CULL_FACE)
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    glPopAttrib()



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
    glTranslatef(0, 2, -gate_width/2)
    glScalef(pillar_width, gate_height, pillar_width)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Pilar direito
    glPushMatrix()
    glTranslatef(0, 2, gate_width/2)
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
    """Guarita texturizada com dois degraus completos, porta no topo e telhado"""
    glPushMatrix()
    glTranslatef(44, 0.15, 12)

    # Textura do prédio
    if 'building' in textures and textures['building'] is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures['building'])
        glColor3f(1, 1, 1)
    # Piso
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(4, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(4, 0, 4)
    glTexCoord2f(0, 1); glVertex3f(0, 0, 4)
    glEnd()

    # Paredes com textura
    glBegin(GL_QUADS)
    # Frente z=0
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(4, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(4, 4, 0)
    glTexCoord2f(0, 1); glVertex3f(0, 4, 0)
    # Fundo z=4
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 4)
    glTexCoord2f(1, 0); glVertex3f(4, 0, 4)
    glTexCoord2f(1, 1); glVertex3f(4, 4, 4)
    glTexCoord2f(0, 1); glVertex3f(0, 4, 4)
    # Lado esquerdo x=0
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(0, 0, 4)
    glTexCoord2f(1, 1); glVertex3f(0, 4, 4)
    glTexCoord2f(0, 1); glVertex3f(0, 4, 0)
    # Lado direito x=4
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(4, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(4, 0, 4)
    glTexCoord2f(1, 1); glVertex3f(4, 4, 4)
    glTexCoord2f(0, 1); glVertex3f(4, 4, 0)
    glEnd()

    # Desabilita textura para degraus e porta
    if 'building' in textures and textures['building'] is not None:
        glDisable(GL_TEXTURE_2D)
 
    # Degrau 1: bloco completo
    glColor3f(0.7, 0.7, 0.7)
    # Topo do primeiro degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(1.3, 0.2, 4.0); glVertex3f(2.7, 0.2, 4.0)
    glVertex3f(2.7, 0.2, 4.52); glVertex3f(1.3, 0.2, 4.52)
    glEnd()
    # Frente do primeiro degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(1.3, 0.0, 4.52); glVertex3f(2.7, 0.0, 4.52)
    glVertex3f(2.7, 0.2, 4.52); glVertex3f(1.3, 0.2, 4.52)
    glEnd()
    # Fundo do primeiro degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glVertex3f(1.3, 0.0, 4.0); glVertex3f(2.7, 0.0, 4.0)
    glVertex3f(2.7, 0.2, 4.0); glVertex3f(1.3, 0.2, 4.0)
    glEnd()
    # Lado esquerdo do primeiro degrau
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glVertex3f(1.3, 0.0, 4.0); glVertex3f(1.3, 0.0, 4.52)
    glVertex3f(1.3, 0.2, 4.52); glVertex3f(1.3, 0.2, 4.0)
    glEnd()
    # Lado direito do primeiro degrau
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(2.7, 0.0, 4.0); glVertex3f(2.7, 0.0, 4.52)
    glVertex3f(2.7, 0.2, 4.52); glVertex3f(2.7, 0.2, 4.0)
    glEnd()

    # Degrau 2: bloco completo
    glColor3f(0.75, 0.75, 0.75)
    # Topo do segundo degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(1.4, 0.4, 4.0); glVertex3f(2.6, 0.4, 4.0)
    glVertex3f(2.6, 0.4, 4.4); glVertex3f(1.4, 0.4, 4.4)
    glEnd()
    # Frente do segundo degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(1.4, 0.2, 4.4); glVertex3f(2.6, 0.2, 4.4)
    glVertex3f(2.6, 0.4, 4.4); glVertex3f(1.4, 0.4, 4.4)
    glEnd()
    # Fundo do segundo degrau
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glVertex3f(1.4, 0.2, 4.0); glVertex3f(2.6, 0.2, 4.0)
    glVertex3f(2.6, 0.4, 4.0); glVertex3f(1.4, 0.4, 4.0)
    glEnd()
    # Lado esquerdo do segundo degrau
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glVertex3f(1.4, 0.2, 4.0); glVertex3f(1.4, 0.2, 4.4)
    glVertex3f(1.4, 0.4, 4.4); glVertex3f(1.4, 0.4, 4.0)
    glEnd()
    # Lado direito do segundo degrau
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(2.6, 0.2, 4.0); glVertex3f(2.6, 0.2, 4.4)
    glVertex3f(2.6, 0.4, 4.4); glVertex3f(2.6, 0.4, 4.0)
    glEnd()

    # Porta acima do topo do segundo degrau
    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(1.5, 0.4, 4.02); glVertex3f(2.5, 0.4, 4.02)
    glVertex3f(2.5, 2.4, 4.02); glVertex3f(1.5, 2.4, 4.02)
    glEnd()

    # Vidro frontal
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.1,0.1,0.6,0.4)
    glBegin(GL_QUADS)
    glNormal3f(0,0,-1)
    glVertex3f(1.0,2.5,-0.02); glVertex3f(3.5,2.5,-0.02)
    glVertex3f(3.5,3.5,-0.02); glVertex3f(1.0,3.5,-0.02)
    glEnd()
    glDisable(GL_BLEND)

   
    
    # Telhado em duas águas
    roof_h = 5.5
    glColor3f(0.3,0.3,0.3)
    # Superfícies inclinadas
    glBegin(GL_QUADS)
    glNormal3f(0,0.7,-0.7)
    glVertex3f(0,4,0); glVertex3f(4,4,0);
    glVertex3f(4,roof_h,2); glVertex3f(0,roof_h,2);
    glNormal3f(0,0.7,0.7)
    glVertex3f(0,4,4); glVertex3f(4,4,4);
    glVertex3f(4,roof_h,2); glVertex3f(0,roof_h,2);
    glEnd()
    # Gables front/back
    glBegin(GL_TRIANGLES)
    glNormal3f(0,0,-1)
    glVertex3f(0,4,0); glVertex3f(4,4,0); glVertex3f(2,roof_h,2);
    glNormal3f(0,0,1)
    glVertex3f(0,4,4); glVertex3f(4,4,4); glVertex3f(2,roof_h,2);
    glEnd()
    # Side gables (lateral closures)
    glBegin(GL_TRIANGLES)
    glNormal3f(-1,0,0)
    glVertex3f(0,4,0); glVertex3f(0,4,4); glVertex3f(0,roof_h,2);
    glEnd()
    glBegin(GL_TRIANGLES)
    glNormal3f(1,0,0)
    glVertex3f(4,4,0); glVertex3f(4,4,4); glVertex3f(4,roof_h,2);
    glEnd()

    glPopMatrix()

    