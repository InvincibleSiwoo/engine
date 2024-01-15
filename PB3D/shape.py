from OpenGL.GLU import *
from pywavefront import Wavefront
from PB3D.math.vector import Vec3

entities = []

def mouse_pos(x, y):
    global selected_shape
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)

    y = viewport[3] - y
    click_pos = gluUnProject(x, y, 0.0, modelview, projection, viewport)

    return click_pos

class Shape:
    def __init__(self, file_path="cube", color=None, position=Vec3(0, 0, 0)):
        self.file_path = file_path
        self.color = color
        self.position = position
        self.selected = False
        if file_path and file_path.endswith(".obj"):
            self.load_obj(file_path)
            self.draw()
        elif file_path == "cube":
            self.vertices = [
                (1 + self.position.x, -1 + self.position.y, -1 + self.position.z),
                (1 + self.position.x, 1 + self.position.y, -1 + self.position.z),
                (-1 + self.position.x, 1 + self.position.y, -1 + self.position.z),
                (-1 + self.position.x, -1 + self.position.y, -1 + self.position.z),
                (1 + self.position.x, -1 + self.position.y, 1 + self.position.z),
                (1 + self.position.x, 1 + self.position.y, 1 + self.position.z),
                (-1 + self.position.x, -1 + self.position.y, 1 + self.position.z),
                (-1 + self.position.x, 1 + self.position.y, 1 + self.position.z)
            ]
            self.draw_cube()

    def load_obj(self, file_path):
        self.obj_mesh = Wavefront(file_path)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)

        if self.obj_mesh:
            self.draw_obj()
        else:
            self.draw_cube()

        glPopMatrix()

    def draw_cube(self):
        glBegin(GL_QUADS)
        for surface in ((0, 1, 2, 3), (3, 2, 7, 6), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)):
            for vertex_i in surface:
                vertex = self.vertices[vertex_i]
                if self.selected:
                    glColor3fv((1, 0, 0))  # Red if selected
                elif self.color:
                    glColor3fv(self.color)
                glVertex3fv(vertex)
        glEnd()

    def draw_obj(self):
        glEnable(GL_DEPTH_TEST)

        if self.selected:
            glColor3fv((1, 0, 0))  # Red if selected
        elif self.color:
            glColor3fv(self.color)

        glBegin(GL_TRIANGLES)
        for face in self.obj_mesh.mesh_list[0].faces:
            for vertex_i in face:
                vertex = self.obj_mesh.mesh_list[0].vertices[vertex_i]
                glVertex3fv(vertex)
        glEnd()

        glDisable(GL_DEPTH_TEST)

    def is_clicked(self, click_pos):
        if self.obj_mesh:
            min_x = min(v[0] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.x
            max_x = max(v[0] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.x
            min_y = min(v[1] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.y
            max_y = max(v[1] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.y
            min_z = min(v[2] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.z
            max_z = max(v[2] for v in self.obj_mesh.mesh_list[0].vertices) + self.position.z
        else:
            min_x = min(v[0] for v in self.vertices) + self.position.x
            max_x = max(v[0] for v in self.vertices) + self.position.x
            min_y = min(v[1] for v in self.vertices) + self.position.y
            max_y = max(v[1] for v in self.vertices) + self.position.y
            min_z = min(v[2] for v in self.vertices) + self.position.z
            max_z = max(v[2] for v in self.vertices) + self.position.z

        return min_x <= click_pos[0] <= max_x and min_y <= click_pos[1] <= max_y and min_z <= click_pos[2] <= max_z

    def get_position(self):
        return self.position

    def set_position(self, position):
        if isinstance(position, tuple):
            self.position = Vec3(position[0], position[1], position[2])
        elif isinstance(position, Vec3):
            self.position = position

    def move(self, x, y, z):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(x, y, z)

        if self.file_path and self.file_path.endswith(".obj"):
            self.load_obj(self.file_path)
        elif self.file_path == "cube":
            self.vertices = [
                (1 + self.position.x, -1 + self.position.y, -1 + self.position.z),
                (1 + self.position.x, 1 + self.position.y, -1 + self.position.z),
                (-1 + self.position.x, 1 + self.position.y, -1 + self.position.z),
                (-1 + self.position.x, -1 + self.position.y, -1 + self.position.z),
                (1 + self.position.x, -1 + self.position.y, 1 + self.position.z),
                (1 + self.position.x, 1 + self.position.y, 1 + self.position.z),
                (-1 + self.position.x, -1 + self.position.y, 1 + self.position.z),
                (-1 + self.position.x, 1 + self.position.y, 1 + self.position.z)
            ]
            self.draw_cube()

class Shape2d:
    def __init__(self, file_path="square", color=None, position=(0, 0)):
        self.file_path = file_path
        self.color = color
        self.position = position
        self.selected = False

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0.0)

        if self.selected:
            glColor3fv((1, 0, 0))
        elif self.color:
            glColor3fv(self.color)

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(50, 0)
        glVertex2f(50, 50)
        glVertex2f(0, 50)
        glEnd()

        glPopMatrix()

    def is_clicked(self, click_pos):
        min_x = self.position[0]
        max_x = self.position[0] + 50
        min_y = self.position[1]
        max_y = self.position[1] + 50

        return min_x <= click_pos[0] <= max_x and min_y <= click_pos[1] <= max_y

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

from OpenGL.GL import *

class Light:
    def __init__(self, position=(0, 0, 0), ambient=1, diffuse=1, specular=1):
        self.position = position
        self.ambient = [ambient, ambient, ambient, 1.0]
        self.diffuse = [diffuse, diffuse, diffuse, 1.0]
        self.specular = [specular, specular, specular, 1.0]

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        self.update()

    def update(self):
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)

    def set_position(self, position):
        self.position = position
        self.update()

    def set_ambient(self, ambient):
        self.ambient = [ambient, ambient, ambient, 1.0]
        self.update()

    def set_diffuse(self, diffuse):
        self.diffuse = [diffuse, diffuse, diffuse, 1.0]
        self.update()

    def set_specular(self, specular):
        self.specular = [specular, specular, specular, 1.0]
        self.update()