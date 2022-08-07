def slow_x(amount, spdx, plyrx):
    spdx = spdx * amount
    plyrx += spdx
    return plyrx, spdx


def slow_y(amount, spdy, plyry):
    spdy += amount
    plyry += spdy
    return plyry, spdy


def move_x(amount, spdx):
    spdx += amount
    return spdx


def collide_y(spdy, plyry):
    spdy *= -1
    plyry += spdy
    spdy = 0
    return plyry, spdy


def collide_x(spdx, plyrx):
    spdx *= -1
    plyrx += spdx
    spdx = 0
    return plyrx, spdx


def slow_rot(amount, spd_rot, plyr_rot):
    spd_rot = spd_rot * amount
    plyr_rot += spd_rot
    return plyr_rot, spd_rot


def move_rot(amount, spd_rot):
    spd_rot += amount
    return spd_rot


def collide_rotate(spd_rot, plyr_rot):
    spd_rot *= -1
    plyr_rot += spd_rot
    spd_rot = 0
    return plyr_rot, spd_rot
