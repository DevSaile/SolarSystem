import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import pyrr
from PIL import Image
from Load_OBJ import ObjLoader

vertex_src = """
#version 330
layout(location=0) in vec3 v_pos;
layout(location=1) in vec2 texture;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
out vec2 v_tex;
void main()
{
    gl_Position = projection * view * model * vec4(v_pos, 1);
    v_tex = texture;
}
"""

fragment_src = """
#version 330
out vec4 out_color;
in vec2 v_tex;
uniform sampler2D s_tex;
void main()
{
    out_color = texture(s_tex, v_tex);
}
"""

def win_resize(event):
    width, height = event.size
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

pygame.init()
screen = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption('window')

shaders = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

indices, data = ObjLoader.load_model("./Planets_INFO/Planets_OBJ/earth.obj")

VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

image = Image.open("./Planets_INFO/Planets_Texture/terraPRO.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
glGenerateMipmap(GL_TEXTURE_2D)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * data.itemsize, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * data.itemsize, ctypes.c_void_p(12))

model_loc = glGetUniformLocation(shaders, "model")
proj_loc = glGetUniformLocation(shaders, "projection")
view_loc = glGetUniformLocation(shaders, "view")

trans_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
scaler_mat = pyrr.Matrix44.from_scale(pyrr.Vector3([3, 3, 3]))
view_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1, 0]))
look_mat = pyrr.matrix44.create_look_at(pyrr.Vector3([-5, 1.5, 0]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

glClearColor(0, 0, 0.2, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

glUseProgram(shaders)
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, look_mat)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            win_resize(event)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rotx = pyrr.Matrix44.from_x_rotation(0 * pygame.time.get_ticks() / 1000.0)
    roty = pyrr.Matrix44.from_y_rotation(1.5 * pygame.time.get_ticks() / 1000.0)
    rotz = pyrr.Matrix44.from_z_rotation(0 * pygame.time.get_ticks() / 1000.0)
    rot_mat = roty * rotx * rotz
    model_mat = pyrr.matrix44.multiply(rot_mat, trans_mat)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model_mat)
    
    glDrawArrays(GL_TRIANGLES, 0, len(indices))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
