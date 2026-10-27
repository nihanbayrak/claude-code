"""Parametric generator for the I Ching #8 (Bi / Grouping) two-piece keychain.

Each piece is printed face-up (design on top), then the two flat backs are
glued together. This gives crisp top-surface detail on BOTH sides.

Output: keychain_front.stl, keychain_back.stl

Requires: pip install shapely manifold3d trimesh fonttools numpy
"""

import math
import sys
from pathlib import Path

import numpy as np
import trimesh
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from manifold3d import CrossSection, FillRule, Manifold
from shapely import affinity
from shapely.geometry import LinearRing, MultiPolygon, Point, Polygon, box
from shapely.ops import polygonize, unary_union

# ---------------------------------------------------------------- parameters (mm)
COIN_R = 25.0          # disc radius -> 50 mm coin
LUG_R = 7.0            # keyring lug radius
LUG_Y = 27.0           # lug centre
HOLE_D = 5.5           # keyring hole
HOLE_Y = 28.0
FILLET_R = 3.0         # blend between disc and lug
RIM_W = 2.0            # raised protective rim

BASE_H = 2.4           # solid base per piece (12 layers @ 0.2)
RELIEF_H = 1.2         # raised design height (6 layers @ 0.2)
CHAMFER = 0.4          # bed-side chamfer, hides elephant's foot at the glue seam

DOWEL_D = 2.1          # alignment holes for 1.75 mm filament dowels
DOWEL_DEPTH = 1.4
DOWEL_POS = [(-18.0, -4.0), (18.0, -4.0)]  # symmetric -> same on both pieces

# Hexagram 8 Bi: lines bottom->top (True = solid yang, False = broken yin)
HEXAGRAM = [False, False, False, False, True, False]
BAR_LEN = 26.0
BAR_T = 2.6
BAR_GAP = 1.7
BROKEN_GAP = 4.0
HEX_CY = 0.0

LATIN_FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
CJK_FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
TEXT_CAP = 5.0         # cap height of arc text
CJK_SIZE = 21.0        # height of the 比 character
CJK_BOLD = 0.3         # outline offset to thicken the light CJK strokes (~1.6 -> ~2.2 mm)
TRACKING = 0.06        # extra letter spacing (fraction of em)

CURVE_STEPS = 12
CIRCLE_RES = 256


# ---------------------------------------------------------------- font -> polygons
class FlattenPen(BasePen):
    """Collects glyph contours as point lists, flattening curves."""

    def __init__(self, glyph_set):
        super().__init__(glyph_set)
        self.contours, self.cur = [], []

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, CURVE_STEPS + 1):
            t = i / CURVE_STEPS
            mt = 1 - t
            self.cur.append(tuple(mt**3 * np.array(p0) + 3 * mt**2 * t * np.array(p1)
                                  + 3 * mt * t**2 * np.array(p2) + t**3 * np.array(p3)))

    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, CURVE_STEPS + 1):
            t = i / CURVE_STEPS
            mt = 1 - t
            self.cur.append(tuple(mt**2 * np.array(p0) + 2 * mt * t * np.array(p1) + t**2 * np.array(p2)))

    def _closePath(self):
        if len(self.cur) >= 3:
            self.contours.append(self.cur)
        self.cur = []

    _endPath = _closePath


class Font:
    def __init__(self, path, font_number=0):
        self.tt = TTFont(path, fontNumber=font_number)
        self.cmap = self.tt.getBestCmap()
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or 0.7 * self.upem

    def glyph(self, ch):
        """Return (shapely geometry in font units, advance width)."""
        name = self.cmap[ord(ch)]
        pen = FlattenPen(self.gs)
        self.gs[name].draw(pen)
        if not pen.contours:
            return Polygon(), self.gs[name].width
        # Non-zero winding fill (CJK fonts use overlapping strokes): split the plane into
        # faces and keep every face whose winding number is not zero.
        rings = [LinearRing(c) for c in pen.contours]
        dirs = [1 if Polygon(r).exterior.is_ccw else -1 for r in rings]
        areas = [Polygon(r) for r in rings]
        kept = []
        for face in polygonize(unary_union(rings)):
            pt = face.representative_point()
            if sum(d for d, a in zip(dirs, areas) if a.contains(pt)) != 0:
                kept.append(face)
        return unary_union(kept), self.gs[name].width


def text_on_arc(font, text, cap_h, baseline_r, centre_deg, outward_up):
    """Lay text along a circle, letters upright and centred on centre_deg.

    outward_up=True  -> top arc (letter tops point away from centre)
    outward_up=False -> bottom arc (letter tops point to centre)
    """
    s = cap_h / font.cap
    glyphs = [font.glyph(c) for c in text]
    advs = [(w + TRACKING * font.upem) * s for _, w in glyphs]
    total = sum(advs) - TRACKING * font.upem * s
    r_mid = baseline_r + (cap_h / 2 if outward_up else -cap_h / 2)
    out, pos = [], -total / 2
    for (g, w), adv in zip(glyphs, advs):
        if g.is_empty:
            pos += adv
            continue
        g = affinity.scale(g, s, s, origin=(0, 0))
        g = affinity.translate(g, -w * s / 2, 0)            # glyph centred on x=0
        centre = pos + w * s / 2
        dphi = centre / r_mid
        phi = math.radians(centre_deg) + (-dphi if outward_up else dphi)
        rot = math.degrees(phi) - 90 if outward_up else math.degrees(phi) + 90
        g = affinity.rotate(g, rot, origin=(0, 0))
        g = affinity.translate(g, baseline_r * math.cos(phi), baseline_r * math.sin(phi))
        out.append(g)
        pos += adv
    return unary_union(out)


def centred_glyph(font, ch, height, cx, cy):
    g, _ = font.glyph(ch)
    minx, miny, maxx, maxy = g.bounds
    s = height / (maxy - miny)
    g = affinity.scale(g, s, s, origin=(0, 0))
    minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, cx - (minx + maxx) / 2, cy - (miny + maxy) / 2)


# ---------------------------------------------------------------- geometry
def outline():
    disc = Point(0, 0).buffer(COIN_R, resolution=CIRCLE_RES // 4)
    lug = Point(0, LUG_Y).buffer(LUG_R, resolution=CIRCLE_RES // 4)
    body = disc.union(lug).buffer(FILLET_R, resolution=32).buffer(-FILLET_R, resolution=32)
    return body


def keyring_hole():
    return Point(0, HOLE_Y).buffer(HOLE_D / 2, resolution=CIRCLE_RES // 4)


def hexagram():
    bars, total = [], len(HEXAGRAM) * BAR_T + (len(HEXAGRAM) - 1) * BAR_GAP
    y0 = HEX_CY - total / 2
    for i, solid in enumerate(HEXAGRAM):
        y = y0 + i * (BAR_T + BAR_GAP)
        if solid:
            bars.append(box(-BAR_LEN / 2, y, BAR_LEN / 2, y + BAR_T))
        else:
            half = (BAR_LEN - BROKEN_GAP) / 2
            bars.append(box(-BAR_LEN / 2, y, -BAR_LEN / 2 + half, y + BAR_T))
            bars.append(box(BAR_LEN / 2 - half, y, BAR_LEN / 2, y + BAR_T))
    return unary_union(bars)


def to_cross_section(geom):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    rings = []
    for p in polys:
        if p.is_empty:
            continue
        rings.append(np.asarray(p.exterior.coords)[:-1])
        rings.extend(np.asarray(r.coords)[:-1] for r in p.interiors)
    return CrossSection(rings, FillRule.EvenOdd)


def slab(geom, z0, z1):
    return Manifold.extrude(to_cross_section(geom), z1 - z0).translate((0, 0, z0))


def build_piece(features):
    body = outline().difference(keyring_hole())
    inner = Point(0, 0).buffer(COIN_R - RIM_W, resolution=CIRCLE_RES // 4)
    frame = body.difference(inner)
    relief = unary_union([frame, features.intersection(inner.buffer(-0.01))]).difference(keyring_hole())

    solid = (slab(body.buffer(-CHAMFER, join_style="round"), 0.0, 0.2)
             + slab(body.buffer(-CHAMFER / 2, join_style="round"), 0.2, 0.4)
             + slab(body, 0.4, BASE_H)
             + slab(relief, BASE_H - 0.01, BASE_H + RELIEF_H))
    dowels = unary_union([Point(x, y).buffer(DOWEL_D / 2, resolution=16) for x, y in DOWEL_POS])
    solid = solid - slab(dowels, -0.1, DOWEL_DEPTH)
    return solid, relief


def to_trimesh(m):
    mesh = m.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                           faces=np.asarray(mesh.tri_verts), process=True)


def min_feature_report(name, geom, nozzle=0.4):
    """Area lost when eroding by half a 2-line width: shows strokes too thin to print."""
    eroded = geom.buffer(-nozzle).buffer(nozzle)
    lost = geom.area - eroded.area
    print(f"  {name}: area {geom.area:7.1f} mm2, lost to 0.8 mm opening test {lost:5.2f} mm2 "
          f"({100 * lost / geom.area:4.1f}%)")


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    latin = Font(LATIN_FONT)
    cjk = Font(CJK_FONT)

    inner_r = COIN_R - RIM_W
    top_baseline = inner_r - 1.5 - TEXT_CAP    # top arc text sits just inside the rim
    bottom_baseline = inner_r - 1.5            # bottom arc baseline next to the rim

    front_features = unary_union([
        hexagram(),
        text_on_arc(latin, "8", TEXT_CAP, top_baseline, 90, outward_up=True),
        text_on_arc(latin, "BǏ", TEXT_CAP, bottom_baseline, -90, outward_up=False),
    ])
    back_features = unary_union([
        centred_glyph(cjk, "比", CJK_SIZE - 2 * CJK_BOLD, 0, 1.5).buffer(CJK_BOLD, join_style="mitre"),
        text_on_arc(latin, "GROUPING", TEXT_CAP, bottom_baseline, -90, outward_up=False),
    ])

    print("Printability check (nozzle 0.4):")
    min_feature_report("front design", front_features)
    min_feature_report("back design", back_features)

    meshes = {}
    for name, feats in (("front", front_features), ("back", back_features)):
        solid, relief = build_piece(feats)
        tm = to_trimesh(solid)
        assert tm.is_watertight and tm.is_winding_consistent, f"{name} mesh not manifold"
        tm.export(out / f"keychain_{name}.stl")
        meshes[name] = tm
        ext = tm.extents
        print(f"{name}: {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, volume {tm.volume / 1000:.2f} cm3, "
              f"{len(tm.faces)} triangles, watertight={tm.is_watertight}")
    return meshes


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
