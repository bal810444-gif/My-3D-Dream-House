from vpython import *
import random

random.seed(7)

# =====================================================
# REALISTIC 3D TWO-STORY DREAM HOUSE
# Controls: right-mouse drag = rotate | scroll = zoom
#           arrow keys = rotate | N = toggle day / night
# =====================================================

scene.title = "MY REALISTIC 3D TWO-STORY DREAM HOUSE"
scene.width = 1000
scene.height = 700
scene.userspin = True
scene.userzoom = True
scene.userpan = True
scene.center = vector(0, 3.5, 0)
scene.range = 11
scene.forward = vector(-0.15, -0.15, -1)
scene.caption = ("Right-drag (or Ctrl+left-drag) / arrow keys = rotate  |  "
                 "scroll = zoom  |  Shift+drag = pan  |  press <b>N</b> for day / night\n")

# ---------- COLORS ----------
DAY_SKY = vector(0.45, 0.72, 0.95)
NIGHT_SKY = vector(0.02, 0.03, 0.10)
wall_color = vector(0.96, 0.86, 0.70)
roof_color = vector(0.80, 0.17, 0.12)
roof_dark = vector(0.55, 0.09, 0.07)
wood_color = vector(0.50, 0.30, 0.16)
trim_color = vector(0.97, 0.97, 0.95)
glass_color = vector(0.60, 0.80, 0.95)
grass_color = vector(0.22, 0.52, 0.20)
stone_color = vector(0.62, 0.60, 0.56)
shutter_color = vector(0.12, 0.30, 0.38)

# ---------- LIGHTING ----------
scene.background = DAY_SKY
scene.lights = []
scene.ambient = color.gray(0.40)

sun_pos = vector(-10, 11, 4)
sun_dir = norm(vector(0, 3, 0) - sun_pos)
sun_light = distant_light(direction=sun_dir, color=color.gray(0.75))
fill_light = distant_light(direction=vector(0.3, -0.3, -1), color=color.gray(0.25))
moon_light = distant_light(direction=vector(0.4, -0.7, -0.6), color=color.black)

# =====================================================
# GROUND, LAWN, DISTANT HILLS
# =====================================================
box(pos=vector(0, -0.22, 0), size=vector(90, 0.4, 90), color=vector(0.18, 0.42, 0.17))

box(pos=vector(0, -0.2, 0), size=vector(24, 0.4, 22),
    color=grass_color, texture=textures.rough)

for hx, hz, hw, hh, shade in [(-22, -26, 34, 7, 0.0), (6, -30, 44, 10, 0.05), (28, -24, 30, 6, 0.02)]:
    ellipsoid(pos=vector(hx, 0, hz), size=vector(hw, hh * 2, 14),
              color=vector(0.20 + shade, 0.40 + shade, 0.30 + shade))

# Fake soft shadows (hidden at night)
shadows = []
shadows.append(box(pos=vector(4.2, 0.014, -1.6), size=vector(6.5, 0.01, 5.4),
                   color=color.black, opacity=0.22))

# Grass tufts for a natural lawn
tufts = []
for _ in range(220):
    gx, gz = random.uniform(-11.5, 11.5), random.uniform(-10.5, 10.5)
    if abs(gx) < 3.4 and -2.7 < gz < 4.6:     # keep house footprint clear
        continue
    if abs(gx) < 0.9 and gz > 4.4:            # keep path clear
        continue
    g = random.uniform(0.0, 0.12)
    tufts.append(cone(pos=vector(gx, 0, gz),
                      axis=vector(random.uniform(-0.05, 0.05), random.uniform(0.18, 0.4), 0),
                      radius=0.05, color=vector(0.15 + g, 0.45 + g, 0.12)))
compound(tufts)

# =====================================================
# HOUSE BODY
# =====================================================
# Stone foundation
box(pos=vector(0, 0.2, 0), size=vector(6.2, 0.4, 5.2),
    color=vector(0.75, 0.73, 0.70), texture=textures.stones)

# First & second floor (stucco texture)
box(pos=vector(0, 1.7, 0), size=vector(6, 2.6, 5), color=wall_color, texture=textures.stucco)
box(pos=vector(0, 4.5, 0), size=vector(6, 3, 5), color=wall_color, texture=textures.stucco)

# Floor divider band
box(pos=vector(0, 3.05, 0), size=vector(6.25, 0.2, 5.25), color=trim_color)

# Corner trim boards
for cx in (-3.0, 3.0):
    for cz in (-2.5, 2.5):
        box(pos=vector(cx, 3.2, cz), size=vector(0.14, 5.6, 0.14), color=trim_color)

# =====================================================
# GABLE ROOF WITH SHINGLES
# =====================================================
eave_y, ridge_y = 5.95, 7.45
half_w, roof_depth = 3.55, 6.2


def roof_panel(a, b):
    axis_v = b - a
    length = mag(axis_v)
    u = norm(axis_v)
    n = cross(vector(0, 0, 1), u)           # outward normal
    if n.y < 0:
        n = -n
    box(pos=(a + b) / 2, axis=axis_v, size=vector(length, roof_depth, 0.18),
        up=vector(0, 0, 1), color=roof_color, texture=textures.rough)
    # shingle courses
    for k in range(1, 14):
        p = a + axis_v * (k / 14.0) + n * 0.10
        shade = roof_dark if k % 2 else roof_color
        box(pos=p, axis=axis_v, size=vector(0.05, roof_depth, 0.04),
            up=vector(0, 0, 1), color=shade)
    # fascia board at eave
    box(pos=a + n * -0.02, axis=axis_v, size=vector(0.08, roof_depth, 0.30),
        up=vector(0, 0, 1), color=trim_color)


roof_panel(vector(-half_w, eave_y, 0), vector(0, ridge_y, 0))
roof_panel(vector(half_w, eave_y, 0), vector(0, ridge_y, 0))

# Ridge cap
cylinder(pos=vector(0, ridge_y + 0.04, -roof_depth / 2), axis=vector(0, 0, roof_depth),
         radius=0.13, color=roof_dark)

# Gable end triangles (front and back) - closes the roof
for gz in (2.5, -2.5):
    triangle(vs=[vertex(pos=vector(-3.0, 6.0, gz), color=wall_color),
                 vertex(pos=vector(3.0, 6.0, gz), color=wall_color),
                 vertex(pos=vector(0, 7.36, gz), color=wall_color)])
# Attic vent in front gable
box(pos=vector(0, 6.55, 2.54), size=vector(0.7, 0.45, 0.06), color=trim_color)
for i in range(4):
    box(pos=vector(0, 6.40 + i * 0.1, 2.58), size=vector(0.6, 0.03, 0.03), color=color.gray(0.3))

# Chimney
box(pos=vector(2.1, 7.0, -0.8), size=vector(0.8, 2.4, 0.8),
    color=vector(0.65, 0.28, 0.20), texture=textures.stones)
box(pos=vector(2.1, 8.25, -0.8), size=vector(1.0, 0.15, 1.0), color=color.gray(0.55))
CHIMNEY_TOP = vector(2.1, 8.45, -0.8)

# =====================================================
# WINDOWS (shutters, sills, glass, interiors)
# =====================================================
window_interiors = []


def make_window(lx, y, w, h, d=2.5, angle=0, shutters=False):
    parts = []
    t = 0.09
    P = parts.append
    # frame
    P(box(pos=vector(lx, y + h / 2 - t / 2, d + 0.06), size=vector(w, t, 0.12), color=trim_color))
    P(box(pos=vector(lx, y - h / 2 + t / 2, d + 0.06), size=vector(w, t, 0.12), color=trim_color))
    P(box(pos=vector(lx - w / 2 + t / 2, y, d + 0.06), size=vector(t, h, 0.12), color=trim_color))
    P(box(pos=vector(lx + w / 2 - t / 2, y, d + 0.06), size=vector(t, h, 0.12), color=trim_color))
    # interior (dark by day, warm light at night)
    inner = box(pos=vector(lx, y, d + 0.02), size=vector(w - 2 * t, h - 2 * t, 0.02),
                color=vector(0.18, 0.16, 0.15))
    P(inner)
    window_interiors.append(inner)
    # curtains
    P(box(pos=vector(lx - w * 0.30, y, d + 0.04), size=vector(w * 0.22, h - 2 * t, 0.02),
          color=vector(0.85, 0.80, 0.70)))
    P(box(pos=vector(lx + w * 0.30, y, d + 0.04), size=vector(w * 0.22, h - 2 * t, 0.02),
          color=vector(0.85, 0.80, 0.70)))
    # glass
    P(box(pos=vector(lx, y, d + 0.08), size=vector(w - 2 * t, h - 2 * t, 0.015),
          color=glass_color, opacity=0.35, shininess=1))
    # mullions
    P(box(pos=vector(lx, y, d + 0.10), size=vector(0.05, h - 2 * t, 0.04), color=trim_color))
    P(box(pos=vector(lx, y, d + 0.10), size=vector(w - 2 * t, 0.05, 0.04), color=trim_color))
    # sill
    P(box(pos=vector(lx, y - h / 2 - 0.05, d + 0.15), size=vector(w + 0.3, 0.08, 0.3), color=trim_color))
    # lintel
    P(box(pos=vector(lx, y + h / 2 + 0.06, d + 0.08), size=vector(w + 0.3, 0.12, 0.16), color=trim_color))
    if shutters:
        for sx in (-1, 1):
            cx = lx + sx * (w / 2 + 0.24)
            P(box(pos=vector(cx, y, d + 0.04), size=vector(0.40, h + 0.1, 0.06),
                  color=shutter_color, texture=textures.wood))
            for k in range(6):
                P(box(pos=vector(cx, y - h / 2 + 0.1 + k * (h / 5.5), d + 0.08),
                      size=vector(0.34, 0.025, 0.03), color=vector(0.07, 0.2, 0.26)))
    if angle != 0:
        for p in parts:
            p.rotate(angle=angle, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
    return parts


# Front
for x in (-1.8, 1.8):
    make_window(x, 1.8, 1.15, 1.15, shutters=True)
    make_window(x, 4.5, 1.25, 1.35, shutters=True)
# Back
for x in (-1.8, 1.8):
    make_window(x, 1.8, 1.15, 1.15, angle=pi)
    make_window(x, 4.5, 1.25, 1.35, angle=pi)
# Sides
for x in (-1.0, 1.0):
    make_window(x, 1.8, 1.0, 1.15, d=3.0, angle=pi / 2)
    make_window(x, 4.5, 1.0, 1.35, d=3.0, angle=pi / 2)
    make_window(x, 1.8, 1.0, 1.15, d=3.0, angle=-pi / 2)
    make_window(x, 4.5, 1.0, 1.35, d=3.0, angle=-pi / 2)

# =====================================================
# FRONT DOOR + PORCH
# =====================================================
# Porch slab and steps
box(pos=vector(0, 0.1, 3.2), size=vector(2.6, 0.2, 1.4), color=stone_color, texture=textures.stones)
box(pos=vector(0, 0.05, 4.1), size=vector(2.4, 0.1, 0.5), color=stone_color, texture=textures.stones)

# Door frame, leaf, panels
box(pos=vector(0, 1.35, 2.55), size=vector(1.4, 2.35, 0.1), color=trim_color)
box(pos=vector(0, 1.3, 2.6), size=vector(1.15, 2.2, 0.1), color=wood_color, texture=textures.wood)
for px in (-0.27, 0.27):
    for py, ph in ((0.85, 0.75), (1.85, 0.75)):
        box(pos=vector(px, py + 0.1, 2.66), size=vector(0.4, ph, 0.03), color=vector(0.38, 0.21, 0.10))
# Door glass strip + transom
box(pos=vector(0, 2.7, 2.58), size=vector(1.15, 0.35, 0.06), color=glass_color, opacity=0.45, shininess=1)
# Handle and knocker
sphere(pos=vector(0.42, 1.25, 2.70), radius=0.06, color=color.yellow, shininess=1)
cylinder(pos=vector(0, 1.95, 2.67), axis=vector(0, 0, 0.04), radius=0.07, color=vector(0.85, 0.65, 0.1))
# Doormat
box(pos=vector(0, 0.215, 3.35), size=vector(1.0, 0.03, 0.55),
    color=vector(0.35, 0.18, 0.12), texture=textures.rug)

# Porch lanterns
lamp_lights, lamp_bulbs = [], []
for lx in (-0.95, 0.95):
    cylinder(pos=vector(lx, 1.9, 2.55), axis=vector(0, 0, 0.12), radius=0.025, color=color.black)
    bulb = sphere(pos=vector(lx, 1.9, 2.7), radius=0.10, color=vector(0.9, 0.9, 0.8), opacity=0.8)
    lamp_bulbs.append(bulb)
    lamp_lights.append(local_light(pos=vector(lx, 1.9, 2.9), color=color.black))

# =====================================================
# SECOND-FLOOR BALCONY
# =====================================================
box(pos=vector(0, 3.2, 3.25), size=vector(3.7, 0.18, 1.4), color=wood_color, texture=textures.wood)
# Balcony door (glass)
box(pos=vector(0, 4.4, 2.55), size=vector(1.3, 2.3, 0.1), color=trim_color)
balcony_in = box(pos=vector(0, 4.4, 2.52), size=vector(1.1, 2.1, 0.02), color=vector(0.18, 0.16, 0.15))
window_interiors.append(balcony_in)
box(pos=vector(0, 4.4, 2.60), size=vector(1.1, 2.1, 0.02), color=glass_color, opacity=0.35, shininess=1)
box(pos=vector(0, 4.4, 2.63), size=vector(0.05, 2.1, 0.04), color=trim_color)
for yy in (3.7, 4.4, 5.1):
    box(pos=vector(0, yy, 2.63), size=vector(1.1, 0.05, 0.04), color=trim_color)

# Support columns
for cx in (-1.7, 1.7):
    cylinder(pos=vector(cx, 0.2, 3.85), axis=vector(0, 2.95, 0), radius=0.09, color=trim_color)
    box(pos=vector(cx, 0.25, 3.85), size=vector(0.28, 0.1, 0.28), color=trim_color)
    box(pos=vector(cx, 3.08, 3.85), size=vector(0.28, 0.1, 0.28), color=trim_color)

# Railings: balusters, top & bottom rails (front)
for x in [-1.7 + i * 0.2833 for i in range(13)]:
    box(pos=vector(x, 3.74, 3.88), size=vector(0.05, 0.9, 0.05), color=trim_color)
box(pos=vector(0, 4.22, 3.88), size=vector(3.7, 0.08, 0.12), color=trim_color)
box(pos=vector(0, 3.32, 3.88), size=vector(3.7, 0.06, 0.1), color=trim_color)
# Railings: sides
for sx in (-1.8, 1.8):
    for z in [2.7 + i * 0.2 for i in range(7)]:
        box(pos=vector(sx, 3.74, z), size=vector(0.05, 0.9, 0.05), color=trim_color)
    box(pos=vector(sx, 4.22, 3.28), size=vector(0.1, 0.08, 1.3), color=trim_color)
    box(pos=vector(sx, 3.32, 3.28), size=vector(0.1, 0.06, 1.3), color=trim_color)

# =====================================================
# PATH, FENCE, GATE
# =====================================================
for i in range(7):
    box(pos=vector(random.uniform(-0.08, 0.08), 0.03, 4.8 + i * 0.85),
        size=vector(1.4, 0.06, 0.65), color=vector(0.70, 0.68, 0.62), texture=textures.stones,
        axis=vector(1, 0, random.uniform(-0.06, 0.06)))

# White picket fence (compound for speed)
pickets = []
FZ = 9.2


def fence_line(x0, z0, x1, z1):
    length = mag(vector(x1 - x0, 0, z1 - z0))
    n = int(length / 0.45)
    d = norm(vector(x1 - x0, 0, z1 - z0))
    for i in range(n + 1):
        p = vector(x0, 0, z0) + d * (i * length / n)
        if abs(p.z - FZ) < 0.01 and abs(p.x) < 1.0:
            continue
        pickets.append(box(pos=p + vector(0, 0.45, 0), size=vector(0.12, 0.9, 0.04), color=trim_color))
    mid = vector((x0 + x1) / 2, 0.7, (z0 + z1) / 2)
    pickets.append(box(pos=mid, axis=vector(x1 - x0, 0, z1 - z0),
                       size=vector(length, 0.06, 0.05), color=trim_color))
    pickets.append(box(pos=mid + vector(0, -0.4, 0), axis=vector(x1 - x0, 0, z1 - z0),
                       size=vector(length, 0.06, 0.05), color=trim_color))


fence_line(-11.6, FZ, -1.0, FZ)
fence_line(1.0, FZ, 11.6, FZ)
fence_line(-11.6, FZ, -11.6, -10.4)
fence_line(11.6, FZ, 11.6, -10.4)
fence_line(-11.6, -10.4, 11.6, -10.4)
for gx in (-1.0, 1.0):
    pickets.append(box(pos=vector(gx, 0.65, FZ), size=vector(0.2, 1.3, 0.2), color=trim_color))
    pickets.append(sphere(pos=vector(gx, 1.35, FZ), radius=0.12, color=trim_color))
compound(pickets)

# Lamp posts along path (glow at night)
for lx in (-1.5, 1.5):
    cylinder(pos=vector(lx, 0, 6.6), axis=vector(0, 1.6, 0), radius=0.05, color=vector(0.1, 0.1, 0.1))
    lantern = sphere(pos=vector(lx, 1.72, 6.6), radius=0.17, color=vector(0.9, 0.9, 0.8), opacity=0.85)
    lamp_bulbs.append(lantern)
    lamp_lights.append(local_light(pos=vector(lx, 1.9, 6.7), color=color.black))
    box(pos=vector(lx, 1.93, 6.6), size=vector(0.3, 0.05, 0.3), color=vector(0.1, 0.1, 0.1))

# Mailbox
cylinder(pos=vector(2.0, 0, 9.7), axis=vector(0, 1.1, 0), radius=0.04, color=wood_color)
box(pos=vector(2.0, 1.2, 9.7), size=vector(0.28, 0.25, 0.5), color=vector(0.15, 0.20, 0.55), shininess=0.8)

# =====================================================
# GARDEN: BEDS, BUSHES, FLOWERS
# =====================================================
for bx in (-3.7, 3.7):
    box(pos=vector(bx, 0.05, 3.4), size=vector(2.4, 0.1, 1.6),
        color=vector(0.30, 0.18, 0.10), texture=textures.gravel)

flower_parts = []
palette = [vector(1, 0.1, 0.4), vector(1, 0.8, 0.1), vector(0.9, 0.3, 1.0),
           vector(1, 1, 1), vector(1, 0.4, 0.1)]
for bx in (-3.7, 3.7):
    for _ in range(14):
        fx = bx + random.uniform(-1.0, 1.0)
        fz = 3.4 + random.uniform(-0.65, 0.65)
        fh = random.uniform(0.3, 0.55)
        fc = random.choice(palette)
        flower_parts.append(cylinder(pos=vector(fx, 0.1, fz), axis=vector(0, fh, 0),
                                     radius=0.015, color=color.green))
        for k in range(5):
            a = k * 2 * pi / 5
            flower_parts.append(sphere(pos=vector(fx + 0.07 * cos(a), 0.1 + fh, fz + 0.07 * sin(a)),
                                       radius=0.05, color=fc))
        flower_parts.append(sphere(pos=vector(fx, 0.1 + fh, fz), radius=0.04, color=color.yellow))
compound(flower_parts)

# Bushes by the house
bush_parts = []
for bx in (-2.9, -1.0, 1.0, 2.9):
    for _ in range(4):
        g = random.uniform(0, 0.1)
        bush_parts.append(sphere(pos=vector(bx + random.uniform(-0.25, 0.25),
                                            0.45 + random.uniform(-0.1, 0.1),
                                            2.95 + random.uniform(-0.1, 0.15)),
                                 radius=random.uniform(0.28, 0.4), color=vector(0.05, 0.35 + g, 0.08)))
compound(bush_parts)

# =====================================================
# TREES
# =====================================================


def oak(x, z, s=1.0):
    parts = [cone(pos=vector(x, 0, z), axis=vector(0, 2.6 * s, 0), radius=0.34 * s,
                  color=vector(0.35, 0.22, 0.12), texture=textures.wood_old)]
    # branches
    for a in (0.5, 2.4, 4.3):
        parts.append(cylinder(pos=vector(x, 1.9 * s, z),
                              axis=vector(0.7 * s * cos(a), 0.8 * s, 0.7 * s * sin(a)),
                              radius=0.08 * s, color=vector(0.35, 0.22, 0.12)))
    for _ in range(11):
        g = random.uniform(0, 0.15)
        parts.append(sphere(pos=vector(x + random.uniform(-0.9, 0.9) * s,
                                       (2.9 + random.uniform(-0.3, 1.0)) * s,
                                       z + random.uniform(-0.9, 0.9) * s),
                            radius=random.uniform(0.6, 1.0) * s,
                            color=vector(0.04 + g * 0.3, 0.30 + g, 0.06)))
    compound(parts)
    shadows.append(ellipsoid(pos=vector(x + 1.4 * s, 0.014, z - 0.6 * s),
                             size=vector(3.2 * s, 0.01, 2.4 * s), color=color.black, opacity=0.22))


def pine(x, z, s=1.0):
    parts = [cylinder(pos=vector(x, 0, z), axis=vector(0, 1.2 * s, 0), radius=0.2 * s,
                      color=vector(0.3, 0.2, 0.1), texture=textures.wood_old)]
    for i in range(5):
        parts.append(cone(pos=vector(x, (0.9 + i * 0.85) * s, z), axis=vector(0, 1.6 * s, 0),
                          radius=(1.5 - i * 0.28) * s, color=vector(0.02, 0.28 + 0.03 * i, 0.12)))
    compound(parts)
    shadows.append(ellipsoid(pos=vector(x + 1.5 * s, 0.014, z - 0.6 * s),
                             size=vector(2.6 * s, 0.01, 1.8 * s), color=color.black, opacity=0.22))


oak(-5.5, 1.0, 1.0)
oak(6.0, 2.5, 1.15)
oak(-7.5, -3.5, 1.1)
pine(7.5, -3.5, 1.1)
pine(-9.5, 4.5, 0.9)
pine(9.5, 5.5, 0.9)

# =====================================================
# SKY: SUN, MOON, STARS, CLOUDS
# =====================================================
sun = sphere(pos=sun_pos, radius=0.9, color=color.yellow, emissive=True)
sun_glow = sphere(pos=sun_pos, radius=1.5, color=vector(1, 0.9, 0.4), opacity=0.25, emissive=True)
moon = sphere(pos=vector(8, 11, -2), radius=0.7, color=vector(0.92, 0.92, 0.85),
              emissive=True, visible=False)

stars = []
for _ in range(90):
    stars.append(sphere(pos=vector(random.uniform(-25, 25), random.uniform(8, 24), -22),
                        radius=random.uniform(0.04, 0.09), color=color.white,
                        emissive=True, visible=False))

clouds = []
for cx, cy, cz, sc in [(-14, 11.5, -14, 1.2), (3, 13, -16, 1.5), (14, 10.5, -12, 1.0), (-4, 9.8, -18, 1.3)]:
    pieces = []
    for dx, dy, rr in [(0, 0, 1.2), (1.1, -0.15, 0.95), (-1.1, -0.2, 0.9), (0.4, 0.45, 0.9), (-0.5, 0.3, 0.75)]:
        pieces.append(sphere(pos=vector(cx + dx * sc, cy + dy * sc, cz), radius=rr * sc, color=color.white))
    c = compound(pieces)
    clouds.append((c, random.uniform(0.01, 0.025)))

# Title label
label(pos=vector(0, 9.3, 0), text="MY DREAM HOUSE", height=22, box=False,
      color=color.white, opacity=0, line=False)

# =====================================================
# DAY / NIGHT TOGGLE
# =====================================================
lit_windows = [w for w in window_interiors if random.random() < 0.75]
night = False


def set_night(n):
    global night
    night = n
    scene.background = NIGHT_SKY if n else DAY_SKY
    scene.ambient = color.gray(0.12) if n else color.gray(0.40)
    sun_light.color = color.black if n else color.gray(0.75)
    fill_light.color = color.gray(0.05) if n else color.gray(0.25)
    moon_light.color = vector(0.18, 0.22, 0.38) if n else color.black
    sun.visible = sun_glow.visible = not n
    moon.visible = n
    for s in stars:
        s.visible = n
    for sh in shadows:
        sh.visible = not n
    for w in window_interiors:
        if n and w in lit_windows:
            w.color = vector(1.0, 0.82, 0.45)
            w.emissive = True
        else:
            w.color = vector(0.18, 0.16, 0.15)
            w.emissive = False
    for L in lamp_lights:
        L.color = vector(1.0, 0.8, 0.45) if n else color.black
    for b in lamp_bulbs:
        b.color = vector(1.0, 0.85, 0.5) if n else vector(0.9, 0.9, 0.8)
        b.emissive = n


# =====================================================
# KEYBOARD CONTROLS (N = day/night, arrows = rotate)
# =====================================================
def on_key(evt):
    k = evt.key.lower()
    if k == 'n':
        set_night(not night)
    elif k == 'left':
        scene.camera.rotate(angle=0.08, axis=vector(0, 1, 0), origin=scene.center)
    elif k == 'right':
        scene.camera.rotate(angle=-0.08, axis=vector(0, 1, 0), origin=scene.center)
    elif k == 'up':
        scene.camera.rotate(angle=0.05, axis=cross(scene.forward, scene.up), origin=scene.center)
    elif k == 'down':
        scene.camera.rotate(angle=-0.05, axis=cross(scene.forward, scene.up), origin=scene.center)


scene.bind('keydown', on_key)

# =====================================================
# ANIMATION: drifting clouds + chimney smoke
# =====================================================
smoke = []
frame = 0

while True:
    rate(30)
    frame += 1

    for c, speed in clouds:
        c.pos.x += speed
        if c.pos.x > 26:
            c.pos.x = -26
        c.visible = not night

    if frame % 14 == 0:
        smoke.append(sphere(pos=CHIMNEY_TOP + vector(random.uniform(-0.1, 0.1), 0, random.uniform(-0.1, 0.1)),
                            radius=0.15, color=vector(0.78, 0.78, 0.8), opacity=0.55))
    for p in smoke[:]:
        p.pos.y += 0.035
        p.pos.x += 0.012
        p.radius += 0.004
        p.opacity -= 0.0028
        if p.opacity <= 0.02:
            p.visible = False
            smoke.remove(p)