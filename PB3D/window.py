import pygame
from pygame.locals import *
from OpenGL.GL import glTranslatef, glClear, glRotatef, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glOrtho, glClearColor
from OpenGL.GLU import gluPerspective
from PB3D.math import Vec4

from OpenGL.GL import glEnable, GL_DEPTH_TEST


def init(size: tuple[int, int], color: tuple[int, int, int, int]):
    """
    This is a function that initializes the 3d mode of PB3D. Here you can adjust the color and size.

    :param size:
    :param color:
    :return:
    """
    pygame.init()
    pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (size[0] / size[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glClearColor(*color)


def init_2d(size: tuple[int, int]):
    """
    This is a function that initializes the 2d mode of PB3D. Here you can adjust the color and size.
    :param size:
    :return:
    """
    pygame.init()
    pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
    glOrtho(0, size[0], size[1], 0, -1, 1)

def update():
    pygame.display.flip()

def clean():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def turn(vec: Vec4):
    """
    This is the function responsible for adjusting the field of view in PB3D
    :param vec
    :return:
    """
    glRotatef(vec.w, vec.x, vec.y, vec.z)


def loop(func1=None, func2=None):
    """
    This is a function that manages loops in PB3D. Basically, you can install a model in func1 and use the keyboard in func2.
    :param func1:
    :param func2:
    :return:
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if func2 != None:
                    func2(event)
        clean()
        if func1 != None:
            func1()
        update()

Event = pygame.event.Event