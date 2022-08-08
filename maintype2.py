import pygame
import math
import player

window = pygame.display.set_mode((500, 500))

lines = []
g_lines = []
tri_lines = []
intersection_points = []

average_x = 0
average_y = 0

B1 = 0
B2 = 0
A1 = 0
A2 = 0
C1 = 0
C2 = 0

speed_x = 0
speed_y = 0
tri_x = 300
tri_y = 10

squares = [(0, 300), (500, 400), (500, 500), (0, 500), (0, 0), (200, 0), (200, 100), (0, 100)]

triangle = [(-50, -50), (50, -50), (0, 50)]

Tri = [(50, 100), (100, 1), (1, 1)]

running = True

count = 0

angle_v = 0
angle = 3.14159

detect = 0

rep = 0

# A = y2 - y1
# B = x1 - x2
# C = A(x1) - B(y1)


def collide_x():
    global tri_x, speed_x
    if detect_collision():
        tri_x, speed_x = player.collide_x(speed_x, tri_x)


def collide_y():
    global tri_y, speed_y
    if detect_collision():
        tri_y, speed_y = player.collide_y(speed_y, tri_y)
        tri_y += 1
        if detect_collision():
            if keys[pygame.K_UP]:
                speed_y -= 10
        tri_y -= 1
        physics()


def collide_rot():
    global angle, angle_v
    if detect_collision():
        angle, angle_v = player.collide_rotate(angle_v, angle)


def setup(tri=(), squ=()):
    global tri_lines
    global g_lines
    tri_lines = []
    g_lines = []

    if tri != 0:
        tri_lines.append((tri[0], tri[1]))
        tri_lines.append((tri[1], tri[2]))
        tri_lines.append((tri[2], tri[0]))
        # tri_lines.append((tri[0], tri[1]))
    r = 0
    if squ != 0:
        while r < len(squ)/4:
            r += 1
            g_lines.append((squ[r * 4 - 4], squ[r * 4 - 3]))
            g_lines.append((squ[r * 4 - 3], squ[r * 4 - 2]))
            g_lines.append((squ[r * 4 - 2], squ[r * 4 - 1]))
            g_lines.append((squ[r * 4 - 1], squ[r * 4 - 4]))

    return


def detect_collision():
    global count, intersection_points, g_lines, triangle, tri_x, tri_y, tri_lines, Tri
    count = 0
    for i in triangle:
        Tri[count] = (i[0] * math.cos(angle) - i[1] * math.sin(angle) + tri_x,
                      i[0] * math.sin(angle) + i[1] * math.cos(angle) + tri_y)
        count += 1
    setup(Tri, squares)

    intersection_points = []
    for i in tri_lines:
        segment_intersection(i, g_lines)

    for e in intersection_points:
        pygame.draw.circle(window, (200, 10, 10), (e[0], -e[1]), 5)

    return intersection_points


def rotate():
    global angle, angle_v
    if keys[pygame.K_m]:
        angle_v = player.move_rot(.005, angle_v)

    if keys[pygame.K_n]:
        angle_v = player.move_rot(-.005, angle_v)

    angle, angle_v = player.slow_x(.9, angle_v, angle)


def move_x():
    global speed_x, tri_x
    if keys[pygame.K_RIGHT]:
        speed_x = player.move_x(1, speed_x)

    if keys[pygame.K_LEFT]:
        speed_x = player.move_x(-1, speed_x)

    tri_x, speed_x = player.slow_x(.9, speed_x, tri_x)


def gravity():
    global tri_y, speed_y
    tri_y, speed_y = player.slow_y(.1, speed_y, tri_y)


def draw():

    for e in tri_lines:
        pygame.draw.line(window, (100, 100, 100), e[0], e[1])

    for e in g_lines:
        pygame.draw.line(window, (100, 100, 100), e[0], e[1])

    for e in intersection_points:
        pygame.draw.circle(window, (200, 10, 10), (e[0], -e[1]), 5)


def calc_intersect(lin=(), ground=()):
    global A1
    global B1
    global A2
    global B2
    global C1
    global C2
    global intersection_points

    if lin != 0:
        p0 = lin[0]
        p1 = lin[1]

        A1 = p0[1] - p1[1]
        B1 = p0[0] - p1[0]
        C1 = A1 * p0[0] - B1 * p0[1]
        # A = y2 - y1
        # B = x1 - x2
        # C = A(x1) - B(y1)

        for j in ground:
            p2 = j[0]
            p3 = j[1]

            A2 = p3[1] - p2[1]
            B2 = p2[0] - p3[0]
            C2 = A2 * p2[0] - B2 * p2[1]

            d = A1 * B2 - A2 * B1

            if d == 0:
                return

            if (B2 * C1 - B1 * C2) / d and (A1 * C2 - A2 * C1) / d:
                intersection_points.append(((B2 * C1 - B1 * C2) / d, (A1 * C2 - A2 * C1) / d))
    return intersection_points


def segment_intersection(lin=(), ground=(), y=0):
    global A1
    global B1
    global A2
    global B2
    global C1
    global C2
    global intersection_points
    global detect

    if lin != 0:
        p0 = lin[0]
        p1 = lin[1]

        A1 = p0[1] - p1[1]
        B1 = p0[0] - p1[0]
        C1 = A1 * p0[0] - B1 * p0[1]

        for j in ground:
            p2 = j[0]
            p3 = j[1]

            A2 = p2[1] - p3[1]
            B2 = p2[0] - p3[0]
            C2 = A2 * p2[0] - B2 * p2[1]
            d = A1 * B2 - A2 * B1

            if d != 0:
                intersect_x = (B2 * C1 - B1 * C2) / d
                intersect_y = (A1 * C2 - A2 * C1) / d

                ry0 = intersect_y
                rx0 = intersect_x

                detect = 0

                if detect == 0 and p0[0] < rx0 < p1[0]:
                    detect = 1

                if detect == 0 and p1[0] < rx0 < p0[0]:
                    detect = 1

                if detect == 0 and p0[1] < -ry0 < p1[1]:
                    detect = 1

                if detect == 0 and p1[1] < -ry0 < p0[1]:
                    detect = 1

                if detect == 1 and p2[0] < rx0 < p3[0]:
                    detect = 2

                if detect == 1 and p3[0] < rx0 < p2[0]:
                    detect = 2

                if detect == 1 and p2[1] < -ry0 < p3[1]:
                    detect = 2

                if detect == 1 and p3[1] < -ry0 < p2[1]:
                    detect = 2

                if detect == 2:
                    intersection_points.append((intersect_x,
                                                intersect_y))

    return intersection_points


def physics():
    global intersection_points, angle_v, average_x, rep, average_y
    average_x = 0
    average_y = 0
    rep = 0

    for e in intersection_points:
        average_x += e[0]
        if e[1]:
            average_y += 100/e[1]
        rep += 1

    if rep:
        average_x = average_x / rep
        average_y = average_y / rep

    # print(tri_x, tri_y)
    # print(average_x, average_y)

    angle_v += (tri_x - average_x + average_y)/1000
    # print(angle_v)


setup(triangle, squares)


while running:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    window.fill((0, 0, 20))

    draw()

    move_x()

    collide_x()

    rotate()

    collide_rot()

    gravity()

    collide_y()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
