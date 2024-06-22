import pygame
import sys
import time
import glob
import numpy as np
from ctypes import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *

def load_shaders(vert_url, frag_url):

    vert_str = "\n".join(open(vert_url).readlines())
    frag_str = "\n".join(open(frag_url).readlines())
    vert_shader = shaders.compileShader(vert_str, GL_VERTEX_SHADER)
    frag_shader = shaders.compileShader(frag_str, GL_FRAGMENT_SHADER)
    program = shaders.compileProgram(vert_shader, frag_shader)
    return program

def load_cubemap(folder_url):

    tex_id = glGenTextures(1)

    face_order = ["front", "top", "bottom", "right", "left", "back"]
    face_urls = sorted(glob.glob(folder_url + "*"))
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_CUBE_MAP, tex_id)

    for i, face in enumerate(face_order):

        face_url = [face_url for face_url in face_urls if face in face_url.lower()][0]
        face_image = pygame.image.load(face_url).convert()
        face_width, face_height = face_image.get_size()
        face_surface = pygame.image.tostring(face_image, 'RGB')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, face_width, face_height, 0, GL_RGB, GL_UNSIGNED_BYTE, face_surface)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    return tex_id


def render(width, height, program, cubemap, rotation_x, rotation_y, fov):

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_CUBE_MAP)

    skybox_right = [1, -1, -1, 1, -1,  1, 1,  1,  1, 1,  1,  1, 1,  1, -1, 1, -1, -1]
    skybox_left = [-1, -1,  1, -1, -1, -1, -1,  1, -1, -1,  1, -1, -1,  1,  1, -1, -1,  1]
    skybox_top = [-1,  1, -1, 1,  1, -1, 1,  1,  1, 1,  1,  1, -1,  1,  1, -1,  1, -1]
    skybox_bottom = [-1, -1, -1, -1, -1,  1, 1, -1, -1, 1, -1, -1, -1, -1,  1, 1, -1,  1]
    skybox_back = [-1,  1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1,  1, -1, -1,  1, -1]
    skybox_front = [-1, -1,  1, -1,  1,  1, 1,  1,  1, 1,  1,  1, 1, -1,  1, -1, -1,  1]

    skybox_vertices = np.array([skybox_right, skybox_left, skybox_top, skybox_bottom, skybox_back, skybox_front], dtype=np.float32).flatten()
    skybox_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, skybox_vbo)
    glBufferData(GL_ARRAY_BUFFER, skybox_vertices.nbytes, skybox_vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, float(width)/height, 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotate(rotation_y, 1, 0, 0)
    glRotate(rotation_x, 0, 1, 0)

    glUseProgram(program)
    glDepthMask(GL_FALSE)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap)
    glEnableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, skybox_vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDisableClientState(GL_VERTEX_ARRAY)
    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
    glDepthMask(GL_TRUE)
    glUseProgram(0)

    pygame.display.flip()



