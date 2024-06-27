# Load_OBJ.py

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import pygame as pg

def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    """
    Compile and link shader modules to make a shader program.
    """
    with open(vertex_filepath, 'r') as f:
        vertex_src = f.readlines()

    with open(fragment_filepath, 'r') as f:
        fragment_src = f.readlines()

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))

    return shader

def load_mesh(filename: str) -> list[float]:
    """
    Load a mesh from an obj file.
    """
    v = []
    vt = []
    vn = []
    vertices = []

    with open(filename, "r") as file:
        line = file.readline()

        while line:
            words = line.split(" ")

            if words[0] == "v":
                v.append(read_vertex_data(words))
            elif words[0] == "vt":
                vt.append(read_texcoord_data(words))
            elif words[0] == "vn":
                vn.append(read_normal_data(words))
            elif words[0] == "f":
                read_face_data(words, v, vt, vn, vertices)

            line = file.readline()

    return vertices

def read_vertex_data(words: list[str]) -> list[float]:
    """
    Returns a vertex description.
    """
    return [float(words[1]), float(words[2]), float(words[3])]

def read_texcoord_data(words: list[str]) -> list[float]:
    """
    Returns a texture coordinate description.
    """
    return [float(words[1]), float(words[2])]

def read_normal_data(words: list[str]) -> list[float]:
    """
    Returns a normal vector description.
    """
    return [float(words[1]), float(words[2]), float(words[3])]

def read_face_data(words: list[str], v: list[list[float]], vt: list[list[float]],
                   vn: list[list[float]], vertices: list[float]) -> None:
    """
    Reads an edgetable and makes a face from it.
    """
    triangleCount = len(words) - 3

    for i in range(triangleCount):
        make_corner(words[1], v, vt, vn, vertices)
        make_corner(words[2 + i], v, vt, vn, vertices)
        make_corner(words[3 + i], v, vt, vn, vertices)

def make_corner(corner_description: str, v: list[list[float]], vt: list[list[float]],
                vn: list[list[float]], vertices: list[float]) -> None:
    """
    Composes a flattened description of a vertex.
    """
    v_vt_vn = corner_description.split("/")

    for element in v[int(v_vt_vn[0]) - 1]:
        vertices.append(element)
    for element in vt[int(v_vt_vn[1]) - 1]:
        vertices.append(element)
    for element in vn[int(v_vt_vn[2]) - 1]:
        vertices.append(element)

class Mesh:
    """
    A mesh that can represent an obj model.
    """
    def __init__(self, filename: str):
        """
        Initialize the mesh.
        """
        self.vertices = load_mesh(filename)
        self.vertex_count = len(self.vertices) // 8
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

    def arm_for_drawing(self) -> None:
        """
        Arm the triangle for drawing.
        """
        glBindVertexArray(self.vao)

    def draw(self) -> None:
        """
        Draw the triangle.
        """
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self) -> None:
        """
        Free any allocated memory.
        """
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

    def bind_texture(self, filepath: str) -> None:
        """
        Bind a texture to the mesh.
        """
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA', 1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

