import pygame
import sys
import time
import glob
import numpy as np
from ctypes import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from LoadBackGround import load_shaders, load_cubemap, render

if __name__ == "__main__":

    title = "Solar System Travel"

    target_fps = 60
    (width, height) = (800, 600)
    flags = pygame.DOUBLEBUF | pygame.OPENGL
    screen = pygame.display.set_mode((width, height), flags)
    prev_time = time.time()
    rotation_x = 0
    rotation_y = 0
    rotation_step = 1

    cubemap = load_cubemap("./SpaceSkybox_INFO/TextureBackGround/")
    program = load_shaders("./SpaceSkybox_INFO/shaders/skybox.vert", "./SpaceSkybox_INFO/shaders/skybox.frag")

    moving = [False, False, False, False]

    # Cambiamos las teclas de flechas a WASD
    keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
    
    fov = 140
    fov_step = 10
    fov_range = (30, 150)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                try:
                    moving[keys.index(event.key)] = True
                except:
                    pass
                if event.key == pygame.K_SPACE:
                    fov += fov_step
                    fov_min, fov_max = fov_range
                    if fov > fov_max:
                        fov = fov_min
            elif event.type == pygame.KEYUP:
                try:
                    moving[keys.index(event.key)] = False
                except:
                    pass

        rotation_x += rotation_step * (moving[1] - moving[0])
        rotation_x %= 360
        rotation_y += rotation_step * (moving[3] - moving[2])
        rotation_y %= 360

        render(width, height, program, cubemap, rotation_x, rotation_y, fov)

        curr_time = time.time()
        diff = curr_time - prev_time
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff)
        prev_time = curr_time
        pygame.display.set_caption("{0}, FPS: {1:.0f} Yaw: {2}, Pitch: {3}, FOV: {4}".format(title, fps, rotation_x, rotation_y, fov))
