import glfw
from OpenGL.GL import *
import ShaderLoader 
import numpy as np
import pyrr
from pyrr import matrix44, vector3
import LoadTexture #Esta de aqui es TextureLoader
from Camera import Camera #Esta de aqui es Camara.py
from PIL import Image
from Load_OBJ import *
from LoadPlanets import planets
import random
import math
import pygame

# Inicializa pygame 
pygame.init()
sound = pygame.mixer.Sound('sonido.mp3')

cam = Camera()
keys = [False] * 1024
lastX, lastY = 640, 360
first_mouse = True

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False

def do_movement(window):

    
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        cam.process_keyboard("FORWARD", 4.05)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        cam.process_keyboard("LEFT", 4.05)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        cam.process_keyboard("RIGHT", 4.05)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        cam.process_keyboard("BACKWARD", 4.05)
    

# Callbacks for mouse input
def mouse_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos  # reversed since y-coordinates go from bottom to top
    last_x = xpos
    last_y = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def scroll_callback(window, xoffset, yoffset):

    cam.process_mouse_scroll(yoffset)

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():
    if not glfw.init():
        return

    w_width, w_height = 800, 600
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "Solar System", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    # Set callbacks for mouse input
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    obj = ObjLoader()
    obj.load_model("./Planets_INFO/sphere.obj")

    texture_offset = len(obj.vertex_index) * 12
    normal_offset = (texture_offset + len(obj.texture_index) * 8)

    shader = ShaderLoader.compile_shader("./shaders/main_vert.vs", "./shaders/main_frag.fs")

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position) 

    texCoords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))
    glEnableVertexAttribArray(texCoords)

    normals = glGetAttribLocation(shader, "vertNormal")
    glVertexAttribPointer(normals, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(normal_offset))
    glEnableVertexAttribArray(normals)

    for planet in planets:

        texture = LoadTexture.load_texture(planets[planet]['image_path'])
        planets[planet]['texture'] = texture

        if planet == 'sun' or planet == 'stars':

            distance_from_sun = planets[planet]['distance_from_sun']
            planets[planet]['initial_position'] = [distance_from_sun, 0.0, distance_from_sun]

        else:

            distance_from_sun = 30.0 + planets[planet]['distance_from_sun']
            x = round(random.uniform(-distance_from_sun, distance_from_sun), 3)
            z = round(math.sqrt((distance_from_sun ** 2) - (x ** 2)), 3)
            planets[planet]['initial_position'] = [x, 0.0, z]

    glEnable(GL_TEXTURE_2D)
    glUseProgram(shader)

    glClearColor(0.0, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 10000.0)
    scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    normal_loc = glGetUniformLocation(shader, "normalMatrix")
    scale_loc = glGetUniformLocation(shader, "scale")
    scale_planet_loc = glGetUniformLocation(shader, "scale_planet")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scale)

    Global_ambient_loc = glGetUniformLocation(shader, "Global_ambient")
    Light_ambient_loc = glGetUniformLocation(shader, "Light_ambient")
    Light_diffuse_loc = glGetUniformLocation(shader, "Light_diffuse")
    Light_specular_loc = glGetUniformLocation(shader, "Light_specular")
    Light_location_loc = glGetUniformLocation(shader, "Light_location")
    Material_ambient_loc = glGetUniformLocation(shader, "Material_ambient")
    Material_diffuse_loc = glGetUniformLocation(shader, "Material_diffuse")
    Material_specular_loc = glGetUniformLocation(shader, "Material_specular")
    Material_shininess_loc = glGetUniformLocation(shader, "Material_shininess")

    glUniform4f(Global_ambient_loc, 0.8, 0.8, 0.9, 0.1)
    glUniform4f(Light_ambient_loc, 0.3, 0.3, 0.3, 1.0)
    glUniform4f(Light_diffuse_loc, 0.25, 0.25, 0.25, 1.0)
    glUniform4f(Light_specular_loc, 0.9, 0.9, 0.9, 1.0)
    glUniform3f(Light_location_loc, 0, 0, 0)


    while not glfw.window_should_close(window):

        glfw.poll_events()
        do_movement(window)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        time = glfw.get_time()

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        sound.play()


        for planet in planets:
            
            glBindTexture(GL_TEXTURE_2D, planets[planet]['texture'])
            revolution_speed = time * planets[planet]['revolution_ratio_relative_to_earth']
            rotation_speed = time * planets[planet]['rotation_ratio_relative_to_earth']
            scale_factor = planets[planet]['size_ratio_relative_to_earth']
            scale_planet = matrix44.create_from_scale(pyrr.Vector3([scale_factor, scale_factor, scale_factor]))
            glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

            model = matrix44.create_from_translation(pyrr.Vector3(planets[planet]['initial_position']))
            revolution = matrix44.create_from_y_rotation(revolution_speed)
            rotation = matrix44.create_from_y_rotation(rotation_speed)
            model = matrix44.multiply(model, revolution)
            model = matrix44.multiply(rotation, model)

            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

            modelView = np.matmul(view, model)
            modelView33 = modelView[0:-1, 0:-1]
            normalMatrix = np.transpose(np.linalg.inv(modelView33))
            glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

            a, b, c, d = planets[planet]['Material_ambient']
            glUniform4f(Material_ambient_loc, a, b, c, d)
            a, b, c, d = planets[planet]['Material_diffuse']
            glUniform4f(Material_diffuse_loc, a, b, c, d)
            a, b, c, d = planets[planet]['Material_specular']
            glUniform4f(Material_specular_loc, a, b, c, d)
            s = planets[planet]['Material_shininess'][0]
            glUniform1f(Material_shininess_loc, s)

            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
