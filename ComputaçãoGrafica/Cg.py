import glfw
from OpenGL.GL import *

def inicializar():
    glfw.init()
    glfw.window_hint(glfw.RESIZABLE, False)
    janela = glfw.create_window(800, 600, "Bandeira da Bahia", None, None)
    glfw.make_context_current(janela)
    return janela

def desenhar_bandeira():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    
    vermelho = (0.8, 0.0, 0.0)
    branco = (1.0, 1.0, 1.0)
    azul = (0.0, 0.2, 0.6)

    
    altura_faixa = 2.0 / 5.0  

    for i in range(5):
        if i % 2 == 0:
            cor = branco
        else:
            cor = vermelho
        y_top = 1.0 - i * altura_faixa
        y_bottom = y_top - altura_faixa
        glBegin(GL_QUADS)
        glColor3f(*cor)
        glVertex2f(-1.0, y_bottom)
        glVertex2f(1.0, y_bottom)
        glVertex2f(1.0, y_top)
        glVertex2f(-1.0, y_top)
        glEnd()

    # quadrado azul no canto superior esquerdo 
    glBegin(GL_QUADS)
    glColor3f(*azul)
    glVertex2f(-1.0, 1.0)
    glVertex2f(-0.5, 1.0)
    glVertex2f(-0.5, 0.6)  # duas faixas
    glVertex2f(-1.0, 0.6)
    glEnd()

    # Triângulo branco dentro do quadrado azul
    glBegin(GL_TRIANGLES)
    glColor3f(*branco)
    glVertex2f(-0.75, 0.95)   # topo
    glVertex2f(-0.95, 0.65)   # canto inferior esquerdo
    glVertex2f(-0.55, 0.65)   # canto inferior direito
    glEnd()

def main():
    janela = inicializar()
    while not glfw.window_should_close(janela):
        desenhar_bandeira()
        glfw.swap_buffers(janela)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()
