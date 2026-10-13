"""Right-facing walking silhouettes. The renderer mirrors these for the left view.

Use the same palette and layered parts as the front portraits. Head, feet, wings
and tail remain separate so each Pip keeps its own signature motion.
"""
from pathlib import Path
import json
from pixel_art import Pixels, INK, WHITE, shape
from pip_drawings import paired_feet


def layer(p, name='', origin=None):
    art = p.svg()
    if 'sprite-head' in name and origin is None and p.cells:
        xs, ys = zip(*p.cells)
        origin = f'{(min(xs)+max(xs)+1)/2:g}px {max(ys)+1}px'
    pivot = f' data-pip-origin="{origin}"' if origin else ''
    return f'<g class="{name}"{pivot}>{art}</g>'


def shaded(draw, palette):
    return shape(draw, *palette)


def eye(x, y, size=4):
    p = Pixels().ellipse(x, y, size, size, INK)
    p.rect(x+1, y+1, 1, 1, WHITE)
    return layer(p, 'sprite-eyes')


FUR = {
    'fox': ('#c68954', '#895d43', '#e0aa72', '#efddbc'),
    'cat': ('#91a6b6', '#637f94', '#c4d3d8', '#ecebdf'),
    'bunny': ('#c5b69d', '#918371', '#e7d8bf', '#f0e6d3'),
    'hamster': ('#c7a174', '#987252', '#e8c59a', '#eee0c2'),
    'raccoon': ('#9cb0bd', '#6a8297', '#cddbe0', '#eae9df'),
    'dog': ('#b89168', '#80634f', '#e0c29a', '#ede1c7'),
    'badger': ('#74828b', '#4f626e', '#a6b2b8', '#e0dfcf'),
    'rat': ('#a1a8b1', '#707f91', '#c9cbd0', '#e5e3d5'),
    'squirrel': ('#bd9065', '#896448', '#e1b887', '#eaddbc'),
    'hedgehog': ('#c0aa8c', '#927d67', '#e2cfad', '#eadbbc'),
    'otter': ('#947761', '#65564b', '#bfa78c', '#dfcfb1'),
    'dragon': ('#6b9fa0', '#487782', '#afd2bd', '#d4d6b1'),
    'goblin': ('#8fb191', '#607f72', '#c2d4ab', '#b8c6a0'),
}


def fur_profile(species):
    base, dark, light, belly = FUR[species]
    palette = base, dark, light
    parts = []
    if species == 'squirrel':
        tail = shaded(lambda p, c: p.ellipse(3, 12, 22, 40, c).ellipse(12, 42, 19, 15, c), ('#aa7956', '#765840', '#d7ac7e'))
        tail.ellipse(7, 17, 13, 27, '#c99c70').line((13, 21), (11, 38), '#e5be8c')
    elif species == 'bunny':
        tail = shaded(lambda p, c: p.ellipse(9, 40, 12, 13, c), palette)
    elif species == 'rat':
        tail = shaded(lambda p, c: p.polygon([(21, 50), (12, 52), (5, 48), (3, 39), (5, 32), (8, 31), (7, 38), (8, 45), (14, 47), (23, 47)], c), ('#c8a4a5', '#977f89', '#e1c7bf'))
    elif species in ('hamster', 'badger', 'goblin'):
        tail = shaded(lambda p, c: p.ellipse(13, 43, 11, 11, c), palette)
    elif species == 'otter':
        tail = shaded(lambda p, c: p.polygon([(23, 47), (15, 49), (5, 53), (4, 56), (13, 57), (28, 53)], c), palette)
    elif species == 'hedgehog':
        tail = shaded(lambda p, c: p.polygon([(28, 15), (23, 10), (20, 17), (14, 14), (14, 22), (7, 22), (11, 29), (5, 35), (11, 40), (6, 46), (13, 49), (12, 55), (26, 56), (36, 34)], c), ('#9a8876', '#6d645a', '#c1ad92'))
        tail.line((18, 22), (20, 29), '#cfbca1').line((12, 35), (19, 39), '#cfbca1')
    elif species == 'cat':
        tail = shaded(lambda p, c: p.polygon([(22, 48), (14, 46), (11, 39), (11, 23), (7, 19), (4, 22), (5, 41), (10, 50), (20, 55)], c), palette)
        tail.marks([(5, 26, 6, 2), (5, 35, 7, 2), (11, 46, 7, 2)], dark)
    else:
        tail = shaded(lambda p, c: p.polygon([(25, 46), (17, 44), (12, 34), (7, 29), (3, 32), (4, 42), (11, 51), (24, 55)], c), palette)
        if species == 'fox':
            tail.polygon([(7, 29), (3, 32), (4, 41), (9, 45), (13, 40)], '#f0dfc2')
        if species == 'raccoon':
            tail.marks([(4, 35, 7, 3), (8, 43, 8, 3), (16, 49, 6, 3)], '#526b80')
    if species != 'goblin':
        parts.append(layer(tail, 'sprite-spines' if species == 'hedgehog' else 'sprite-tail', '22px 49px'))
    body = shaded(lambda p, c: p.ellipse(17, 33, 30, 23, c), palette)
    body.ellipse(30, 39, 15, 16, belly)
    if species == 'goblin':
        body = shaded(lambda p, c: p.ellipse(24, 34, 21, 23, c), ('#9b8973', '#736b5b', '#c3b59c'))
        body.rect(28, 43, 15, 3, '#706452').rect(36, 43, 3, 3, '#d7ba80')
    parts.append(layer(body))
    if species == 'dragon':
        wing = shaded(lambda p, c: p.polygon([(29, 37), (20, 21), (12, 21), (10, 35), (16, 32), (23, 43), (32, 44)], c), ('#649499', '#416e7b', '#abd0bd'))
        wing.line((18, 26), (26, 38), '#c3d8ad')
        parts.append(layer(wing, 'sprite-wings sprite-wing-left', '29px 39px'))
    feet = shaded(lambda p, c: p.ellipse(19, 48, 10, 12, c).ellipse(38, 47, 10, 13, c), palette)
    feet.rect(23, 56, 9, 4, light).rect(41, 56, 11, 4, light)
    parts.append(paired_feet(feet, 35))
    arm = shaded(lambda p, c: p.ellipse(33, 39, 8, 14, c), palette)
    parts.append(layer(arm, 'sprite-arms', '37px 40px'))
    top = 23 if species == 'bunny' else 18
    head_palette = (belly, '#a2a799', '#f3efe1') if species == 'badger' else palette
    head = shaded(lambda p, c: p.ellipse(30, top, 23, 24, c).ellipse(42, top+12, 16, 10, c), head_palette)
    head.ellipse(44, top+13, 13, 8, belly)
    if species == 'raccoon':
        head.polygon([(35, 24), (49, 24), (53, 30), (42, 32), (35, 29)], '#526b80')
    if species == 'badger':
        head.polygon([(36, 19), (42, 20), (48, 25), (54, 32), (49, 36), (44, 29), (37, 26)], '#4f626e')
    if species == 'cat':
        head.marks([(33, 20, 2, 6), (37, 19, 2, 5)], dark)
    if species == 'dragon':
        head.rect(54, 29, 2, 1, '#557c70').line((44, 18), (48, 20), light)
    if species == 'goblin':
        head.ellipse(49, 29, 10, 6, '#85ab83').rect(43, 23, 6, 1, '#638b72')
    head.ellipse(55, top+14, 4, 3, '#8b747c' if species == 'rat' else '#514b45')
    mouth = Pixels().line((49, top+21), (54, top+20), dark)
    if species in ('fox', 'cat', 'squirrel', 'dragon'):
        ear = shaded(lambda p, c: p.polygon([(31, 22), (31, 9), (36, 12), (42, 23)], c), palette)
        ear.polygon([(33, 14), (35, 15), (38, 21), (33, 21)], '#bfa29c')
    elif species == 'bunny':
        ear = shaded(lambda p, c: p.ellipse(31, 3, 9, 26, c), palette)
        ear.ellipse(34, 7, 4, 17, '#d4acb1')
    elif species == 'dog':
        ear = shaded(lambda p, c: p.ellipse(27, 16, 12, 23, c), ('#a57855', '#725440', '#c69b72'))
        ear.line((31, 23), (32, 33), '#b58963')
    elif species == 'goblin':
        ear = shaded(lambda p, c: p.polygon([(35, 24), (20, 17), (24, 27), (34, 33)], c), palette)
        ear.polygon([(24, 21), (31, 25), (31, 29)], '#b6b4a0')
    else:
        ear = shaded(lambda p, c: p.ellipse(28, 11 if species == 'rat' else top-5, 15 if species == 'rat' else 10, 16 if species == 'rat' else 11, c), palette)
        ear.ellipse(31, 14 if species == 'rat' else top-2, 9 if species == 'rat' else 5, 10 if species == 'rat' else 6, '#c7a3aa')
    parts.append(layer(head, 'sprite-head'))
    parts.append(layer(ear, 'sprite-ears', '35px 23px'))
    parts.append(eye(44, top+8))
    parts.append(layer(mouth, 'sprite-smile'))
    if species in ('cat', 'rat', 'otter', 'hamster'):
        parts.append(layer(Pixels().line((52, top+19), (62, top+16), '#cdd3cd').line((52, top+20), (62, top+23), '#b9c5c5')))
    return ''.join(parts), dict(cx=43, top=top, eye=top+10, width=23, neck=top+24)


def bird_profile(species):
    palette = {'owl': ('#a78c69', '#75604c', '#d0b38a'), 'duck': ('#a8b8b4', '#6e8885', '#d7e0d9'), 'penguin': ('#506c86', '#354d69', '#93afc3')}[species]
    body = shaded(lambda p, c: p.ellipse(18, 26, 31, 32, c), palette)
    body.ellipse(36, 32, 11, 23, '#ead8b8' if species == 'owl' else '#f0ede0')
    feet = shaded(lambda p, c: p.polygon([(28, 53), (32, 53), (32, 57), (38, 58), (37, 61), (24, 60), (23, 58), (28, 57)], c).polygon([(39, 54), (43, 54), (43, 58), (50, 59), (48, 61), (38, 60)], c), ('#c59b68', '#8d714f', '#ead2a4'))
    head = shaded(lambda p, c: p.ellipse(29, 13, 23, 25, c), ('#7f9c86', '#527761', '#b5cbb0') if species == 'duck' else palette)
    if species == 'owl':
        head.ellipse(37, 19, 13, 15, '#e9dab9').line((32, 17), (35, 12), '#d0b38a')
    elif species == 'penguin':
        head.ellipse(38, 19, 12, 17, '#f1ede0')
    beak = shaded(lambda p, c: p.polygon([(49, 26), (58, 29), (57, 32), (49, 33)], c), ('#caaa6d', '#917644', '#efd397'))
    wing = shaded(lambda p, c: p.ellipse(21, 32, 19, 20, c), palette)
    wing.line((26, 39), (34, 46), palette[1]).line((25, 43), (30, 49), palette[2])
    return layer(body)+paired_feet(feet, 38)+layer(wing, 'sprite-wings sprite-wing-left', '32px 34px')+layer(head, 'sprite-head')+layer(beak)+eye(44, 23), dict(cx=42, top=13, eye=25, width=22, neck=36)


def small_profile(species):
    parts = []
    if species in ('frog', 'axolotl', 'turtle'):
        palette = ('#88b48c', '#4d7a5d', '#c0ddb4') if species == 'frog' else ('#ddb1c1', '#b4809c', '#efd0d9') if species == 'axolotl' else ('#a9c489', '#718e66', '#d2dfab')
        body = shaded(lambda p, c: p.ellipse(18, 33, 30, 23, c), palette)
        hind = shaded(lambda p, c: p.ellipse(15, 41, 18, 15, c).ellipse(23, 52, 17, 8, c).ellipse(40, 44, 9, 15, c), palette)
        if species == 'turtle':
            shell = shaded(lambda p, c: p.ellipse(11, 26, 34, 28, c), ('#7da277', '#527b58', '#bdd19a'))
            shell.ellipse(16, 30, 23, 18, '#92b384').line((22, 29), (20, 39), '#66885c').line((20, 39), (26, 48), '#66885c').line((20, 39), (13, 42), '#66885c').line((20, 39), (32, 38), '#66885c').line((32, 38), (35, 29), '#66885c')
            parts.append(layer(shell, 'sprite-shell', '27px 42px'))
        elif species == 'axolotl':
            tail = shaded(lambda p, c: p.polygon([(28, 48), (17, 43), (8, 36), (3, 37), (4, 44), (15, 53), (26, 55)], c), palette)
            parts.append(layer(tail, 'sprite-tail', '26px 49px'))
        else:
            parts.append(layer(body))
        head = shaded(lambda p, c: p.ellipse(33, 25, 25, 20, c), palette)
        if species == 'frog':
            head.ellipse(41, 20, 11, 11, palette[0]).line((46, 40), (56, 37), '#54755a')
        if species == 'axolotl':
            gills = shaded(lambda p, c: p.polygon([(36, 29), (29, 22), (25, 23), (28, 29), (24, 31), (25, 35), (33, 35), (29, 42), (33, 43), (38, 37)], c), ('#cb9eb1', '#a67591', '#e8c1d0'))
            parts.append(layer(gills, 'sprite-gills sprite-ears', '36px 34px'))
        parts += [paired_feet(hind, 39), layer(head, 'sprite-head'), eye(49, 27 if species != 'frog' else 24), layer(Pixels().line((50, 39), (55, 38), palette[1]), 'sprite-smile')]
        anchor = dict(cx=47, top=25, eye=29, width=23, neck=44)
    elif species == 'snail':
        shell = shaded(lambda p, c: p.ellipse(9, 17, 31, 35, c), ('#b79872', '#89724f', '#dcc19a'))
        shell.ellipse(14, 22, 22, 24, '#c7ac83').ellipse(19, 26, 13, 16, '#a38965').ellipse(23, 30, 6, 8, '#dec89f').rect(17, 25, 2, 1, '#ead7b4')
        foot = shaded(lambda p, c: p.ellipse(8, 47, 50, 13, c), ('#9aafa0', '#6b8c82', '#c6d5b8'))
        head = shaded(lambda p, c: p.ellipse(37, 33, 19, 22, c), ('#b0c6aa', '#819e8c', '#dce3c0'))
        stalk = shaded(lambda p, c: p.rect(48, 26, 3, 12, c).ellipse(46, 23, 7, 7, c), ('#b0c6aa', '#819e8c', '#dce3c0'))
        parts = [layer(shell, 'sprite-shell', '25px 42px'), layer(foot, 'sprite-feet'), layer(head, 'sprite-head'), layer(stalk, 'sprite-ears', '49px 36px'), eye(49, 25, 3), layer(Pixels().line((49, 46), (53, 44), '#6f9084'), 'sprite-smile')]
        anchor = dict(cx=47, top=33, eye=27, width=19, neck=51)
    elif species == 'robot':
        body = shaded(lambda p, c: p.rect(25, 32, 20, 22, c), ('#8aaebf', '#58798f', '#c0d8df'))
        body.rect(39, 38, 4, 10, '#476574').rect(39, 39, 3, 3, '#a7d5b6')
        head = shaded(lambda p, c: p.rect(28, 13, 21, 19, c).rect(47, 20, 7, 10, c), ('#a1becb', '#6c889e', '#d9e7e5'))
        head.rect(43, 18, 9, 9, '#355a68')
        display = Pixels().rect(46, 21, 5, 3, '#bee9e7')
        feet = shaded(lambda p, c: p.rect(25, 52, 7, 8, c).rect(40, 52, 7, 8, c).rect(28, 57, 9, 4, c).rect(43, 57, 9, 4, c), ('#789cb5', '#4d718a', '#b7d1df'))
        arm = shaded(lambda p, c: p.rect(30, 36, 6, 16, c).rect(29, 48, 8, 6, c), ('#9ebac7', '#637f98', '#d3e3e6'))
        antenna = Pixels().rect(36, 7, 2, 6, '#92aeb2').ellipse(34, 3, 6, 5, '#d5bd80')
        parts = [paired_feet(feet, 39), layer(body), layer(arm, 'sprite-arms', '33px 38px'), layer(antenna, 'sprite-ears', '37px 12px'), layer(head, 'sprite-head'), layer(display, 'sprite-eyes', '48px 22px')]
        anchor = dict(cx=43, top=13, eye=23, width=21, neck=34)
    elif species == 'cloud':
        puff = shaded(lambda p, c: p.ellipse(6, 29, 25, 24, c).ellipse(20, 18, 27, 33, c).ellipse(36, 29, 23, 24, c).rect(17, 36, 30, 19, c), ('#c2dbe4', '#8dabbc', '#eef4f1'))
        puff.ellipse(25, 24, 15, 22, '#dce9eb').ellipse(9, 34, 15, 11, '#dce9eb')
        rain = Pixels().line((19, 57), (17, 61), '#93b6bd').line((29, 57), (27, 62), '#bed4d4')
        parts = [layer(puff, 'sprite-head'), layer(rain, 'sprite-rain', '26px 57px'), eye(46, 36), layer(Pixels().line((49, 46), (53, 44), '#8dabbc'), 'sprite-smile')]
        anchor = dict(cx=43, top=19, eye=38, width=29, neck=53)
    elif species == 'rock':
        stone = shaded(lambda p, c: p.polygon([(16, 52), (17, 31), (27, 18), (36, 17), (46, 24), (52, 42), (49, 56), (23, 58)], c), ('#91a4b0', '#647e8e', '#c3d1d5'))
        stone.polygon([(18, 31), (28, 20), (35, 20), (28, 36), (21, 45)], '#b8c6c9').polygon([(18, 45), (28, 51), (24, 56), (18, 53)], '#748e9b')
        facets = Pixels().line((26, 23), (28, 25), '#dbe1dc').rect(22, 48, 2, 1, '#b6c7c8')
        parts = [layer(stone, 'sprite-head'), layer(facets, 'sprite-facets', '29px 37px'), eye(43, 34), layer(Pixels().line((45, 45), (49, 43), '#647e8e'), 'sprite-smile')]
        anchor = dict(cx=40, top=17, eye=36, width=26, neck=52)
    elif species == 'mushroom':
        stem = shaded(lambda p, c: p.ellipse(28, 29, 20, 29, c), ('#ded3b6', '#b4a88c', '#f1e8ce'))
        cap = shaded(lambda p, c: p.ellipse(11, 10, 45, 27, c), ('#b27f7b', '#805e67', '#d7aaa0'))
        cap.ellipse(20, 16, 10, 7, '#eddbc0').ellipse(39, 16, 7, 6, '#eddbc0').ellipse(32, 26, 8, 5, '#e0c4ab').line((18, 34), (49, 34), '#a38b7c')
        feet = shaded(lambda p, c: p.ellipse(25, 53, 11, 7, c).ellipse(39, 53, 12, 7, c), ('#b4a88c', '#8e8774', '#ded3b6'))
        parts = [paired_feet(feet, 37), layer(stem, 'sprite-head'), eye(42, 39), layer(Pixels().line((43, 48), (47, 47), '#a38b7c'), 'sprite-smile'), layer(cap, 'sprite-cap', '35px 32px')]
        anchor = dict(cx=38, top=10, eye=41, width=27, neck=54)
    elif species == 'octopus':
        palette = '#ae9bbd', '#796e99', '#d5c3dc'
        for i, points in enumerate([[(29, 39), (20, 44), (11, 44), (8, 48), (17, 52), (33, 47)], [(34, 41), (28, 53), (35, 59), (41, 57), (37, 52), (42, 43)], [(42, 39), (45, 48), (52, 53), (58, 49), (56, 45), (51, 47), (48, 38)]]):
            arm = shaded(lambda p, c, pts=points: p.polygon(pts, c), palette)
            parts.append(layer(arm, f'sprite-arm-{i} sprite-arms', '36px 43px'))
        head = shaded(lambda p, c: p.ellipse(26, 16, 29, 30, c), palette)
        head.ellipse(42, 36, 8, 4, '#c2a8c4')
        parts = ['<g class="sprite-tentacles" data-pip-origin="36px 43px">'+''.join(parts)+'</g>', layer(head, 'sprite-head'), eye(46, 29), layer(Pixels().line((47, 40), (52, 38), '#796e99'), 'sprite-smile')]
        anchor = dict(cx=42, top=16, eye=31, width=26, neck=43)
    else:
        raise ValueError(species)
    return ''.join(parts), anchor


def flying_profile(species):
    palette = {'bee': ('#d5b362', '#a18749', '#f0d496'), 'bat': ('#8e8aab', '#636b89', '#c3bad3'), 'moth': ('#c4b69e', '#908776', '#e6d6b9')}[species]
    wing_palette = {'bee': ('#cce1e7', '#9abcc9', '#eff6f4'), 'bat': ('#8d819e', '#625e80', '#b9afc4'), 'moth': ('#b2a6b9', '#807a99', '#d8cdd4')}[species]
    if species == 'bat':
        wing = shaded(lambda p, c: p.polygon([(36, 36), (22, 17), (10, 14), (6, 24), (4, 40), (12, 34), (18, 45), (25, 40), (33, 49)], c), wing_palette)
        wing.line((16, 21), (13, 32), '#b1a3c0').line((23, 29), (22, 40), '#b1a3c0')
    else:
        wing = shaded(lambda p, c: p.ellipse(12, 13, 23, 30, c).ellipse(16, 34, 18, 18, c), wing_palette)
        wing.line((18, 22), (29, 39), wing_palette[1])
        if species == 'moth':
            wing.ellipse(16, 19, 14, 15, '#c8bba9').ellipse(19, 23, 8, 8, '#8795a6').ellipse(21, 25, 4, 4, '#e9d9b6')
    body = shaded(lambda p, c: p.ellipse(23, 31, 24, 25, c), palette)
    if species == 'bee':
        body.marks([(24, 36, 18, 3), (27, 43, 16, 4)], '#746854')
    else:
        body.ellipse(35, 38, 10, 15, '#d9d6d9' if species == 'bat' else '#e6d6b9')
    head = shaded(lambda p, c: p.ellipse(33, 20, 23, 22, c).ellipse(48, 31, 10, 8, c), palette)
    head.ellipse(49, 33, 7, 5, '#d8d2da' if species == 'bat' else palette[2])
    if species == 'bat':
        antenna = shaded(lambda p, c: p.polygon([(35, 23), (33, 6), (38, 8), (43, 23)], c), palette)
        antenna.polygon([(35, 12), (37, 13), (40, 22), (36, 22)], '#b79cae')
    else:
        antenna = Pixels().line((41, 22), (44, 13), '#83968f').ellipse(42, 10, 5, 4, '#b3c5b6')
    feet = Pixels().line((31, 54), (28, 59), palette[1]).rect(27, 58, 6, 2, palette[2]).line((41, 53), (45, 58), palette[1]).rect(43, 58, 6, 2, palette[2])
    return layer(body, 'sprite-tail' if species == 'bee' else '')+layer(wing, 'sprite-wings sprite-wing-left', '33px 38px')+layer(feet, 'sprite-feet')+layer(antenna, 'sprite-ears', '40px 23px')+layer(head, 'sprite-head')+eye(46, 27)+layer(Pixels().line((51, 38), (56, 36), palette[1]), 'sprite-smile'), dict(cx=44, top=20, eye=29, width=23, neck=41)


def build():
    from pip_drawings import MAKERS
    art, anchors = {}, {}
    for maker in MAKERS:
        name = maker.__name__
        drawing = fur_profile(name) if name in FUR else bird_profile(name) if name in ('owl', 'duck', 'penguin') else flying_profile(name) if name in ('bee', 'bat', 'moth') else small_profile(name)
        art[name], anchors[name] = drawing
    source = '// Generated by tools/pip_profiles.py; walking profiles face right.\n'
    source += 'const ART='+json.dumps(art, separators=(',', ':'))+';\n'
    source += 'export const PIP_PROFILE_ANCHORS='+json.dumps(anchors, separators=(',', ':'))+';\n'
    source += 'export function pipProfileArtwork(id){return ART[id]||ART.fox;}\n'
    target = Path(__file__).resolve().parents[1]/'public'/'pip-profile-art.js'
    target.write_text(source, encoding='utf-8', newline='\n')
    print(f'Built {len(art)} walking profiles ({len(source):,} bytes).')


if __name__ == '__main__':
    build()
