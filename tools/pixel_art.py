"""Small deterministic native pixel drawing helpers."""
SIZE = 64
INK = '#283b49'
WHITE = '#f1ede1'

class Pixels:
    def __init__(self):
        self.cells = {}

    def rect(self, x, y, w, h, colour):
        for py in range(y, y+h):
            for px in range(x, x+w):
                if 0 <= px < SIZE and 0 <= py < SIZE:
                    self.cells[px, py] = colour
        return self

    def ellipse(self, x, y, w, h, colour):
        for py in range(y, y+h):
            for px in range(x, x+w):
                if ((px+.5-x-w/2)/(w/2))**2+((py+.5-y-h/2)/(h/2))**2 <= 1:
                    self.rect(px, py, 1, 1, colour)
        return self

    def polygon(self, points, colour):
        for y in range(min(p[1] for p in points), max(p[1] for p in points)):
            for x in range(min(p[0] for p in points), max(p[0] for p in points)):
                inside = False
                for a, b in zip(points, points[1:]+points[:1]):
                    if (a[1] > y+.5) != (b[1] > y+.5):
                        cross = (b[0]-a[0])*(y+.5-a[1])/(b[1]-a[1])+a[0]
                        if x+.5 < cross:
                            inside = not inside
                if inside:
                    self.rect(x, y, 1, 1, colour)
        return self

    def line(self, a, b, colour):
        x, y = a
        ex, ey = b
        dx, dy = abs(ex-x), -abs(ey-y)
        sx, sy = (1 if x < ex else -1), (1 if y < ey else -1)
        err = dx+dy
        while True:
            self.rect(x, y, 1, 1, colour)
            if (x, y) == (ex, ey):
                break
            e = 2*err
            if e >= dy:
                err += dy
                x += sx
            if e <= dx:
                err += dx
                y += sy
        return self

    def marks(self, marks, colour):
        for x, y, w, h in marks:
            self.rect(x, y, w, h, colour)
        return self

    def shaded(self, dark, light):
        original = set(self.cells)
        for x, y in original:
            if (x+1, y) not in original or (x, y+1) not in original:
                self.cells[x, y] = dark
            elif (x-1, y) not in original or (x, y-1) not in original:
                self.cells[x, y] = light
        return self

    def outline(self):
        original = set(self.cells)
        for x, y in original:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (x+dx, y+dy) not in original:
                    self.rect(x+dx, y+dy, 1, 1, INK)
        return self

    def svg(self, class_name=''):
        colours = {}
        for y in range(SIZE):
            x = 0
            while x < SIZE:
                colour = self.cells.get((x, y))
                end = x+1
                while end < SIZE and self.cells.get((end, y)) == colour:
                    end += 1
                if colour:
                    colours.setdefault(colour, []).append(f'M{x} {y}h{end-x}v1H{x}Z')
                x = end
        paths = ''.join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in colours.items())
        return f'<g class="{class_name}">{paths}</g>' if class_name else paths

def shape(draw, base, dark, light):
    return draw(Pixels(), base).shaded(dark, light).outline()

