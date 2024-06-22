import pygame
import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
import pyassimp


def setup_lighting_and_camera():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 1, 2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    
    # Configuración de la cámara
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width/height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

def load_model(file_path):
    with pyassimp.load(file_path) as scene:
        if not scene.meshes:
            raise Exception("No meshes found in model file.")
        return scene

def draw_model(scene):
    for mesh in scene.meshes:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for index in face:  # Cambiado de face.indices a face
                glVertex3fv(mesh.vertices[index])
        glEnd()

def render_model(scene):

    global rotation_x 
    global rotation_y 

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)
    
    
    # Draw the model
    draw_model(scene)
    
    pygame.display.flip()

if __name__ == "__main__":
    pygame.init()

    title = "Solar System Travel"

    target_fps = 60
    (width, height) = (800, 600)
    flags = pygame.DOUBLEBUF | pygame.OPENGL
    screen = pygame.display.set_mode((width, height), flags)
    prev_time = time.time()

    rotation_x = 0
    rotation_y = 0

    model_path = "./Planets_INFO/Planets_OBJ/saturno.obj"  # Actualiza esta ruta a tu archivo de modelo
    scene = None
    with pyassimp.load(model_path) as loaded_scene:
        
        scene = loaded_scene

    setup_lighting_and_camera()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    rotation_y -= 60
                elif event.key == pygame.K_d:
                    rotation_y += 60
                elif event.key == pygame.K_w:
                    rotation_x -= 60
                elif event.key == pygame.K_s:
                    rotation_x += 60

        render_model(scene)
        
        curr_time = time.time()
        diff = curr_time - prev_time
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff)
        prev_time = curr_time
        pygame.display.set_caption("{0}, FPS: {1:.0f}".format(title, fps))

