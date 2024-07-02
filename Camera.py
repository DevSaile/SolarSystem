from OpenGL.GL import *
from pyrr import Matrix44, Vector3, Quaternion
import numpy as np

class Camera:
    def __init__(self, position=Vector3([0.0, 0.0, 3.0]), up=Vector3([0.0, 1.0, 0.0]), yaw=-90.0, pitch=0.0):
        self.position = position
        self.front = Vector3([0.0, 0.0, -1.0])
        self.up = up
        self.right = Vector3([1.0, 0.0, 0.0])
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        self.zoom = 45.0

        self.update_camera_vectors()

    def get_view_matrix(self):
        return Matrix44.look_at(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        if self.zoom >= 1.0 and self.zoom <= 45.0:
            self.zoom -= yoffset
        if self.zoom <= 1.0:
            self.zoom = 1.0
        if self.zoom >= 45.0:
            self.zoom = 45.0

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        front.y = np.sin(np.radians(self.pitch))
        front.z = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        self.front = front.normalized
        self.right = self.front.cross(self.world_up).normalized
        self.up = self.right.cross(self.front).normalized