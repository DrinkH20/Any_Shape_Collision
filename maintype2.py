import pygame
import math
import player

window = pygame.display.set_mode((500, 500))

lines = []
g_lines = []
tri_lines = []
intersection_points = []
intersecting_lines = []

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
tri_x = 400
tri_y = 10
center_x = 0
center_y = 0

scrollX = 1
scrollY = 1

squares = [(-100, 400), (500, 300), (500, 400), (-100, 400), (-1000, 400), (1000, 400), (1000, 500), (-1000, 500)]

triangle = [(37.5, -75), (-37.5, -75), (-75, -37.5), (-75, 37.5),
            (-37.5, 75), (37.5, 75), (75, 37.5), (75, -37.5)]

play_tri = [(37.5, -75), (-37.5, -75), (-75, -37.5), (-75, 37.5),
            (-37.5, 75), (37.5, 75), (75, 37.5), (75, -37.5)]

running = True

count = 0

angle_v = 0
angle = 0

detect = 0

rep = 0

part1 = 0
part2 = 0
part3 = 0
part4 = 0
part5 = 0
part6 = 0


def collide_x():
    global tri_x, speed_x, tri_y
    if detect_collision():
        tri_y -= 1
        if detect_collision():
            tri_y -= 1
            if detect_collision():
                tri_y -= 1
                if detect_collision():
                    tri_y -= 1
                    if detect_collision():
                        tri_y += 4
                        tri_x, speed_x = player.collide_x(speed_x, tri_x)
                        physics()


def collide_y():
    global tri_y, speed_y
    if detect_collision():
        tri_y, speed_y = player.collide_y(speed_y, tri_y)
        tri_y += 1
        if detect_collision():
            if keys[pygame.K_UP]:
                speed_y = -5
        tri_y -= 1
        physics()


def collide_rot():
    global angle, angle_v, tri_y
    if detect_collision():
        angle, angle_v = player.collide_rotate(angle_v, angle)


def setup(tri=(), squ=()):
    global tri_lines
    global g_lines, rep, average_y, average_x, center_y, center_x, part1, part2
    tri_lines = []
    g_lines = []

    if tri != 0:
        average_x = 0
        average_y = 0
        rep = 0
        for e in tri:
            average_x += e[0]
            average_y += e[1]
            rep += 1

        for r in range(len(tri) - 1):
            part1 = tri[r]
            part2 = tri[r + 1]
            tri_lines.append(((part1[0] + center_x, part1[1] + center_y),
                              (part2[0] + center_x, part2[1] + center_y)))

        part1 = tri[len(tri) - 1]
        part2 = tri[0]
        tri_lines.append(((part1[0] + center_x, part1[1] + center_y),
                          (part2[0] + center_x, part2[1] + center_y)))

    r = 0
    if squ != 0:
        while r < len(squ) / 4:
            r += 1
            g_lines.append((squ[r * 4 - 4], squ[r * 4 - 3]))
            g_lines.append((squ[r * 4 - 3], squ[r * 4 - 2]))
            g_lines.append((squ[r * 4 - 2], squ[r * 4 - 1]))
            g_lines.append((squ[r * 4 - 1], squ[r * 4 - 4]))

    return


def detect_collision():
    global count, intersection_points, g_lines, triangle, tri_x, tri_y, tri_lines, play_tri, intersecting_lines
    count = 0
    for v in triangle:
        play_tri[count] = (v[0] * math.cos(angle) - v[1] * math.sin(angle) + tri_x,
                           v[0] * math.sin(angle) + v[1] * math.cos(angle) + tri_y)
        count += 1
    setup(play_tri, squares)

    intersection_points = []
    intersecting_lines = []
    for v in tri_lines:
        segment_intersection(v, g_lines)

    # for e in intersection_points:
    #     pygame.draw.circle(window, (200, 10, 10), (e[0], -e[1]), 5)

    return intersection_points


def rotate():
    global angle, angle_v
    if keys[pygame.K_m]:
        angle_v = player.move_rot(.005, angle_v)

    if keys[pygame.K_n]:
        angle_v = player.move_rot(-.005, angle_v)

    angle, angle_v = player.slow_rot(.9, angle_v, angle)


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
    global scrollY, scrollX, part1, part2

    for e in tri_lines:
        part1, part2 = e[0], e[1]
        pygame.draw.line(window, (100, 100, 100), (part1[0] + scrollX, part1[1] + scrollY)
                         , (part2[0] + scrollX, part2[1] + scrollY))

    for e in g_lines:
        part1, part2 = e[0], e[1]
        pygame.draw.line(window, (100, 100, 100), (part1[0] + scrollX, part1[1] + scrollY)
                         , (part2[0] + scrollX, part2[1] + scrollY))

    # for e in intersection_points:
    #     pygame.draw.circle(window, (200, 10, 10), (e[0], -e[1]), 5)

    # pygame.draw.line(window, (200, 10, 10), (tri_x, tri_y), (tri_x, tri_y + 5), 5)
    # pygame.draw.line(window, (200, 10, 10), (tri_x + scrollX, tri_y + scrollY),
    #                  (tri_x + scrollX, tri_y + scrollY + 100), 1)


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
    global detect
    global intersecting_lines

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
                    if not intersecting_lines.__contains__(g_lines.index(j)):
                        intersecting_lines.append(g_lines.index(j))

    return intersection_points


def physics():
    global intersection_points, angle_v, average_x, rep, average_y, speed_x, part6
    average_x = 0
    average_y = 0
    rep = 0

    if intersection_points:
        for e in intersection_points:
            average_x += e[0]
            if e[1]:
                average_y += 100 / e[1]
            rep += 1

        if rep:
            average_x = average_x / rep
            average_y = average_y / rep

        angle_v += (tri_x - average_x) / 1000
        part6 = (tri_x - average_x) / -10
        # if keys[pygame.K_i]:
        #     speed_x += (round(tri_x) - round(average_x)) / 10


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

    scrollX += (tri_x + (scrollX - 250)) * -.1
    scrollY += (tri_y + (scrollY - 250)) * -.1

    part5 = 0
    rep = 0
    for i in intersecting_lines:
        part1 = g_lines[i]
        part2 = part1[0]
        part3 = part1[1]
        if (part2[0] - part3[0]) != 0:
            part4 = (part2[1] - part3[1])/(part2[0] - part3[0])
            part5 += part4
            rep += 1

    if rep != 0:
        part5 = part5/rep
        speed_x += part5*part6

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
