# LoadPlanets.py
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
import pygame as pg
from OpenGL.GL import *
from Load_OBJ import create_shader, Mesh

class App:
    """
    For now, the app will be handling everything.
    Later on we'll break it into subcomponents.
    """
    def __init__(self):

        self.camera_position = np.array([0.0, 0.0, 2.0], dtype=np.float32)  # Inicializa la posición 
        self._set_up_pygame()
        self._set_up_timer()
        self._set_up_opengl()
        self._create_assets()
        self._set_onetime_uniforms()
        self._get_uniform_locations()

    def _set_up_pygame(self) -> None:
        """
        Initialize and configure pygame.
        """
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)

    def _set_up_timer(self) -> None:
        """
        Set up the app's timer.
        """
        self.clock = pg.time.Clock()

    def _set_up_opengl(self) -> None:
        """
        Configure any desired OpenGL options
        """
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

    def _create_assets(self) -> None:
        """
        Create all of the assets needed for drawing.
        """
        self.planet_mesh = Mesh("Planets_INFO/Planets_OBJ/earth.obj")
        self.planet_mesh.bind_texture("Planets_INFO/Planets_Texture/terraPRO.png")  # Load texture here
        self.shader = create_shader(
            vertex_filepath="Planets_INFO/Planets_Shaders/Vertex.txt",
            fragment_filepath="Planets_INFO/Planets_Shaders/Fragment.txt")

    def _set_onetime_uniforms(self) -> None:
        """
        Some shader data only needs to be set once.
        """
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

    def _get_uniform_locations(self) -> None:
        """
        Query and store the locations of shader uniforms
        """
        glUseProgram(self.shader)
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

    def run(self) -> None:
            """ Run the app """

            keys = pg.key.get_pressed()

            running = True
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif keys[pg.KEYDOWN]:

                        # Si la tecla "S" está presionada, aleja la cámara
                        self.camera_position[2] -= 0.1  # Puedes ajustar el valor según tus necesidades

                self._update()

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glUseProgram(self.shader)

                glUniformMatrix4fv(
                    self.modelMatrixLocation, 1, GL_FALSE,
                    self._get_model_transform()
                )

                self.planet_mesh.arm_for_drawing()
                self.planet_mesh.draw()

                pg.display.flip()
                self.clock.tick(60)


    def quit(self) -> None:
        """ Cleanup the app, run exit code """
        self.planet_mesh.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

    def _update(self) -> None:
        """ Update the app state """
        pass  # Placeholder for now

    def _get_model_transform(self) -> np.ndarray:
        """ Returns the model transformation matrix """
        return pyrr.matrix44.create_identity(dtype=np.float32)

if __name__ == "__main__":
    my_app = App()
    my_app.run()
    my_app.quit()
