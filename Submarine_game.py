import math

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


def draw_circle(r, c1, c2):
    d = 5 - 4 * r
    x = 0
    y = r

    draw_8_way(x, y, c1, c2)

    while x < y:

        if d < 0:
            d = d + 2 * x + 3
            x += 1

        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y = y - 1

        draw_8_way(x, y, c1, c2)


def draw_8_way(x, y, c1, c2):
    draw_points(x + c1, y + c2)

    draw_points(y + c1, x + c2)

    draw_points(y + c1, -x + c2)

    draw_points(x + c1, -y + c2)

    draw_points(-x + c1, -y + c2)

    draw_points(-y + c1, -x + c2)

    draw_points(-y + c1, x + c2)

    draw_points(-x + c1, y + c2)


def draw_points(x, y):
    global pixel_size
    glPointSize(pixel_size)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 1500, 750)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1500, 0.0, 750, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_rectangle(x1, y1, x2, y2):
    glColor3f(135 / 255, 206 / 255, 235 / 255)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)  # Bottom-left vertex
    glVertex2f(x1, y2)  # Top-left vertex
    glVertex2f(x2, y2)  # Top-right vertex
    glVertex2f(x2, y1)  # Bottom-right vertex
    glEnd()


def midptellipse(rx, ry, xc, yc):
    x = 0
    y = ry

    # Initial decision parameter of region 1
    d1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    # For region 1
    while (dx < dy):

        # Print points based on 4-way symmetry
        draw_points(x + xc, y + yc)
        draw_points(-x + xc, y + yc)
        draw_points(x + xc, -y + yc)
        draw_points(-x + xc, -y + yc)

        # Checking and updating value of
        # decision parameter based on algorithm
        if (d1 < 0):
            x += 1
            dx = dx + (2 * ry * ry)
            d1 = d1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    # Decision parameter of region 2
    d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))

    # Plotting points of region 2
    while (y >= 0):

        # printing points based on 4-way symmetry
        draw_points(x + xc, y + yc)
        draw_points(-x + xc, y + yc)
        draw_points(x + xc, -y + yc)
        draw_points(-x + xc, -y + yc)

        # Checking and updating parameter
        # value based on algorithm
        if (d2 > 0):
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)


def draw_cloud(x, y):
    glColor3f(1.0, 1.0, 1.0)
    a = 20
    b = 15
    while b > 1:
        midptellipse(a, b, x + 5, y + 7)
        a -= 1
        b -= 1
    a = 20
    b = 15
    while b > 1:
        midptellipse(a, b, x - 8, y - 8)
        a -= 1
        b -= 1

    a = 20
    b = 15
    while b > 1:
        midptellipse(a, b, x + 8, y - 8)
        a -= 1
        b -= 1


def setBackground():
    glClearColor(0.0, 119 / 255, 190 / 255, 1.0)
    draw_rectangle(0, 750, 1500, 600)
    draw_cloud(50, 700)
    draw_cloud(500, 650)
    draw_cloud(1000, 720)
    draw_cloud(1300, 630)


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                return x0, y0, x1, y1, 0
            else:
                return x0, -y0, x1, -y0, 7
        else:
            if dy >= 0:
                return -x0, y0, -x1, y1, 3
            else:
                return -x0, -y0, -x1, -y1, 4
    else:
        if dx >= 0:
            if dy >= 0:
                return y0, x0, y1, x1, 1
            else:
                return -y0, x0, -y1, x1, 6
        else:
            if dy >= 0:
                return y0, -x0, y1, -x1, 2
            else:
                return -y0, -x0, -y1, -x1, 5


def draw(x, y, zone):
    glPointSize(2)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    if zone == 0:
        glVertex2f(x, y)
    if zone == 1:
        glVertex2f(y, x)
    if zone == 2:
        glVertex2f(-y, x)
    if zone == 3:
        glVertex2f(-x, y)
    if zone == 4:
        glVertex2f(-x, -y)
    if zone == 5:
        glVertex2f(-y, -x)
    if zone == 6:
        glVertex2f(y, -x)
    if zone == 7:
        glVertex2f(x, -y)

    glEnd()


def draw_line(x0, y0, x1, y1):
    x0, y0, x1, y1, zone = findZone(x0, y0, x1, y1)
    dy = y1 - y0
    dx = x1 - x0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x0
    y = y0
    draw(x, y, zone)
    while x <= x1:
        if d <= 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
        draw(x, y, zone)


def submarine(i):
    # border
    # ===============================================================================================================
    glColor3f(0, 0, 0.0)
    midptellipse(71, 41, 100 + i, 620 - i)  # body

    glColor3f(0, 0, 0.0)
    midptellipse(31, 11, 100 + i, 660 - i)  # lower bump

    glColor3f(0, 0, 0.0)
    midptellipse(21, 11, 100 + i, 670 - i)  # upper bump

    # body
    # ===============================================================================================================
    glColor3f(1.0, 1.0, 0.0)
    a = 70
    b = 40
    while b > 0:
        midptellipse(a, b, 100 + i, 620 - i)
        a -= 1
        b -= 1

    # middle window
    # ===============================================================================================================
    middle_window_center = (100 + i, 620 - i)
    glColor3f(1.0, 0.5, 0.0)
    r = 15
    while r > 10:
        draw_circle(r, 100 + i, 620 - i)
        r -= 1
    glColor3f(0.7, 0.7, 0.7)
    while r > 0:
        draw_circle(r, 100 + i, 620 - i)
        r -= 1
    glColor3f(0, 0, 0.0)
    draw_circle(16, 100 + i, 620 - i)
    # right window
    # ===============================================================================================================

    glColor3f(1.0, 0.5, 0.0)
    r = 13
    while r > 9:
        draw_circle(r, 140 + i, 628 - i)
        r -= 1
    glColor3f(0.7, 0.7, 0.7)
    while r > 0:
        draw_circle(r, 140 + i, 628 - i)
        r -= 1
    glColor3f(0, 0, 0.0)
    draw_circle(14, 140 + i, 628 - i)

    # left window
    # ===============================================================================================================
    glColor3f(1.0, 0.5, 0.0)
    r = 13
    while r > 9:
        draw_circle(r, 60 + i, 628 - i)
        r -= 1
    glColor3f(0.7, 0.7, 0.7)
    while r > 0:
        draw_circle(r, 60 + i, 628 - i)
        r -= 1

    glColor3f(0, 0, 0.0)
    draw_circle(14, 60 + i, 628 - i)

    # lower bump
    # ===============================================================================================================
    glColor3f(1.0, 1.0, 0.0)
    a = 30
    b = 10
    while b > 0:
        midptellipse(a, b, 100 + i, 660 - i)
        a -= 1
        b -= 1

    # upper bump
    # ===============================================================================================================

    glColor3f(1.0, 1.0, 0.0)
    a = 20
    b = 10
    while b > 0:
        midptellipse(a, b, 100 + i, 670 - i)
        a -= 1
        b -= 1

    # vertical pipe
    # ===============================================================================================================

    glColor3f(1.0, 1.0, 0.0)
    x = middle_window_center[0] - 5
    y = middle_window_center[1] + 50
    width = 10
    height = 30
    while width > 0:
        draw_line(x + width, y, x + width, y + height)
        width -= 1

    # horizontal pipe
    # ===============================================================================================================

    x = middle_window_center[0] - 5
    y = middle_window_center[1] + 80
    width = 20
    height = 10
    while width > 0:
        draw_line(x + width, y, x + width, y + height)
        width -= 1
    # proppeler pipe
    # ===============================================================================================================
    x = middle_window_center[0] - 90
    y = middle_window_center[1] - 10
    width = 20
    height = 5
    while width > 0:
        draw_line(x + width, y, x + width, y + height)
        width -= 1

    # proppeler
    # ===============================================================================================================
    global pixel_size
    pixel_size = 4
    fixed_x = middle_window_center[0] - 90
    fixed_y = middle_window_center[1] - 6
    offset = transform_proppeler()
    moving_point_x = middle_window_center[0] - 90 + offset[0]
    moving_point_y = middle_window_center[1] - 6 + offset[1]
    draw_line(fixed_x, fixed_y, moving_point_x, moving_point_y)

    fixed_x = middle_window_center[0] - 90
    fixed_y = middle_window_center[1] - 6
    offset = transform_proppeler()
    moving_point_x = middle_window_center[0] - 90 - offset[0]
    moving_point_y = middle_window_center[1] - 6 - offset[1]
    draw_line(fixed_x, fixed_y, moving_point_x, moving_point_y)

    pixel_size = 2


def transform_proppeler():
    global angle
    angle += 2

    radian_angle = math.radians(angle)
    a = math.cos(radian_angle)
    b = math.sin(radian_angle)

    r = np.array([[a, -b, 0],
                  [b, a, 0],
                  [0, 0, 1]])

    v1 = np.array([[10],
                   [10],
                   [1]])
    # Apply rotation transformation
    v11 = np.matmul(r, v1)
    return v11[0][0], v11[1][0]

def titanic():

    glColor3f(1,1,1)
    draw_line(1500,160,1100,160)

    glColor3f(0.2,0.2,0.2)
    draw_line(1500,160,1100,160)



    for i in range(400):

        draw_line(1200+i,80,1100,160)

    for i in range(80):

        draw_line(1500,80+i,1100,160)

    glColor3f(1.0,1.0,1.0)
    draw_circle(10,1200,130)

    draw_circle(10, 1250, 130)
    draw_circle(10, 1300, 130)
    draw_circle(10, 1350, 130)

    for i in range(10):

        glColor3f(1.0, 1.0, 1.0)
        draw_circle(10-i, 1200, 130)

        draw_circle(10-i, 1250, 130)
        draw_circle(10-i, 1300, 130)
        draw_circle(10-i, 1350, 130)

    for i in range(300):
        glColor(0.36,0.25,0.20)
        draw_line(1200+i,162,1200+i,180)

    for i in range(50):
        glColor3f(0,0,0)
        draw_line(1300+i,182,1300+i,210)


def lower_surface():

    glColor3f(0.5, 0.35, 0.05)
    for i in range(60):
        draw_line(0,0+i,1500,0+i)
    for i in range(50):

        draw_line(1000,60,1500,60+i)
def submarine_game():
    pass


def showScreen():
    global i
    glClearColor(0.0, 119 / 255, 190 / 255, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0)  # konokichur color set (RGB)
    i += 3
    #input("player1:)
    #input()
    setBackground()
    submarine(i)
    submarine_game()
    titanic()
    lower_surface()


    glutSwapBuffers()
    time.sleep(0.01)  # Adjust the delay for the desired animation speed
    glutPostRedisplay()


pixel_size = 1

angle = 0
i = 0
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1500, 750)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(showScreen)

glutMainLoop()
