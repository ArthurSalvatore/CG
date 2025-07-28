from typing import Tuple, List, Optional
from dataclasses import dataclass, field
import numpy as np
from OpenGL.GL import *
from PIL import Image
from OpenGL.GLUT import *
import math

def load_png_as_texture(filepath: str) -> int:
    
    img = Image.open(filepath)
    img = img.convert('RGB')
    img_data = np.array(img, dtype=np.uint8)
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,   GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,   GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return tex_id

def compute_mesh(scale: Tuple[float,float,float], subdivisions: int, uv_scale: Tuple[float, float] = (1.0, 1.0)):

    sx, sy, sz = scale
    ux = max(1, int(subdivisions * sx))
    uy = max(1, int(subdivisions * sy))
    uz = max(1, int(subdivisions * sz))

    verts = []
    uvs   = []
    norms = []

    def add_quad(v1, v2, v3, v4, normal, uv1, uv2, uv3, uv4):
        
        # Triângulo 1: v1, v2, v3
        verts.extend([v1, v2, v3])
        uvs.extend([uv1, uv2, uv3])
        norms.extend([normal, normal, normal])
        
        # Triângulo 2: v1, v3, v4
        verts.extend([v1, v3, v4])
        uvs.extend([uv1, uv3, uv4])
        norms.extend([normal, normal, normal])

    # Face frontal (Z positivo) - normal (0, 0, 1)
    for i in range(ux):
        for j in range(uy):
            x0, x1 = (i/ux - 0.5) * sx, ((i+1)/ux - 0.5) * sx
            y0, y1 = (j/uy - 0.5) * sy, ((j+1)/uy - 0.5) * sy
            z = sz / 2
            
            v1 = (x0, y0, z)
            v2 = (x1, y0, z)
            v3 = (x1, y1, z)
            v4 = (x0, y1, z)
            
            u0, u1 = i/ux * sx * uv_scale[0], (i+1)/ux * sx * uv_scale[0]
            v0, v1_uv = j/uy * sy * uv_scale[1], (j+1)/uy * sy * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (0, 0, 1),
                    (u0, v0), (u1, v0), (u1, v1_uv), (u0, v1_uv))

    # Face traseira (Z negativo) - normal (0, 0, -1)
    for i in range(ux):
        for j in range(uy):
            x0, x1 = (i/ux - 0.5) * sx, ((i+1)/ux - 0.5) * sx
            y0, y1 = (j/uy - 0.5) * sy, ((j+1)/uy - 0.5) * sy
            z = -sz / 2
            
            v1 = (x1, y0, z)  
            v2 = (x0, y0, z)
            v3 = (x0, y1, z)
            v4 = (x1, y1, z)
            
            u0, u1 = i/ux * sx * uv_scale[0], (i+1)/ux * sx * uv_scale[0]
            v0, v1_uv = j/uy * sy * uv_scale[1], (j+1)/uy * sy * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (0, 0, -1),
                    (u1, v0), (u0, v0), (u0, v1_uv), (u1, v1_uv))

    # Face direita (X positivo) - normal (1, 0, 0)
    for i in range(uz):
        for j in range(uy):
            z0, z1 = (i/uz - 0.5) * sz, ((i+1)/uz - 0.5) * sz
            y0, y1 = (j/uy - 0.5) * sy, ((j+1)/uy - 0.5) * sy
            x = sx / 2
            
            v1 = (x, y0, z1)
            v2 = (x, y0, z0)
            v3 = (x, y1, z0)
            v4 = (x, y1, z1)
            
            u0, u1 = i/uz * sz * uv_scale[0], (i+1)/uz * sz * uv_scale[0]
            v0, v1_uv = j/uy * sy * uv_scale[1], (j+1)/uy * sy * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (1, 0, 0),
                    (u0, v0), (u1, v0), (u1, v1_uv), (u0, v1_uv))

    # Face esquerda (X negativo) - normal (-1, 0, 0)
    for i in range(uz):
        for j in range(uy):
            z0, z1 = (i/uz - 0.5) * sz, ((i+1)/uz - 0.5) * sz
            y0, y1 = (j/uy - 0.5) * sy, ((j+1)/uy - 0.5) * sy
            x = -sx / 2
            
            v1 = (x, y0, z0)
            v2 = (x, y0, z1)
            v3 = (x, y1, z1)
            v4 = (x, y1, z0)
            
            u0, u1 = i/uz * sz * uv_scale[0], (i+1)/uz * sz * uv_scale[0]
            v0, v1_uv = j/uy * sy * uv_scale[1], (j+1)/uy * sy * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (-1, 0, 0),
                    (u0, v0), (u1, v0), (u1, v1_uv), (u0, v1_uv))

    # Face superior (Y positivo) - normal (0, 1, 0)
    for i in range(ux):
        for j in range(uz):
            x0, x1 = (i/ux - 0.5) * sx, ((i+1)/ux - 0.5) * sx
            z0, z1 = (j/uz - 0.5) * sz, ((j+1)/uz - 0.5) * sz
            y = sy / 2
            
            v1 = (x0, y, z1)
            v2 = (x1, y, z1)
            v3 = (x1, y, z0)
            v4 = (x0, y, z0)
            
            u0, u1 = i/ux * sx * uv_scale[0], (i+1)/ux * sx * uv_scale[0]
            v0, v1_uv = j/uz * sz * uv_scale[1], (j+1)/uz * sz * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (0, 1, 0),
                    (u0, v0), (u1, v0), (u1, v1_uv), (u0, v1_uv))

    # Face inferior (Y negativo) - normal (0, -1, 0)
    for i in range(ux):
        for j in range(uz):
            x0, x1 = (i/ux - 0.5) * sx, ((i+1)/ux - 0.5) * sx
            z0, z1 = (j/uz - 0.5) * sz, ((j+1)/uz - 0.5) * sz
            y = -sy / 2
            
            v1 = (x0, y, z0)
            v2 = (x1, y, z0)
            v3 = (x1, y, z1)
            v4 = (x0, y, z1)
            
            u0, u1 = i/ux * sx * uv_scale[0], (i+1)/ux * sx * uv_scale[0]
            v0, v1_uv = j/uz * sz * uv_scale[1], (j+1)/uz * sz * uv_scale[1]
            
            add_quad(v1, v2, v3, v4, (0, -1, 0),
                    (u0, v0), (u1, v0), (u1, v1_uv), (u0, v1_uv))

    # Converte para numpy arrays
    vertices = np.array(verts, dtype=np.float32)
    texcoords = np.array(uvs, dtype=np.float32)
    normals = np.array(norms, dtype=np.float32)
    return vertices, texcoords, normals

@dataclass
class Fragment:
    position: Tuple[float,float,float]
    scale: Tuple[float,float,float]
    rotation: Tuple[float,float,float] = (0.0,0.0,0.0)
    texture_id: Optional[int] = None
    mesh_vertices: np.ndarray = field(init=False)
    mesh_uvs: np.ndarray      = field(init=False)
    mesh_normals: np.ndarray  = field(init=False)
    uv_scale: Tuple[float, float] = (1.0, 1.0)

    def __post_init__(self):
        subdivisions = 1
        verts, uvs, norms = compute_mesh(self.scale, subdivisions, self.uv_scale)

        # Rotaciona as normais conforme self.rotation
        if self.rotation != (0.0, 0.0, 0.0):
            rx, ry, rz = [math.radians(a) for a in self.rotation]
            # Matrizes de rotação
            def rot_x(v):
                x, y, z = v
                return (
                    x,
                    y * math.cos(rx) - z * math.sin(rx),
                    y * math.sin(rx) + z * math.cos(rx)
                )
            def rot_y(v):
                x, y, z = v
                return (
                    x * math.cos(ry) + z * math.sin(ry),
                    y,
                    -x * math.sin(ry) + z * math.cos(ry)
                )
            def rot_z(v):
                x, y, z = v
                return (
                    x * math.cos(rz) - y * math.sin(rz),
                    x * math.sin(rz) + y * math.cos(rz),
                    z
                )
            rotated_norms = []
            for n in norms:
                n1 = rot_x(n)
                n2 = rot_y(n1)
                n3 = rot_z(n2)
                rotated_norms.append(n3)
            self.mesh_normals = np.array(rotated_norms, dtype=np.float32)
        else:
            self.mesh_normals = np.array(norms, dtype=np.float32)
        self.mesh_vertices = np.array(verts, dtype=np.float32)
        self.mesh_uvs = np.array(uvs, dtype=np.float32)

class FragmentRenderer:
    @staticmethod
    def draw(fragment: Fragment):
        glPushMatrix()
        glTranslatef(*fragment.position)
        glRotatef(fragment.rotation[0], 1, 0, 0)
        glRotatef(fragment.rotation[1], 0, 1, 0)
        glRotatef(fragment.rotation[2], 0, 0, 1)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        

        if fragment.texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, fragment.texture_id)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, fragment.mesh_vertices)
        glTexCoordPointer(2, GL_FLOAT, 0, fragment.mesh_uvs)
        glNormalPointer(GL_FLOAT, 0, fragment.mesh_normals)

        
        glDrawArrays(GL_TRIANGLES, 0, len(fragment.mesh_vertices))

        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        if fragment.texture_id is not None:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()

class Wall:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (0,0,0),
                 scale:       Tuple[float,float,float] = (1,1,1),
                 frag_qtd:    int                      = 100,
                 texture_path: str = "textures/wall_texture.jpg",
                 uv_scale: Tuple[float, float] = (1.0, 1.0)):
        self.base_fragment = Fragment(
            position=pos_initial,
            scale=scale,
            uv_scale=uv_scale
        )
        # carrega textura 1×
        self.base_fragment.texture_id = load_png_as_texture(texture_path)
        self.fragments = self._generate_fragments(frag_qtd, uv_scale)

    def _generate_fragments(self, frag_qtd: int, uv_scale: Tuple[float, float]) -> List[Fragment]:
        fragments = []
        total_scale = sum(self.base_fragment.scale)
        subdivisions = max(1, min(int(frag_qtd / total_scale), 20))
        sx, sy, sz = self.base_fragment.scale

        for i in range(subdivisions):
            for j in range(subdivisions):
                pos = (
                    self.base_fragment.position[0] + i*(sx/subdivisions),
                    self.base_fragment.position[1] + j*(sy/subdivisions),
                    self.base_fragment.position[2]
                )
                sc = (sx/subdivisions, sy/subdivisions, sz)
                frag = Fragment(position=pos, scale=sc, uv_scale=uv_scale)
                frag.texture_id = self.base_fragment.texture_id
                fragments.append(frag)

        return fragments

    def draw(self):
        for frag in self.fragments:
            FragmentRenderer.draw(frag)

class Floor:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (0,0,0),
                 scale:       Tuple[float,float,float] = (1,1,1),
                 frag_qtd:    int                      = 100,
                 texture_path: str = "textures/ground_texture.jpg"):
        self.base_fragment = Fragment(
            position=pos_initial,
            scale=scale
        )
        
        # Gera mesh correta para o floor usando triângulos
        sx, sy, sz = scale
        subdivisions = max(1, min(int(frag_qtd / (sx+sz)), 20))
        verts = []
        uvs = []
        norms = []
        
        for i in range(subdivisions):
            for j in range(subdivisions):
                # Calcula coordenadas do quad
                x0 = -sx/2 + i * (sx/subdivisions)
                x1 = -sx/2 + (i+1) * (sx/subdivisions)
                z0 = -sz/2 + j * (sz/subdivisions)
                z1 = -sz/2 + (j+1) * (sz/subdivisions)
                y = 0  # Floor está no plano XZ
                
                # Vértices do quad no plano XZ (ordem anti-horária vista de cima)
                v1 = (x0, y, z0)  # Bottom-left
                v2 = (x1, y, z0)  # Bottom-right  
                v3 = (x1, y, z1)  # Top-right
                v4 = (x0, y, z1)  # Top-left
                
                # UVs correspondentes
                u0 = i * (sx/subdivisions)
                u1 = (i+1) * (sx/subdivisions)
                v0 = j * (sz/subdivisions)
                v1_uv = (j+1) * (sz/subdivisions)
                
                uv1 = (u0, v0)
                uv2 = (u1, v0)
                uv3 = (u1, v1_uv)
                uv4 = (u0, v1_uv)
                
                # Normal sempre apontando para cima
                normal = (0, 1, 0)
                
                # Primeiro triângulo: v1, v2, v3
                verts.extend([v1, v2, v3])
                uvs.extend([uv1, uv2, uv3])
                norms.extend([normal, normal, normal])
                
                # Segundo triângulo: v1, v3, v4
                verts.extend([v1, v3, v4])
                uvs.extend([uv1, uv3, uv4])
                norms.extend([normal, normal, normal])
        
        self.base_fragment.mesh_vertices = np.array(verts, dtype=np.float32)
        self.base_fragment.mesh_uvs = np.array(uvs, dtype=np.float32)
        self.base_fragment.mesh_normals = np.array(norms, dtype=np.float32)
        self.base_fragment.texture_id = load_png_as_texture(texture_path)
        self.fragments = [self.base_fragment]
    
    def draw(self):
        for frag in self.fragments:
            FragmentRenderer.draw(frag)


class Gate:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (50, 0, 0),
                 gate_width: float = 20,
                 gate_height: float = 4,
                 pillar_width: float = 0.5,
                 num_bars: int = 5,
                 pillar_texture_path: str = "textures/pillar.jpg",
                 bar_texture_path: str = "textures/metal.jpg"):
        
        self.pos_initial = pos_initial
        self.gate_width = gate_width
        self.gate_height = gate_height
        self.pillar_width = pillar_width
        self.num_bars = num_bars
        self.gate_offset = 0.0  # Controla o quanto o portão está aberto
        self.is_opening = False
        self.is_closing = False
        self.max_opening = gate_width * 0.8  # Distância máxima de abertura (80% da largura)
        
        # Carrega texturas
        self.pillar_texture_id = load_png_as_texture(pillar_texture_path)
        self.bar_texture_id = load_png_as_texture(bar_texture_path)
        
        # Cria fragmento base para colisão
        self.base_fragment = Fragment(
            position=pos_initial,
            scale=(pillar_width, gate_height, gate_width)
        )
        
        self.fragments = self._generate_gate_fragments()
    
    def _generate_gate_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.pos_initial
        
        # Pilar esquerdo (fixo)
        left_pillar = Fragment(
            position=(x, y + self.gate_height/2, z - self.gate_width/2),
            scale=(self.pillar_width, self.gate_height, self.pillar_width),
            texture_id=self.pillar_texture_id
        )
        fragments.append(left_pillar)
        
        # Pilar direito (fixo)
        right_pillar = Fragment(
            position=(x, y + self.gate_height/2, z + self.gate_width/2),
            scale=(self.pillar_width, self.gate_height, self.pillar_width),
            texture_id=self.pillar_texture_id
        )
        fragments.append(right_pillar)
        
        # Viga superior (fixa)
        top_beam = Fragment(
            position=(x, y + self.gate_height, z),
            scale=(self.pillar_width, 0.3, self.gate_width),
            texture_id=self.pillar_texture_id
        )
        fragments.append(top_beam)
        
        # Portão móvel - grades horizontais
        bar_thickness = 0.1
        for i in range(self.num_bars):
            y_pos = y + (self.gate_height * (i + 1)) / (self.num_bars + 1)
            bar = Fragment(
                position=(x, y_pos, z),
                scale=(bar_thickness, bar_thickness, self.gate_width ),
                texture_id=self.bar_texture_id
            )
            fragments.append(bar)
        
        # Portão móvel - grades verticais
        num_vertical_bars = 4
        for i in range(num_vertical_bars):
            z_offset = (i - (num_vertical_bars-1)/2) * (self.gate_width * 0.7) / (num_vertical_bars-1)
            z_pos = z + z_offset
            vertical_bar = Fragment(
                position=(x, y + self.gate_height/2, z_pos),
                scale=(bar_thickness, self.gate_height , bar_thickness),
                texture_id=self.bar_texture_id
            )
            fragments.append(vertical_bar)
        
        return fragments
    
    def draw(self):
        for i, frag in enumerate(self.fragments):
            glPushMatrix()
            
            # Cor diferente para cada tipo de componente
            if i < 3:  # Pilares e viga superior
                glColor3f(0.6, 0.4, 0.2)  # Marrom madeira
            else:
                glColor3f(0.3, 0.3, 0.3)  # Cinza metálico para grades
            
            FragmentRenderer.draw(frag)
            glPopMatrix()
    
    def update(self, delta_time: float):
        """Atualiza a animação de abertura/fechamento do portão"""
        opening_speed = 12.0  # Velocidade de abertura/fechamento
        
        if self.is_opening and self.gate_offset < self.max_opening:
            self.gate_offset += opening_speed * delta_time
            if self.gate_offset >= self.max_opening:
                self.gate_offset = self.max_opening
                self.is_opening = False
            self._update_gate_position()
        
        elif self.is_closing and self.gate_offset > 0:
            self.gate_offset -= opening_speed * delta_time
            if self.gate_offset <= 0:
                self.gate_offset = 0
                self.is_closing = False
            self._update_gate_position()
    
    def _update_gate_position(self):
        """Atualiza a posição das partes móveis do portão"""
        # Move apenas as grades lateralmente
        for i in range(3, len(self.fragments)):
            original_pos = self._get_original_position(i)
            # Move no eixo Z (lateral)
            new_z = original_pos[2] + self.gate_offset
            self.fragments[i].position = (original_pos[0], original_pos[1], new_z)
    
    def _get_original_position(self, fragment_index: int):
        """Retorna a posição original de um fragmento específico"""
        x, y, z = self.pos_initial
        
        if fragment_index < 3:
            # Pilares e viga superior (fixos)
            if fragment_index == 0:  # Pilar esquerdo
                return (x, y + self.gate_height/2, z - self.gate_width/2)
            elif fragment_index == 1:  # Pilar direito
                return (x, y + self.gate_height/2, z + self.gate_width/2)
            else:  # Viga superior
                return (x, y + self.gate_height, z)
        
        elif fragment_index < 3 + self.num_bars:
            # Grades horizontais
            bar_index = fragment_index - 3
            y_pos = y + (self.gate_height * (bar_index + 1)) / (self.num_bars + 1)
            return (x, y_pos, z)
        
        else:
            # Grades verticais
            bar_index = fragment_index - 3 - self.num_bars
            num_vertical_bars = 4
            z_offset = (bar_index - (num_vertical_bars-1)/2) * (self.gate_width * 0.7) / (num_vertical_bars-1)
            z_pos = z + z_offset
            return (x, y + self.gate_height/2, z_pos)
    
    def toggle_gate(self):
        """Alterna entre abrir e fechar o portão"""
        if self.gate_offset <= 0.1:
            # Portão fechado, começar a abrir
            self.is_opening = True
            self.is_closing = False
            print("Abrindo portão...")
        elif self.gate_offset >= self.max_opening - 0.1:
            # Portão aberto, começar a fechar
            self.is_opening = False
            self.is_closing = True
            print("Fechando portão...")
        else:
            # Portão em movimento, reverter direção
            if self.is_opening:
                self.is_opening = False
                self.is_closing = True
                print("Revertendo para fechar...")
            else:
                self.is_opening = True
                self.is_closing = False
                print("Revertendo para abrir...")
    
    def is_gate_blocking(self):
        """Verifica se o portão está bloqueando a passagem"""
        return self.gate_offset < self.gate_width * 0.6  # Considera bloqueado se não estiver 60% aberto
    
    def get_collision_fragments(self):
        """Retorna fragmentos para colisão"""
        collision_frags = []
        
        # Sempre adiciona pilares (sempre sólidos)
        collision_frags.extend([self.fragments[0], self.fragments[1]])
        
        # Se o portão estiver bloqueando, adiciona as grades
        if self.is_gate_blocking():
            # Adiciona grades como fragmentos de colisão
            for i in range(3, len(self.fragments)):
                collision_frags.append(self.fragments[i])
        
        return collision_frags


class Skybox:
    def __init__(self, texture_path: str = "textures/skybox.jpg", size: float = 1000.0):
        self.size = size
        self.texture_id = load_png_as_texture(texture_path)
        
        # Mapeamento das faces no atlas (col, row)
        self.face_pos = {
            'left':   (0, 1),
            'front':  (1, 1),
            'right':  (2, 1),
            'back':   (3, 1),
            'top':    (1, 2),
            'bottom': (1, 0),
        }
    
    def _get_uv(self, col: int, row: int, atlas_cols: float = 4.0, atlas_rows: float = 3.0):
        """Calcula coordenadas UV para uma face específica no atlas"""
        u0 = col / atlas_cols
        v0 = row / atlas_rows
        u1 = (col + 1) / atlas_cols
        v1 = (row + 1) / atlas_rows
        return u0, 1 - v1, u1, 1 - v0  # flip V para OpenGL
    
    def draw(self):
        """Renderiza a skybox"""
        s = self.size / 2  # metade do tamanho do cubo
        
        glPushAttrib(GL_ENABLE_BIT | GL_DEPTH_BUFFER_BIT | GL_TEXTURE_BIT)
        glPushMatrix()
        
        # Centraliza na câmera (remove translação)
        m = glGetFloatv(GL_MODELVIEW_MATRIX)
        m[3][0] = m[3][1] = m[3][2] = 0.0
        glLoadMatrixf(m)

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glDisable(GL_CULL_FACE)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor3f(1.0, 1.0, 1.0)
        
        glBegin(GL_QUADS)
        # Face esquerda (-X)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['left'])
        glTexCoord2f(u0, v0); glVertex3f(-s, -s, s)
        glTexCoord2f(u1, v0); glVertex3f(-s, -s, -s)
        glTexCoord2f(u1, v1); glVertex3f(-s, s, -s)
        glTexCoord2f(u0, v1); glVertex3f(-s, s, s)
        
        # Face frontal (+Z)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['front'])
        glTexCoord2f(u0, v1); glVertex3f(-s, -s, s)
        glTexCoord2f(u0, v0); glVertex3f(-s, s, s)
        glTexCoord2f(u1, v0); glVertex3f(s, s, s)
        glTexCoord2f(u1, v1); glVertex3f(s, -s, s)
        
        # Face direita (+X)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['right'])
        glTexCoord2f(u1, v0); glVertex3f(s, -s, -s)
        glTexCoord2f(u0, v0); glVertex3f(s, -s, s)
        glTexCoord2f(u0, v1); glVertex3f(s, s, s)
        glTexCoord2f(u1, v1); glVertex3f(s, s, -s)
        
        # Face traseira (-Z)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['back'])
        glTexCoord2f(u1, v1); glVertex3f(s, -s, -s)
        glTexCoord2f(u1, v0); glVertex3f(s, s, -s)
        glTexCoord2f(u0, v0); glVertex3f(-s, s, -s)
        glTexCoord2f(u0, v1); glVertex3f(-s, -s, -s)
        
        # Face superior (+Y)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['top'])
        glTexCoord2f(u0, v1); glVertex3f(-s, s, -s)
        glTexCoord2f(u1, v1); glVertex3f(s, s, -s)
        glTexCoord2f(u1, v0); glVertex3f(s, s, s)
        glTexCoord2f(u0, v0); glVertex3f(-s, s, s)
        
        # Face inferior (-Y)
        u0, v0, u1, v1 = self._get_uv(*self.face_pos['bottom'])
        glTexCoord2f(u0, v0); glVertex3f(-s, -s, s)
        glTexCoord2f(u1, v0); glVertex3f(s, -s, s)
        glTexCoord2f(u1, v1); glVertex3f(s, -s, -s)
        glTexCoord2f(u0, v1); glVertex3f(-s, -s, -s)
        glEnd()

        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_CULL_FACE)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glPopAttrib()

class Balcony:
    def __init__(self, 
                 pos_initial: Tuple[float,float,float] = (0, 10, -0.2),
                 width: float = 5.0,
                 height: float = 1.0,
                 depth: float = 0.2):
        self.position = pos_initial
        self.width = width
        self.height = height
        self.depth = depth
        self.fragments = self._generate_balcony_fragments()
    
    def _generate_balcony_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.position
        


        # Piso da varanda
        floor_fragment = Fragment(
            position=(x, y, z),
            scale=(self.width, 0.1, self.depth)
        )
        fragments.append(floor_fragment)
        
        # Guarda-corpo frontal
        railing_front = Fragment(
            position=(x, y + self.height/2, z - self.depth/2),
            scale=(self.width, self.height, 0.05)
        )
        fragments.append(railing_front)
        
        # Guarda-corpos laterais
        railing_left = Fragment(
            position=(x - self.width/2, y + self.height/2, z),
            scale=(0.05, self.height, self.depth)
        )
        fragments.append(railing_left)
        
        railing_right = Fragment(
            position=(x + self.width/2, y + self.height/2, z),
            scale=(0.05, self.height, self.depth)
        )
        fragments.append(railing_right)

        # janela
        window = Fragment(
            position=(x, y + self.height/2 + 1.5, z - self.depth/2+0.25),
            scale=(self.width * 0.8, self.height * 4, 0.05)
        )
        fragments.append(window)

        
        return fragments
    
    def draw(self):
        for i, frag in enumerate(self.fragments):
            glPushMatrix()
            if i == 0:  # Piso
                glColor3f(1.0, 1.0, 1.0)
            elif i<=3:  # Guarda-corpo
                glColor3f(1.0, 0.0, 0.0)
            else:  # Janela
                glColor4f(0.0, 0.7, 0.7,0.7)
            FragmentRenderer.draw(frag)
            glPopMatrix()

class Vehicle:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (0, 0.35, 0),
                 car_width: float = 3.6,
                 car_length: float = 6.4,
                 car_height: float = 0.7,
                 color: Tuple[float,float,float] = (1.0, 0.0, 0.0)):
        self.position = pos_initial
        self.car_width = car_width
        self.car_length = car_length
        self.car_height = car_height
        self.color = color
        self.fragments = self._generate_vehicle_fragments()
    
    def _generate_vehicle_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.position
        
        # Carroceria principal
        body = Fragment(
            position=(x, y, z),
            scale=(self.car_width * 0.9, self.car_height, self.car_length * 0.8)
        )
        fragments.append(body)
        
        # Cabine 
        cabin = Fragment(
            position=(x, y + self.car_height/2 + 0.3, z - self.car_length * 0.1),
            scale=(self.car_width * 0.6, 0.6, self.car_length * 0.3)
        )
        fragments.append(cabin)
        
        
        wheel_radius = 0.35
        wheel_positions = [
            (self.car_width * 0.45, -self.car_length * 0.35),
            (-self.car_width * 0.45, -self.car_length * 0.35),
            (self.car_width * 0.45, self.car_length * 0.35),
            (-self.car_width * 0.45, self.car_length * 0.35)
        ]
        
        for wx, wz in wheel_positions:
            wheel = Fragment(
                position=(x + wx, y - self.car_height/2 + wheel_radius, z + wz),
                scale=(wheel_radius * 2, wheel_radius * 2, wheel_radius * 2)
            )
            fragments.append(wheel)
        
        return fragments
    
    def draw(self):
        for i, frag in enumerate(self.fragments):
            if i == 0:  # Carroceria
                glColor3f(*self.color)
                FragmentRenderer.draw(frag)
            elif i == 1:  # Cabine
                glColor3f(0.2, 0.2, 0.3)
                FragmentRenderer.draw(frag)
            else:  # Rodas 
                glPushMatrix()
                glColor3f(0.05, 0.05, 0.05)
                glTranslatef(*frag.position)
                glRotatef(90, 0, 1, 0)
                glutSolidTorus(0.1, frag.scale[0]/2, 12, 24)
                glPopMatrix()

    def get_collision_fragments(self):
        
        return self.fragments[0]


class Garage:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (-25, -0.85, 13),
                 garage_width: float = 50.0,
                 garage_depth: float = 8.0,
                 num_slots: int = 8): 
        self.position = pos_initial
        self.garage_width = garage_width
        self.garage_depth = garage_depth
        self.num_slots = num_slots
        self.slot_spacing = garage_width / num_slots  #
        self.slot_width = 4.0  # Largura individual da vaga
        
        # Cores dos carros (6 cores para os primeiros 6 carros)
        self.car_colors = [
            (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0),
            (0.0, 1.0, 0.0), (1.0, 0.5, 0.0), (1.0, 0.0, 1.0)
        ]
        
        self.fragments = self._generate_garage_fragments()
        self.vehicles = self._generate_vehicles()
    
    def _generate_garage_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.position
        
        # Piso da garagem (uma faixa contínua)
        floor = Fragment(
            position=(x + self.garage_width/2, y, z - self.garage_depth/2),
            scale=(self.garage_width, 0.02, self.garage_depth)
        )
        fragments.append(floor)
        
        # Marcações das vagas individuais
        for i in range(self.num_slots):
            slot_x = x + i * self.slot_spacing + self.slot_spacing/2
            slot_marking = Fragment(
                position=(slot_x, y + 0.02, z - self.garage_depth/2),
                scale=(self.slot_width, 0.01, self.garage_depth * 0.9)
            )
            fragments.append(slot_marking)
        
        return fragments
    
    def _generate_vehicles(self) -> List[Vehicle]:
        vehicles = []
        x, y, z = self.position
        
        
        for i in range(min(6, self.num_slots)):
            car_x = x + i * self.slot_spacing + self.slot_spacing/2
            car_z = z - self.garage_depth/2
            color = self.car_colors[i]
            
            vehicle = Vehicle(
                pos_initial=(car_x, y + 0.35, car_z),
                car_width=self.slot_width * 0.9,
                car_length=self.garage_depth * 0.8,
                color=color
            )
            vehicles.append(vehicle)
        
        return vehicles
    
    def draw(self):
        # Desenha piso
        for i, frag in enumerate(self.fragments):
            if i == 0:  # Piso principal
                glColor3f(0.4, 0.4, 0.4)
            else:  # Marcações das vagas
                glColor3f(0.2, 0.2, 0.2)
            FragmentRenderer.draw(frag)
        
        # Desenha veículos
        for vehicle in self.vehicles:
            vehicle.draw()

    def get_collision_fragments(self):
        return [vehicle.get_collision_fragments() for vehicle in self.vehicles]





class Guardhouse:
    def __init__(self,
                 pos_initial: Tuple[float,float,float] = (44, -0.85, 12),
                 width: float = 4.0,
                 height: float = 4.0,
                 depth: float = 4.0,
                 texture_path: str = "textures/brick_wall_diffuse.jpg"):
        self.position = pos_initial
        self.width = width
        self.height = height
        self.depth = depth
        self.texture_id = load_png_as_texture(texture_path)
        self.fragments = self._generate_guardhouse_fragments()
    
    def _generate_guardhouse_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.position
        

        # Estrutura principal 
        main_structure = Fragment(
            position=(x + self.width/2, y + self.height/2, z + self.depth/2),
            scale=(self.width, self.height, self.depth),
            texture_id=self.texture_id
        )
        fragments.append(main_structure) #0

        
        # Degraus 
         # Primeiro degrau
        step1 = Fragment(
            position=(x + self.width/2, y + 0.1, z + self.depth + 0.26),
            scale=(1.4, 0.2, 0.52)
        )
        fragments.append(step1) #1
        
         # Segundo degrau
        step2 = Fragment(
            position=(x + self.width/2, y + 0.3, z + self.depth + 0.2),
            scale=(1.2, 0.2, 0.4)
        )
        fragments.append(step2) #2

        # Telhado (prisma triangular)
        roof_base = Fragment(
            position=(x + self.width/2, y + self.height + 0.75, z + self.depth/2),
            scale=(self.width + 0.2, 1.5, self.depth + 0.2)
        )
        fragments.append(roof_base) #3


        #janela
        window = Fragment(
            position=(x + self.width/2, y + self.height - 1.5, z ),
            scale=(2.2, 1, 0.01)
        )
        fragments.append(window) #4

        # porta
        door = Fragment(
            position=(x + self.width/2, y + 1.65, z + self.depth + 0.1),
            scale=(1.5, 2.4, 0.01)
        )
        fragments.append(door) #5
        

        
        return fragments
    
    def draw(self):
        x, y, z = self.position
        
        # Estrutura principal com textura
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.8, 0.8, 0.8)
        
        FragmentRenderer.draw(self.fragments[0])
        
        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
        
        # Degraus
        glColor3f(0.7, 0.7, 0.7)
        FragmentRenderer.draw(self.fragments[1])
        FragmentRenderer.draw(self.fragments[2])
        
        # Telhado como prisma triangular
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(x + self.width/2, y + self.height, z + self.depth/2)
        
        roof_height = 1.5
        roof_width = self.width + 0.2
        roof_depth = self.depth + 0.2
        
        # Desenha telhado como prisma triangular
        glBegin(GL_TRIANGLES)
        # Face frontal
        glNormal3f(0, 0, -1)
        glVertex3f(-roof_width/2, 0, -roof_depth/2)
        glVertex3f(roof_width/2, 0, -roof_depth/2)
        glVertex3f(0, roof_height, -roof_depth/2)
        
        # Face traseira
        glNormal3f(0, 0, 1)
        glVertex3f(-roof_width/2, 0, roof_depth/2)
        glVertex3f(roof_width/2, 0, roof_depth/2)
        glVertex3f(0, roof_height, roof_depth/2)
        glEnd()
        
        # Faces inclinadas
        glBegin(GL_QUADS)
        # Face esquerda inclinada
        glNormal3f(-0.707, 0.707, 0)
        glVertex3f(-roof_width/2, 0, -roof_depth/2)
        glVertex3f(0, roof_height, -roof_depth/2)
        glVertex3f(0, roof_height, roof_depth/2)
        glVertex3f(-roof_width/2, 0, roof_depth/2)
        
        # Face direita inclinada
        glNormal3f(0.707, 0.707, 0)
        glVertex3f(roof_width/2, 0, -roof_depth/2)
        glVertex3f(0, roof_height, -roof_depth/2)
        glVertex3f(0, roof_height, roof_depth/2)
        glVertex3f(roof_width/2, 0, roof_depth/2)
        glEnd()
        
        glPopMatrix()

        # janela
        glColor4f(0.0, 0.7, 0.7,0.7)
        FragmentRenderer.draw(self.fragments[4])
        # porta
        glColor3f(0.3, 0.2, 0.1) 
        FragmentRenderer.draw(self.fragments[5])

    
    def get_collision_fragments(self):
        
        return self.fragments[0:4]  


class LeisureArea:
    def __init__(self, pos=(-40, -1, -35), area_width=15.0, area_depth=15.0, pillar_height=3.0):
        self.position = pos
        self.area_width = area_width
        self.area_depth = area_depth
        self.pillar_height = pillar_height
        self.fragments = self._generate_leisure_fragments()
    
    def _generate_leisure_fragments(self) -> List[Fragment]:
        fragments = []
        x, y, z = self.position
        
        # Piso elevado
        elevated_floor = Fragment(
            position=(x + self.area_width/2, y + 0.15, z + self.area_depth/2),
            scale=(self.area_width, 0.3, self.area_depth))
        fragments.append(elevated_floor)
        
        # Pilares de sustentação
        pillar_positions = [
            (x + 2.5, z + 2.5),    # Canto inferior esquerdo
            (x + 2.5, z + 12.5),    # Canto superior esquerdo
            (x + 12.5, z + 2.5),    # Canto inferior direito
            (x + 12.5, z + 7.5),    # Meio direito
            (x + 12.5, z + 12.5)    # Canto superior direito
        ]
        
        for px, pz in pillar_positions:
            pillar = Fragment(
                position=(px, y + self.pillar_height/2 + 0.3, pz),
                scale=(0.6, self.pillar_height, 0.6)
            )
            fragments.append(pillar)
        
        # Telhado
        roof = Fragment(
            position=(x + self.area_width/2, y + self.pillar_height + 0.55, z + self.area_depth/2),
            scale=(self.area_width + 1, 0.5, self.area_depth + 1)
        )
        fragments.append(roof)
        
        return fragments
    
    def draw(self):
        # Piso
        glColor3f(0.8, 0.8, 0.8)  
        FragmentRenderer.draw(self.fragments[0])
        
        # Pilares
        glColor3f(0.7, 0.5, 0.3)  
        for frag in self.fragments[1:-1]:
            FragmentRenderer.draw(frag)
        
        # Telhado
        glColor3f(0.3, 0.2, 0.1)  
        FragmentRenderer.draw(self.fragments[-1])
    
    def get_collision_fragments(self):
        
        return self.fragments[1:-1]  # somente os pilares