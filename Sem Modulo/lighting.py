from OpenGL.GL import *

def configurar_luz(light_id, position, color, intensity):
    """Configura a luz com os parâmetros fornecidos."""
    glLightfv(light_id, GL_POSITION, position+[1])
    glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1.0])
    glLightfv(light_id, GL_SPECULAR, color + [1.0])
    
    glLightf(light_id,GL_CONSTANT_ATTENUATION,1)
    glLightf(light_id,GL_LINEAR_ATTENUATION,0.1)
    glLightf(light_id,GL_QUADRATIC_ATTENUATION,0.001)

    glEnable(light_id)