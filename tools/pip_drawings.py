"""Detailed pixel companions with centred faces and balanced paired features."""
from pixel_art import Pixels, shape, INK, WHITE


def mirror(p):
    """Reflect the left half about the middle of the 64-pixel drawing."""
    left = {(x, y): colour for (x, y), colour in p.cells.items() if x < 32}
    p.cells = left | {(63-x, y): colour for (x, y), colour in left.items()}
    return p


def balanced(draw, base, dark, light):
    return shape(lambda p, colour: mirror(draw(p, colour)), base, dark, light)


def group(parts, name):
    return f'<g class="{name}">{"".join(parts)}</g>'


def paired_feet(p, split=32):
    """Retain every foot pixel, with a separate pivot for each planted step."""
    parts = []
    for name, test in [('back', lambda x: x < split), ('front', lambda x: x >= split)]:
        foot = Pixels()
        foot.cells = {(x, y): colour for (x, y), colour in p.cells.items() if test(x)}
        if not foot.cells:
            continue
        xs, ys = zip(*foot.cells)
        origin = f'{(min(xs)+max(xs)+1)/2:g}px {min(ys)}px'
        parts.append(f'<g class="sprite-foot-{name}" data-pip-origin="{origin}">{foot.svg()}</g>')
    return group(parts, 'sprite-feet')


def eyes(x=24, y=25, colour=INK):
    p = Pixels().rect(x, y+1, 4, 2, colour).rect(x+1, y, 2, 4, colour)
    p.rect(x+1, y+1, 1, 1, WHITE)
    return mirror(p).svg('sprite-eyes')


def smile(y, colour='#765b54'):
    return mirror(Pixels().line((28, y), (29, y+1), colour).line((29, y+1), (31, y+1), colour)).svg('sprite-smile')


def muzzle(p, y=30, colour='#f0e4ce', nose='#66524b'):
    p.ellipse(24, y-1, 16, 8, colour).ellipse(30, y, 4, 2, nose)
    p.line((31, y+2), (31, y+3), nose)
    return mirror(p)


def fur_body(base, dark, light, belly, paws=None):
    body = balanced(lambda p, c: p.ellipse(19, 31, 26, 26, c), base, dark, light)
    body.ellipse(24, 35, 16, 19, belly).marks([(22, 38, 1, 2), (41, 38, 1, 2)], light)
    arms = balanced(lambda p, c: p.ellipse(18, 41, 8, 13, c), base, dark, light)
    arms.marks([(21, 50, 1, 2), (42, 50, 1, 2)], light)
    feet = balanced(lambda p, c: p.ellipse(18, 53, 12, 7, c), paws or base, dark, light)
    feet.marks([(22, 57, 1, 2), (25, 57, 1, 2), (38, 57, 1, 2), (41, 57, 1, 2)], dark)
    return body.svg() + arms.svg('sprite-arms') + paired_feet(feet)


def ears_pointed(base, dark, light, lining):
    p = balanced(lambda p, c: p.polygon([(18, 7), (24, 10), (28, 21), (18, 23), (16, 17)], c), base, dark, light)
    return mirror(p.polygon([(19, 11), (22, 13), (24, 20), (19, 20)], lining)).svg('sprite-ears')


def paired_wings(p):
    left, right = Pixels(), Pixels()
    left.cells = {(x, y): c for (x, y), c in p.cells.items() if x < 32}
    right.cells = {(63-x, y): c for (x, y), c in left.cells.items()}
    return group([left.svg('sprite-wing-left'), right.svg('sprite-wing-right')], 'sprite-wings')


def fox():
    tail = shape(lambda p, c: p.polygon([(38, 49), (44, 44), (48, 37), (53, 32), (58, 33), (60, 39), (57, 49), (48, 57), (37, 57)], c), '#c68954', '#895d43', '#e0aa72')
    tail.polygon([(53, 33), (57, 34), (59, 39), (56, 46), (51, 48), (49, 43)], '#f0dfc2').marks([(43, 50, 3, 1), (47, 47, 2, 1)], '#dba36b')
    head = balanced(lambda p, c: p.polygon([(18, 19), (23, 15), (32, 14), (43, 19), (46, 26), (42, 32), (36, 37), (28, 37), (21, 32), (17, 26)], c), '#ce945f', '#946448', '#e8b782')
    head = mirror(head.ellipse(19, 27, 13, 8, '#f3e6cf').rect(23, 19, 3, 1, '#edc393'))
    muzzle(head, 31)
    face = group([head.svg(), eyes(24, 24), smile(34, '#7d5c48')], 'sprite-head')
    return tail.svg('sprite-tail') + fur_body('#c68954', '#895d43', '#e0aa72', '#efddbc', '#a77b53') + ears_pointed('#ce945f', '#946448', '#e8b782', '#b48678') + face


def cat():
    tail = shape(lambda p, c: p.polygon([(39, 51), (47, 50), (52, 45), (52, 33), (50, 27), (54, 25), (57, 30), (58, 42), (54, 51), (47, 57), (39, 57)], c), '#91a6b6', '#637f94', '#c4d3d8')
    tail.marks([(52, 31, 5, 2), (53, 39, 5, 2), (49, 48, 6, 2), (43, 53, 5, 2)], '#607b91')
    head = balanced(lambda p, c: p.ellipse(17, 16, 30, 23, c), '#a4b8c5', '#6f889c', '#d6dfe0')
    head = mirror(head.rect(24, 18, 2, 4, '#70899b').rect(29, 17, 2, 4, '#70899b').rect(18, 27, 4, 1, '#70899b').rect(18, 30, 4, 1, '#70899b'))
    muzzle(head, 31, '#f0ede1', '#b38986')
    whiskers = mirror(Pixels().line((23, 32), (13, 30), '#d7d9cb').line((23, 34), (14, 36), '#b7c6c5'))
    face = group([head.svg(), eyes(24, 25), smile(35, '#746b65'), whiskers.svg()], 'sprite-head')
    return tail.svg('sprite-tail') + fur_body('#91a6b6', '#637f94', '#c4d3d8', '#ecebdf', '#d3dbd8') + ears_pointed('#a4b8c5', '#6f889c', '#d6dfe0', '#c7a3aa') + face


def frog():
    hind = balanced(lambda p, c: p.ellipse(9, 34, 17, 20, c), '#668e66', '#456b53', '#9bbd88')
    hind = mirror(hind.line((13, 50), (7, 53), '#abd3a1').line((14, 52), (12, 57), '#abd3a1'))
    body = balanced(lambda p, c: p.ellipse(18, 30, 28, 25, c), '#79a882', '#4d7a5d', '#b5d6aa')
    body.ellipse(24, 36, 16, 17, '#dce3bb')
    head = balanced(lambda p, c: p.ellipse(14, 23, 36, 18, c).ellipse(17, 14, 12, 18, c), '#88b48c', '#557f62', '#c0ddb4')
    head = mirror(head.ellipse(20, 18, 7, 9, '#bdcea5').ellipse(18, 31, 5, 3, '#9dc6a0').rect(29, 28, 1, 1, '#6b906b'))
    feet = balanced(lambda p, c: p.ellipse(20, 39, 7, 17, c).ellipse(17, 53, 12, 6, c), '#81b28b', '#4d7a5d', '#c0ddb4')
    return hind.svg() + body.svg() + feet.svg('sprite-feet sprite-arms') + group([head.svg(), eyes(21, 20), smile(34, '#4b745b')], 'sprite-head')


def axolotl():
    tail = shape(lambda p, c: p.polygon([(41, 43), (50, 37), (56, 34), (59, 37), (57, 46), (49, 53), (40, 55)], c), '#cb9eb1', '#a67591', '#e8c1d0')
    tail.line((47, 46), (55, 39), '#eac9d4')
    body = balanced(lambda p, c: p.ellipse(20, 35, 24, 21, c), '#ddb1c1', '#b4809c', '#efd0d9')
    body.ellipse(25, 40, 14, 13, '#f4dfe0')
    gills = Pixels()
    for x, y in [(16, 23), (14, 29), (15, 35)]:
        gills.line((x+3, y+2), (x-5, y), '#ac7694').ellipse(x-7, y-3, 8, 5, '#d39cb5').rect(x-5, y-2, 3, 1, '#f0c5d2')
    gills = mirror(gills)
    head = balanced(lambda p, c: p.ellipse(16, 20, 32, 22, c), '#e3b7c6', '#b985a0', '#f3d5de')
    head = mirror(head.ellipse(19, 32, 7, 4, '#e8aebb').rect(24, 23, 2, 1, '#f7e2e5'))
    feet = balanced(lambda p, c: p.ellipse(16, 49, 11, 8, c), '#ddb1c1', '#b4809c', '#efd0d9')
    arms = balanced(lambda p, c: p.ellipse(17, 40, 8, 9, c), '#ddb1c1', '#b4809c', '#efd0d9')
    return tail.svg('sprite-tail') + body.svg() + gills.svg('sprite-gills sprite-ears') + feet.svg('sprite-feet') + arms.svg('sprite-arms') + group([head.svg(), eyes(24, 28), smile(36, '#965f7d')], 'sprite-head')


def owl():
    body = balanced(lambda p, c: p.ellipse(18, 24, 28, 33, c), '#a78c69', '#75604c', '#d0b38a')
    body.ellipse(24, 31, 16, 24, '#ead8b8')
    for y in range(35, 53, 4):
        for x in (26, 30):
            body.rect(x, y, 2, 2, '#b39a73').rect(62-x, y, 2, 2, '#b39a73')
    wing = shape(lambda p, c: p.polygon([(20, 29), (13, 33), (13, 43), (18, 51), (24, 51), (23, 35)], c), '#917c61', '#695849', '#c4a77e')
    for y in (36, 40, 44):
        wing.line((16, y), (21, y+3), '#c5af89')
    head = balanced(lambda p, c: p.polygon([(18, 13), (24, 16), (32, 15), (44, 14), (47, 24), (43, 32), (35, 36), (23, 34), (17, 25)], c), '#b29773', '#80654d', '#d9bd92')
    head = mirror(head.ellipse(20, 18, 13, 16, '#f2e4cb').ellipse(23, 21, 8, 10, '#d9bf87').ellipse(22, 29, 5, 3, '#e3c59c'))
    head.polygon([(29, 29), (35, 29), (32, 34)], '#bb9458')
    feet = mirror(Pixels().rect(24, 55, 2, 4, '#bb985e').rect(21, 58, 8, 2, '#ccae77'))
    return body.svg() + paired_wings(wing) + feet.svg('sprite-feet') + group([head.svg(), eyes(25, 24)], 'sprite-head')


def bunny():
    ears = balanced(lambda p, c: p.ellipse(20, 3, 8, 27, c), '#c5b69d', '#918371', '#e7d8bf')
    ears = mirror(ears.ellipse(22, 7, 4, 19, '#d4acb1').rect(23, 10, 1, 11, '#e6c5c6'))
    head = balanced(lambda p, c: p.ellipse(18, 22, 28, 23, c), '#d0c2aa', '#9b8b79', '#f0e2ca')
    head = mirror(head.ellipse(19, 35, 10, 6, '#e0d3bc'))
    muzzle(head, 36, '#f2e8d5', '#bd9294')
    whiskers = mirror(Pixels().line((24, 37), (14, 35), '#b9baa9').line((24, 39), (14, 41), '#b9baa9'))
    return ears.svg('sprite-ears') + fur_body('#c5b69d', '#918371', '#e7d8bf', '#f0e6d3', '#d3c6ac') + group([head.svg(), eyes(24, 30), smile(40, '#8e7970'), whiskers.svg()], 'sprite-head')


def robot():
    feet = balanced(lambda p, c: p.rect(22, 45, 7, 12, c).rect(19, 55, 11, 5, c), '#789cb5', '#4d718a', '#b7d1df')
    feet = mirror(feet.rect(22, 48, 7, 2, '#436277').rect(20, 56, 8, 1, '#c4d7df'))
    arms = balanced(lambda p, c: p.polygon([(20, 32), (16, 33), (13, 44), (15, 50), (20, 50), (20, 43), (23, 36)], c), '#9ebac7', '#637f98', '#d3e3e6')
    arms = mirror(arms.ellipse(15, 43, 4, 4, '#d1b778'))
    body = balanced(lambda p, c: p.polygon([(23, 30), (41, 30), (44, 36), (42, 49), (22, 49), (20, 36)], c), '#91adbe', '#5c8097', '#cbdde3')
    body.rect(25, 35, 14, 9, '#45637a').rect(27, 37, 3, 3, '#d7bd80').rect(33, 37, 4, 1, '#c5e9e6').rect(33, 40, 3, 1, '#c5e9e6')
    head = balanced(lambda p, c: p.polygon([(22, 12), (42, 12), (46, 16), (46, 29), (42, 33), (22, 33), (18, 29), (18, 16)], c), '#9abcc9', '#65849c', '#d9e8e9')
    head.rect(22, 17, 20, 11, '#284d62').rect(23, 18, 18, 1, '#618f9f')
    antenna = mirror(Pixels().rect(31, 6, 1, 6, '#92aeb2').ellipse(29, 3, 6, 4, '#d5bd80'))
    bolts = mirror(Pixels().rect(21, 15, 1, 1, '#e4eadf').rect(21, 30, 1, 1, '#e4eadf'))
    return feet.svg('sprite-feet') + arms.svg('sprite-arms') + body.svg() + antenna.svg('sprite-ears') + group([head.svg(), eyes(25, 20, '#bee9e7'), smile(25, '#badfdc'), bolts.svg()], 'sprite-head')


def cloud():
    base = balanced(lambda p, c: p.ellipse(19, 19, 26, 28, c).ellipse(8, 29, 21, 21, c).rect(18, 35, 28, 17, c), '#c2dbe4', '#8dabbc', '#eef4f1')
    base = mirror(base.ellipse(13, 33, 15, 12, '#dce9eb').ellipse(23, 23, 9, 14, '#eef6f0').rect(17, 46, 2, 1, '#a7c9d6').rect(26, 48, 2, 1, '#a7c9d6').ellipse(18, 41, 6, 3, '#d1dee2'))
    rain = mirror(Pixels().line((19, 55), (18, 59), '#93b6bd').line((29, 56), (29, 61), '#bed4d4'))
    return group([base.svg(), eyes(24, 37), smile(45, '#7895a6')], 'sprite-head sprite-face') + rain.svg('sprite-rain')


def duck():
    body = balanced(lambda p, c: p.ellipse(18, 31, 28, 25, c), '#a8b8b4', '#6e8885', '#d7e0d9')
    body.ellipse(23, 36, 18, 17, '#8f7057').ellipse(27, 41, 10, 12, '#b49877')
    wing = shape(lambda p, c: p.ellipse(13, 34, 11, 19, c), '#9bafac', '#678581', '#d4e0d8')
    wing.line((17, 39), (19, 47), '#bfcdc4').rect(16, 45, 5, 2, '#607f91')
    neck = balanced(lambda p, c: p.ellipse(24, 27, 16, 16, c), '#51876e', '#356852', '#9fbc8c')
    neck.rect(24, 35, 16, 3, '#ebe6cc')
    head = balanced(lambda p, c: p.ellipse(20, 15, 24, 22, c), '#4f967a', '#35745e', '#9bceb0')
    head = mirror(head.rect(24, 18, 3, 1, '#b3d8bc').ellipse(22, 28, 5, 3, '#83b498'))
    bill = balanced(lambda p, c: p.ellipse(24, 29, 16, 7, c), '#e0b972', '#ad884e', '#f3d69b')
    bill.line((26, 33), (37, 33), '#b09360')
    feet = balanced(lambda p, c: p.polygon([(25, 52), (29, 52), (30, 57), (28, 60), (18, 59), (20, 56)], c), '#c6a261', '#977b4c', '#e7c68b')
    return body.svg() + paired_wings(wing) + neck.svg() + feet.svg('sprite-feet') + group([head.svg(), eyes(24, 24), bill.svg()], 'sprite-head')


def penguin():
    body = balanced(lambda p, c: p.ellipse(20, 17, 24, 40, c), '#506c86', '#354d69', '#93afc3')
    body.ellipse(24, 32, 16, 23, '#f0ede0')
    wing = shape(lambda p, c: p.polygon([(22, 29), (16, 32), (12, 43), (14, 49), (18, 48), (25, 34)], c), '#58758c', '#354d69', '#9db8c9')
    wing.line((16, 36), (14, 44), '#9bb5c2')
    head = balanced(lambda p, c: p.ellipse(20, 12, 24, 24, c), '#506c86', '#354d69', '#93afc3')
    head = mirror(head.ellipse(23, 20, 10, 13, '#f2efe4').rect(24, 16, 3, 1, '#a9c3d0'))
    head.polygon([(28, 29), (36, 29), (32, 34)], '#d8b06c')
    feet = balanced(lambda p, c: p.ellipse(18, 54, 13, 6, c), '#c9a363', '#947744', '#e5c68a')
    return body.svg() + paired_wings(wing) + feet.svg('sprite-feet') + group([head.svg(), eyes(25, 24)], 'sprite-head')


def turtle():
    shell = balanced(lambda p, c: p.ellipse(14, 28, 36, 28, c), '#7da277', '#527b58', '#bdd19a')
    shell = mirror(shell.ellipse(18, 31, 28, 21, '#92b384').line((24, 32), (22, 42), '#66885c').line((22, 42), (27, 50), '#66885c').line((22, 42), (16, 43), '#66885c').line((27, 50), (31, 48), '#66885c').rect(18, 49, 3, 1, '#c3d3a5'))
    shell.ellipse(26, 35, 12, 14, '#b3cd93')
    feet = balanced(lambda p, c: p.ellipse(12, 41, 11, 12, c).ellipse(17, 51, 12, 8, c), '#93b583', '#63845d', '#c8dda8')
    feet = mirror(feet.rect(15, 50, 1, 2, '#e0dfb5').rect(19, 56, 1, 2, '#e0dfb5').rect(23, 56, 1, 2, '#e0dfb5'))
    neck = balanced(lambda p, c: p.ellipse(25, 31, 14, 14, c), '#99b582', '#67885f', '#d0dfa8')
    head = balanced(lambda p, c: p.ellipse(20, 22, 24, 19, c), '#afca92', '#779e6c', '#e0e8bb')
    head = mirror(head.ellipse(22, 34, 5, 3, '#c0d5a4').rect(25, 25, 2, 1, '#e9edce'))
    return shell.svg() + feet.svg('sprite-feet') + neck.svg() + group([head.svg(), eyes(24, 29), smile(36, '#668660')], 'sprite-head')


def dragon():
    tail = shape(lambda p, c: p.polygon([(40, 47), (48, 43), (53, 34), (57, 29), (60, 31), (58, 44), (52, 54), (40, 58)], c), '#6b9fa0', '#487782', '#afd2bd')
    tail.marks([(52, 43, 2, 2), (47, 49, 2, 2)], '#d0c58e')
    wing = shape(lambda p, c: p.polygon([(24, 33), (14, 22), (8, 23), (6, 39), (14, 35), (20, 43), (27, 39)], c), '#649499', '#416e7b', '#abd0bd')
    wing.polygon([(11, 27), (11, 35), (15, 32), (22, 39)], '#d0cda8').line((23, 34), (10, 24), '#c6c69f')
    body = balanced(lambda p, c: p.ellipse(20, 31, 24, 26, c), '#83b1a8', '#547f83', '#c0dbc4')
    body.ellipse(25, 34, 14, 21, '#e6dcbc')
    for y in (39, 44, 49):
        body.line((27, y), (36, y), '#b8aa85')
    horns = balanced(lambda p, c: p.polygon([(23, 19), (21, 8), (25, 10), (28, 20)], c), '#c2b287', '#948366', '#e4d2ad')
    head = balanced(lambda p, c: p.ellipse(17, 16, 30, 23, c), '#8ab8ae', '#568a8b', '#c1dfcb')
    head.ellipse(22, 29, 20, 9, '#c7ddc2')
    head = mirror(head.rect(28, 31, 1, 1, '#6e8f78').rect(24, 20, 2, 1, '#d4e5cf'))
    feet = balanced(lambda p, c: p.ellipse(18, 53, 12, 7, c), '#87b4ac', '#547f83', '#c0dbc4')
    feet = mirror(feet.rect(21, 57, 1, 2, '#dfd3a6').rect(25, 57, 1, 2, '#dfd3a6'))
    return tail.svg('sprite-tail') + paired_wings(wing) + body.svg() + horns.svg('sprite-ears') + feet.svg('sprite-feet') + group([head.svg(), eyes(24, 24), smile(35, '#648473')], 'sprite-head')


def hamster():
    ears = balanced(lambda p, c: p.ellipse(17, 15, 10, 12, c), '#c7a174', '#987252', '#e8c59a')
    ears = mirror(ears.ellipse(20, 18, 5, 7, '#d5b0a7'))
    body = balanced(lambda p, c: p.ellipse(17, 31, 30, 27, c), '#c7a174', '#987252', '#e8c59a')
    body.ellipse(23, 37, 18, 18, '#f1e1c8')
    head = balanced(lambda p, c: p.ellipse(16, 21, 32, 25, c), '#d7b181', '#a8805b', '#efd1a6')
    head = mirror(head.ellipse(17, 32, 14, 11, '#f2e2c7').rect(24, 24, 2, 1, '#f4dab6'))
    muzzle(head, 35, '#f6ead5', '#be9586')
    paws = balanced(lambda p, c: p.ellipse(22, 43, 7, 10, c), '#dcc6a8', '#a28b6e', '#f1dec5')
    feet = balanced(lambda p, c: p.ellipse(18, 54, 12, 6, c), '#c6ad8b', '#957a5d', '#e3cfaf')
    whiskers = mirror(Pixels().line((23, 36), (12, 35), '#c6bda5').line((23, 39), (13, 42), '#c6bda5'))
    return body.svg() + ears.svg('sprite-ears') + paws.svg('sprite-arms') + feet.svg('sprite-feet') + group([head.svg(), eyes(24, 29), smile(39, '#907562'), whiskers.svg()], 'sprite-head sprite-cheeks')


def raccoon():
    tail = shape(lambda p, c: p.polygon([(39, 49), (46, 49), (52, 44), (53, 34), (52, 29), (56, 28), (59, 34), (59, 44), (54, 53), (47, 58), (38, 58)], c), '#9cb0bd', '#6a8297', '#cddbe0')
    tail.marks([(53, 34, 6, 3), (53, 43, 6, 3), (47, 51, 8, 3), (40, 55, 6, 3)], '#526b80')
    ears = balanced(lambda p, c: p.ellipse(17, 10, 10, 13, c), '#9baeb9', '#6d8594', '#d0dbe0')
    ears = mirror(ears.ellipse(20, 13, 5, 7, '#c4b5ad'))
    head = balanced(lambda p, c: p.ellipse(16, 17, 32, 23, c), '#b1c1cb', '#7e95a6', '#e0e8e8')
    head = mirror(head.ellipse(19, 23, 12, 9, '#72899b').rect(25, 20, 2, 1, '#d6e0df'))
    muzzle(head, 32, '#f2eee1', '#465c66')
    return tail.svg('sprite-tail') + fur_body('#9cb0bd', '#6a8297', '#cddbe0', '#eae9df', '#849eae') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 25), smile(36, '#6e7b78')], 'sprite-head')


def bee():
    wing = shape(lambda p, c: p.ellipse(9, 17, 18, 25, c), '#cce1e7', '#9abcc9', '#eff6f4')
    wing.line((14, 24), (21, 36), '#b6d1dc').rect(14, 22, 4, 1, '#f2f8f6')
    abdomen = balanced(lambda p, c: p.ellipse(22, 32, 20, 25, c), '#d5b362', '#a18749', '#f0d496')
    abdomen = mirror(abdomen.rect(22, 39, 20, 4, '#62665d').rect(25, 49, 14, 4, '#62665d'))
    legs = mirror(Pixels().line((24, 39), (18, 43), '#738183').line((23, 46), (19, 50), '#738183').line((27, 53), (25, 58), '#738183').rect(17, 43, 3, 2, '#9aaaa6').rect(18, 50, 3, 2, '#9aaaa6').rect(24, 58, 3, 2, '#9aaaa6'))
    head = balanced(lambda p, c: p.ellipse(19, 19, 26, 21, c), '#dfc27e', '#ad8f54', '#f5dfaa')
    head = mirror(head.ellipse(22, 31, 6, 3, '#e8c997').rect(24, 22, 2, 1, '#f7e7be'))
    antenna = mirror(Pixels().line((25, 21), (23, 13), '#83968f').ellipse(20, 10, 5, 4, '#b3c5b6'))
    return paired_wings(wing) + legs.svg('sprite-feet') + abdomen.svg('sprite-tail') + antenna.svg('sprite-ears') + group([head.svg(), eyes(24, 27), smile(34, '#9a794a')], 'sprite-head')


def octopus():
    arms = []
    patterns = [
        [(24, 39), (19, 44), (13, 44), (9, 41), (7, 43), (10, 49), (17, 50), (26, 45)],
        [(25, 43), (22, 49), (15, 53), (12, 51), (10, 53), (14, 57), (21, 55), (29, 46)],
        [(28, 44), (25, 52), (21, 56), (20, 59), (25, 59), (31, 49)],
        [(31, 44), (28, 53), (28, 59), (31, 60), (32, 58), (33, 47)],
    ]
    for i, points in enumerate(patterns):
        arm = shape(lambda p, c: p.polygon(points, c), '#d7a5ac' if i % 2 else '#ca97a4', '#a57791', '#efc9cc')
        for x, y in points[2:4]:
            arm.rect(x, y, 2, 1, '#f5ded9')
        left, right = Pixels(), Pixels()
        left.cells = {(x, y): c for (x, y), c in arm.cells.items() if x < 32}
        right.cells = {(63-x, y): c for (x, y), c in left.cells.items()}
        arms.extend([left.svg(), right.svg()])
    head = balanced(lambda p, c: p.ellipse(17, 15, 30, 30, c), '#d6a4af', '#ad7b98', '#efcbd1')
    head = mirror(head.ellipse(21, 18, 11, 13, '#e5bbc3').ellipse(20, 35, 7, 4, '#e3afbd').rect(25, 21, 2, 1, '#f6dcdd'))
    return group(arms, 'sprite-tentacles sprite-feet') + group([head.svg(), eyes(24, 32), smile(40, '#9b6b87')], 'sprite-head')




def dog():
    tail = shape(lambda p, c: p.polygon([(39, 51), (47, 50), (52, 44), (53, 36), (57, 34), (59, 39), (57, 48), (50, 56), (39, 58)], c), '#b89168', '#80634f', '#e0c29a')
    ears = balanced(lambda p, c: p.polygon([(18, 15), (23, 13), (26, 19), (24, 34), (20, 38), (15, 35), (13, 26), (15, 18)], c), '#a57855', '#725440', '#c69b72')
    ears = mirror(ears.line((17, 21), (18, 32), '#b58963'))
    head = balanced(lambda p, c: p.ellipse(18, 15, 28, 25, c), '#d0ab7d', '#98744f', '#edcfaa')
    head = mirror(head.rect(25, 18, 2, 1, '#f2dabc').ellipse(19, 30, 7, 5, '#dec29f'))
    muzzle(head, 32, '#f4e6cb', '#68564a')
    return tail.svg('sprite-tail') + fur_body('#b89168', '#80634f', '#e0c29a', '#ede1c7', '#cdb18e') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 25), smile(36, '#80644d')], 'sprite-head')


def badger():
    ears = balanced(lambda p, c: p.ellipse(18, 10, 9, 12, c), '#74828b', '#4f626e', '#a6b2b8')
    ears = mirror(ears.ellipse(20, 13, 5, 6, '#c4b7b1'))
    head = balanced(lambda p, c: p.ellipse(16, 17, 32, 25, c), '#e0dfcf', '#a2a799', '#f3efe1')
    head = mirror(head.polygon([(20, 18), (27, 19), (29, 28), (25, 35), (20, 32), (18, 25)], '#536b79').rect(23, 20, 2, 2, '#8a9ca4'))
    muzzle(head, 34, '#ece6d5', '#405661')
    tail = mirror(Pixels().ellipse(26, 49, 12, 11, '#708690').rect(28, 56, 8, 2, '#a8b8bd'))
    return tail.svg('sprite-tail') + fur_body('#74828b', '#4f626e', '#a6b2b8', '#cbd1c7', '#546b77') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 26), smile(38, '#6f7a76')], 'sprite-head')


def rat():
    tail = shape(lambda p, c: p.polygon([(40, 51), (48, 53), (55, 50), (57, 44), (55, 39), (57, 38), (60, 44), (59, 51), (54, 57), (44, 59), (38, 56)], c), '#c8a4a5', '#977f89', '#e1c7bf')
    ears = balanced(lambda p, c: p.ellipse(13, 9, 16, 18, c), '#a1a8b1', '#707f91', '#c9cbd0')
    ears = mirror(ears.ellipse(17, 13, 9, 10, '#d7b5b9').ellipse(19, 15, 5, 6, '#e7cbc8'))
    head = balanced(lambda p, c: p.polygon([(20, 20), (26, 17), (32, 17), (44, 22), (46, 29), (39, 37), (32, 40), (24, 36), (18, 29)], c), '#acb5be', '#7e8e9b', '#d6dadb')
    head = mirror(head.rect(25, 21, 2, 1, '#e3e5df'))
    muzzle(head, 34, '#e8e5d9', '#b9919a')
    whiskers = mirror(Pixels().line((25, 35), (12, 32), '#b9c5c5').line((25, 37), (13, 40), '#cdd3cd'))
    return tail.svg('sprite-tail') + fur_body('#a1a8b1', '#707f91', '#c9cbd0', '#e5e3d5', '#c3a6a6') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 27), smile(38, '#8b747c'), whiskers.svg()], 'sprite-head')


def squirrel():
    tail = shape(lambda p, c: p.polygon([(39, 53), (43, 44), (45, 26), (49, 15), (55, 11), (60, 16), (61, 27), (58, 40), (53, 50), (46, 58), (38, 58)], c), '#aa7956', '#765840', '#d7ac7e')
    tail.polygon([(50, 20), (55, 15), (58, 20), (58, 28), (54, 38), (50, 45), (48, 43), (52, 31)], '#c99c70').marks([(50, 24, 2, 4), (51, 35, 2, 3)], '#e5be8c')
    ears = balanced(lambda p, c: p.polygon([(19, 22), (17, 14), (20, 7), (25, 12), (27, 22)], c), '#bd9065', '#896448', '#e1b887')
    ears = mirror(ears.polygon([(20, 13), (23, 15), (24, 20), (20, 20)], '#c3a097'))
    head = balanced(lambda p, c: p.ellipse(17, 18, 30, 23, c), '#c79b70', '#926e4e', '#eaca9c')
    head = mirror(head.ellipse(18, 30, 10, 7, '#ead6b5').rect(24, 21, 2, 1, '#f0d6ad'))
    muzzle(head, 33, '#f1e2c7', '#755c4c')
    return tail.svg('sprite-tail') + fur_body('#bd9065', '#896448', '#e1b887', '#eaddbc', '#a47d58') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 26), smile(37, '#8c6a51')], 'sprite-head')


def bat():
    wing = shape(lambda p, c: p.polygon([(23, 31), (16, 26), (7, 22), (5, 31), (4, 43), (9, 39), (14, 45), (19, 43), (23, 49), (26, 40)], c), '#8d819e', '#625e80', '#b9afc4')
    wing.line((16, 29), (10, 38), '#b1a3c0').line((18, 32), (17, 41), '#b1a3c0')
    ears = balanced(lambda p, c: p.polygon([(18, 22), (17, 10), (22, 6), (27, 20)], c), '#8e8aab', '#636b89', '#c3bad3')
    ears = mirror(ears.polygon([(20, 13), (22, 11), (25, 20), (21, 20)], '#b39aac'))
    head = balanced(lambda p, c: p.ellipse(18, 18, 28, 24, c), '#a29bb6', '#757b99', '#cec6d7')
    head = mirror(head.ellipse(20, 31, 7, 4, '#baacba').rect(24, 21, 2, 1, '#e1d8e4'))
    muzzle(head, 34, '#d8d2da', '#897b91')
    return fur_body('#8e8aab', '#636b89', '#c3bad3', '#d9d6d9', '#83839f') + paired_wings(wing) + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 27), smile(38, '#847289')], 'sprite-head')


def goblin():
    ears = balanced(lambda p, c: p.polygon([(22, 21), (7, 17), (11, 25), (18, 31), (24, 30)], c), '#8fb191', '#607f72', '#c2d4ab')
    ears = mirror(ears.polygon([(19, 23), (12, 21), (17, 27), (22, 28)], '#b6b4a0'))
    coat = balanced(lambda p, c: p.ellipse(18, 35, 28, 22, c), '#9b8973', '#736b5b', '#c3b59c')
    coat = mirror(coat.polygon([(23, 36), (31, 43), (30, 52), (24, 48)], '#d1c7a6').rect(31, 43, 1, 10, '#665f55').rect(29, 45, 2, 1, '#e0c99a'))
    arms = balanced(lambda p, c: p.ellipse(17, 42, 9, 11, c), '#8fb191', '#607f72', '#c2d4ab')
    feet = balanced(lambda p, c: p.ellipse(18, 54, 12, 6, c), '#7a7971', '#555f60', '#a9ada0')
    head = balanced(lambda p, c: p.ellipse(17, 16, 30, 27, c), '#a3c197', '#729877', '#d3deb5')
    head = mirror(head.ellipse(19, 31, 7, 5, '#b8c6a0').rect(23, 22, 5, 1, '#789373').rect(26, 19, 2, 1, '#e3e6c3'))
    head.ellipse(29, 32, 6, 4, '#85ab83')
    return coat.svg() + arms.svg('sprite-arms') + feet.svg('sprite-feet') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 26), smile(38, '#638b72')], 'sprite-head')


def rock():
    stone = balanced(lambda p, c: p.polygon([(12, 47), (15, 29), (24, 18), (32, 16), (42, 20), (50, 35), (52, 50), (46, 57), (18, 57)], c), '#91a4b0', '#647e8e', '#c3d1d5')
    stone = mirror(stone.polygon([(16, 30), (25, 20), (31, 19), (27, 29), (19, 35)], '#b8c6c9').polygon([(15, 43), (21, 48), (25, 55), (17, 53)], '#748e9b').line((24, 22), (27, 24), '#dbe1dc').ellipse(18, 39, 6, 3, '#a9b9bc'))
    facets = mirror(Pixels().line((17, 35), (20, 30), '#aabbbf').rect(21, 49, 2, 1, '#b6c7c8'))
    return group([stone.svg(), facets.svg('sprite-facets'), eyes(24, 33), smile(44, '#597889')], 'sprite-head')


def hedgehog():
    spines = balanced(lambda p, c: p.polygon([(31, 12), (27, 8), (24, 14), (18, 10), (17, 18), (11, 16), (13, 24), (7, 27), (12, 33), (7, 39), (13, 44), (11, 50), (18, 52), (20, 58), (32, 59)], c), '#9a8876', '#6d645a', '#c1ad92')
    spines = mirror(spines.line((20, 18), (22, 25), '#cfbca1').line((14, 29), (18, 34), '#bca88e').line((14, 41), (20, 43), '#cfbca1'))
    ears = balanced(lambda p, c: p.ellipse(18, 18, 9, 11, c), '#c0aa8c', '#927d67', '#e2cfad')
    ears = mirror(ears.ellipse(21, 21, 4, 6, '#d4b4a3'))
    head = balanced(lambda p, c: p.ellipse(18, 23, 28, 22, c), '#cfb797', '#a68d6e', '#ecd9b7')
    muzzle(head, 36, '#f1e4c9', '#7d6454')
    return spines.svg('sprite-spines') + fur_body('#c0aa8c', '#927d67', '#e2cfad', '#eadbbc', '#b8a083') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 29), smile(40, '#9a7c63')], 'sprite-head')


def otter():
    tail = shape(lambda p, c: p.polygon([(38, 51), (45, 51), (53, 47), (58, 44), (58, 49), (53, 54), (45, 59), (36, 58)], c), '#947761', '#65564b', '#bfa78c')
    ears = balanced(lambda p, c: p.ellipse(17, 16, 9, 10, c), '#a88b6d', '#79644f', '#d0b594')
    ears = mirror(ears.ellipse(20, 19, 4, 5, '#c6ac9a'))
    head = balanced(lambda p, c: p.ellipse(16, 20, 32, 23, c), '#b69a79', '#887052', '#dac4a2')
    head = mirror(head.ellipse(17, 31, 13, 9, '#e2ceb0').rect(24, 23, 2, 1, '#ead6b7'))
    muzzle(head, 35, '#f0e0c3', '#786253')
    whiskers = mirror(Pixels().line((23, 35), (13, 34), '#b0b4a4').line((23, 38), (14, 40), '#c6cab5'))
    return tail.svg('sprite-tail') + fur_body('#947761', '#65564b', '#bfa78c', '#dfcfb1', '#89735e') + ears.svg('sprite-ears') + group([head.svg(), eyes(24, 28), smile(39, '#8b715a'), whiskers.svg()], 'sprite-head')


def moth():
    wing = shape(lambda p, c: p.ellipse(4, 17, 25, 29, c).ellipse(11, 38, 19, 20, c), '#b2a6b9', '#807a99', '#d8cdd4')
    wing.ellipse(8, 23, 16, 16, '#c8bba9').ellipse(12, 26, 8, 8, '#8795a6').ellipse(14, 28, 4, 4, '#e9d9b6')
    wing.line((15, 41), (24, 49), '#d3c4c0').line((8, 39), (19, 43), '#91869e')
    body = balanced(lambda p, c: p.ellipse(24, 29, 16, 27, c), '#b7a591', '#827c6a', '#ddd0b5')
    body = mirror(body.rect(25, 39, 14, 2, '#968b7a').rect(27, 46, 10, 2, '#968b7a'))
    antenna = mirror(Pixels().line((26, 20), (21, 9), '#a6afa3').line((23, 13), (18, 12), '#c6cbb7').line((24, 16), (20, 17), '#c6cbb7'))
    head = balanced(lambda p, c: p.ellipse(21, 17, 22, 21, c), '#d0c2a9', '#9e9682', '#f0e4cd')
    head = mirror(head.ellipse(22, 29, 5, 3, '#ddc5b3'))
    feet = mirror(Pixels().line((26, 52), (23, 58), '#aaa897').rect(21, 57, 4, 2, '#c1bdab'))
    return paired_wings(wing) + body.svg() + feet.svg('sprite-feet') + antenna.svg('sprite-ears') + group([head.svg(), eyes(24, 25), smile(33, '#998a79')], 'sprite-head')


def snail():
    shell = balanced(lambda p, c: p.ellipse(15, 14, 34, 35, c), '#b79872', '#89724f', '#dcc19a')
    shell = mirror(shell.ellipse(20, 18, 24, 24, '#c7ac83').ellipse(25, 22, 14, 15, '#a38965').ellipse(29, 26, 6, 6, '#dec89f').rect(24, 21, 2, 1, '#ead7b4'))
    foot = balanced(lambda p, c: p.ellipse(12, 44, 40, 15, c), '#9aafa0', '#6b8c82', '#c6d5b8')
    foot = mirror(foot.line((17, 54), (29, 56), '#d6dfc3'))
    stalks = mirror(Pixels().line((25, 36), (23, 24), '#8faca0').ellipse(20, 21, 6, 6, '#bad0b0').rect(22, 22, 2, 1, '#e0e8c9'))
    head = balanced(lambda p, c: p.ellipse(19, 32, 26, 21, c), '#b0c6aa', '#819e8c', '#dce3c0')
    head = mirror(head.ellipse(21, 44, 6, 3, '#c3d0ac'))
    return shell.svg('sprite-shell') + foot.svg('sprite-feet') + stalks.svg('sprite-ears') + group([head.svg(), eyes(24, 38), smile(47, '#6f9084')], 'sprite-head')


def mushroom():
    stem = balanced(lambda p, c: p.ellipse(22, 27, 20, 31, c), '#d4c8af', '#a29887', '#f0e8d3')
    stem = mirror(stem.line((24, 42), (25, 51), '#e8dcc2').ellipse(23, 41, 5, 3, '#ddc1ab'))
    arms = balanced(lambda p, c: p.ellipse(18, 41, 8, 12, c), '#cabda4', '#a29887', '#eadfc7')
    feet = balanced(lambda p, c: p.ellipse(21, 54, 9, 6, c), '#c5b59c', '#958974', '#e3d4b7')
    cap = balanced(lambda p, c: p.ellipse(11, 10, 42, 25, c).rect(12, 26, 40, 6, c), '#b78278', '#865b63', '#d9ada0')
    cap = mirror(cap.ellipse(18, 17, 8, 6, '#eee3ca').ellipse(27, 12, 10, 5, '#f2e8d3').ellipse(14, 27, 5, 4, '#e5d4bb').rect(23, 12, 2, 1, '#ecc8b3'))
    brim = mirror(Pixels().rect(14, 32, 36, 3, '#cbb39c').line((17, 33), (20, 33), '#efdfc1'))
    return arms.svg('sprite-arms') + feet.svg('sprite-feet') + group([stem.svg(), eyes(24, 36), smile(46, '#928270')], 'sprite-head') + group([cap.svg(), brim.svg()], 'sprite-cap')



MAKERS = (fox, cat, frog, axolotl, owl, bunny, robot, cloud, duck, penguin, turtle, dragon, hamster, raccoon, bee, octopus, dog, badger, rat, squirrel, bat, goblin, rock, hedgehog, otter, moth, snail, mushroom)

# Centred accessory positions in the same 64-pixel art space.
ANCHORS = {'fox': {'cx': 32, 'top': 14, 'eye': 26, 'width': 28, 'neck': 38},
 'cat': {'cx': 32, 'top': 16, 'eye': 27, 'width': 28, 'neck': 40},
 'frog': {'cx': 32, 'top': 17, 'eye': 22, 'width': 33, 'neck': 41},
 'axolotl': {'cx': 32, 'top': 20, 'eye': 30, 'width': 30, 'neck': 42},
 'owl': {'cx': 32, 'top': 15, 'eye': 26, 'width': 29, 'neck': 37},
 'bunny': {'cx': 32, 'top': 22, 'eye': 32, 'width': 26, 'neck': 44},
 'robot': {'cx': 32, 'top': 12, 'eye': 22, 'width': 27, 'neck': 34},
 'cloud': {'cx': 32, 'top': 19, 'eye': 39, 'width': 37, 'neck': 51},
 'duck': {'cx': 32, 'top': 15, 'eye': 26, 'width': 22, 'neck': 37},
 'penguin': {'cx': 32, 'top': 13, 'eye': 26, 'width': 22, 'neck': 36},
 'turtle': {'cx': 32, 'top': 22, 'eye': 31, 'width': 22, 'neck': 41},
 'dragon': {'cx': 32, 'top': 16, 'eye': 26, 'width': 28, 'neck': 40},
 'hamster': {'cx': 32, 'top': 21, 'eye': 31, 'width': 30, 'neck': 46},
 'raccoon': {'cx': 32, 'top': 17, 'eye': 27, 'width': 30, 'neck': 41},
 'bee': {'cx': 32, 'top': 19, 'eye': 29, 'width': 24, 'neck': 40},
 'octopus': {'cx': 32, 'top': 15, 'eye': 34, 'width': 28, 'neck': 44},
 'dog': {'cx': 32, 'top': 15, 'eye': 27, 'width': 26, 'neck': 41},
 'badger': {'cx': 32, 'top': 17, 'eye': 28, 'width': 30, 'neck': 43},
 'rat': {'cx': 32, 'top': 17, 'eye': 29, 'width': 28, 'neck': 41},
 'squirrel': {'cx': 32, 'top': 18, 'eye': 28, 'width': 28, 'neck': 42},
 'bat': {'cx': 32, 'top': 18, 'eye': 29, 'width': 26, 'neck': 43},
 'goblin': {'cx': 32, 'top': 16, 'eye': 28, 'width': 28, 'neck': 43},
 'rock': {'cx': 32, 'top': 16, 'eye': 35, 'width': 30, 'neck': 48},
 'hedgehog': {'cx': 32, 'top': 23, 'eye': 31, 'width': 26, 'neck': 45},
 'otter': {'cx': 32, 'top': 20, 'eye': 30, 'width': 30, 'neck': 44},
 'moth': {'cx': 32, 'top': 17, 'eye': 27, 'width': 21, 'neck': 39},
 'snail': {'cx': 32, 'top': 32, 'eye': 40, 'width': 24, 'neck': 53},
 'mushroom': {'cx': 32, 'top': 10, 'eye': 38, 'width': 26, 'neck': 51}}
