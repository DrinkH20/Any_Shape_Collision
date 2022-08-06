import pygame
import math

window = pygame.display.set_mode((500, 500))

lines = []
g_lines = []
tri_lines = []
intersection_points = []

B1 = 0
B2 = 0
A1 = 0
A2 = 0
C1 = 0
C2 = 0

squares = [(100, 100), (200, 100), (200, 200), (100, 200), (200, 100), (400, 100), (400, 50), (300, 200)]

triangle = [(-50, -50), (50, -50), (0, 50)]

Tri = [(50, 100), (100, 1), (1, 1)]

running = True

count = 0

tri_x = 10
tri_y = 10

angle = 0


# A = y2 - y1
# B = x1 - x2
# C = A(x1) - B(y1)


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


def segment_intersection(lin=(), ground=()):
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

                ry0 = p0[1] + intersect_y
                ry00 = p1[1] + intersect_y
                rx0 = p0[0] - intersect_x
                rx00 = p1[0] - intersect_x

                ry1 = p2[1] + intersect_y
                ry11 = p3[1] + intersect_y
                rx1 = p2[0] - intersect_x
                rx11 = p3[0] - intersect_x

                if ry0 <= p0[1] - p1[1] or ry00 <= p1[1] - p0[1]:
                    if ry0 >= p0[1] - p1[1] or ry00 >= p1[1] - p0[1]:

                        if rx0 <= p0[0] - p1[0] or rx00 <= p1[0] - p0[0]:
                            if rx0 >= p0[0] - p1[0] or rx00 >= p1[0] - p0[0]:

                                if ry1 <= p2[1] - p3[1] or ry11 <= p3[1] - p2[1]:
                                    if ry1 >= p2[1] - p3[1] or ry11 >= p3[1] - p2[1]:

                                        if rx1 <= p2[0] - p3[0] or rx11 <= p3[0] - p2[0]:
                                            if rx1 >= p2[0] - p3[0] or rx11 >= p3[0] - p2[0]:

                                                intersection_points.append(((B2 * C1 - B1 * C2) / d,
                                                                            (A1 * C2 - A2 * C1) / d))

    return intersection_points


setup(triangle, squares)


while running:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    window.fill((0, 0, 20))

    for i in tri_lines:
        pygame.draw.line(window, (100, 100, 100), i[0], i[1])
    for i in g_lines:
        pygame.draw.line(window, (100, 100, 100), i[0], i[1])

    for i in intersection_points:
        pygame.draw.circle(window, (200, 10, 10), (i[0], -i[1]), 5)

    if keys[pygame.K_RIGHT]:
        tri_x += 10

    if keys[pygame.K_LEFT]:
        tri_x -= 10

    if keys[pygame.K_UP]:
        tri_y -= 10

    if keys[pygame.K_DOWN]:
        tri_y += 10

    if keys[pygame.K_m]:
        angle += .1

    if keys[pygame.K_n]:
        angle -= .1

    count = 0
    for i in triangle:
        Tri[count] = (i[0] * math.cos(angle) - i[1] * math.sin(angle) + tri_x,
                      i[0] * math.sin(angle) + i[1] * math.cos(angle) + tri_y)
        count += 1
    setup(Tri, squares)

    intersection_points = []
    for i in tri_lines:
        segment_intersection(i, g_lines)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
