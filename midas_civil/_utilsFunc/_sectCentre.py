"""
centerline.py

Extract the wall centerline (medial axis / skeleton) of a thin-walled cross
section defined by an outer polygon and zero or more inner holes, together with
the local wall thickness along the centerline.

Typical use: box-girder / hollow sections where you want the "pink line" that
runs down the middle of the walls, flanges and slabs.

Main entry point
----------------
    extract_centerlines(outer_points, holes, ...) -> list of
        (x1, y1, x2, y2, thickness) tuples

Dependencies: numpy, scipy, scikit-image, pillow
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage.morphology import skeletonize


# --------------------------------------------------------------------------- #
#  Input normalisation
# --------------------------------------------------------------------------- #
def _normalise_holes(holes):
    """
    Accept:
        None
        single hole:    [(x,y), (x,y), ...]
        multiple holes: [[(x,y), ...], [(x,y), ...], ...]
    Return a list of holes, each a list of (x, y) tuples.
    """
    if holes is None:
        return []
    if len(holes) == 0:
        return []

    # Detect a single hole: its first element is a coordinate pair (2 numbers).
    first = holes[0]
    is_single = (
        isinstance(first, (tuple, list))
        and len(first) == 2
        and all(isinstance(v, (int, float, np.integer, np.floating)) for v in first)
    )
    if is_single:
        return [list(holes)]
    return [list(h) for h in holes]


# --------------------------------------------------------------------------- #
#  Rasterisation
# --------------------------------------------------------------------------- #
def _rasterise(outer, holes, px):
    """
    Rasterise the *wall* region (outer polygon minus holes) into a boolean mask.

    Returns
    -------
    mask   : (H, W) bool array, True = wall material
    origin : (minx, miny) real-world coordinate of pixel (col=0, row=0)
    scale  : real-world units per pixel  (real = pixel * scale + origin)
    """
    pts = np.asarray(outer, dtype=float)
    for h in holes:
        pts = np.vstack([pts, np.asarray(h, dtype=float)])

    minx, miny = pts[:, 0].min(), pts[:, 1].min()
    maxx, maxy = pts[:, 0].max(), pts[:, 1].max()

    span = max(maxx - minx, maxy - miny)
    if span == 0:
        raise ValueError("Degenerate geometry (zero extent).")

    pad = 2  # pixels of background border so the skeleton never touches the edge
    scale = span / (px - 2 * pad)

    def to_px(poly):
        arr = np.asarray(poly, dtype=float)
        cols = (arr[:, 0] - minx) / scale + pad
        rows = (arr[:, 1] - miny) / scale + pad
        return list(zip(cols, rows))

    W = int(np.ceil((maxx - minx) / scale)) + 2 * pad + 1
    H = int(np.ceil((maxy - miny) / scale)) + 2 * pad + 1

    img = Image.new("L", (W, H), 0)
    drw = ImageDraw.Draw(img)
    drw.polygon(to_px(outer), fill=1)
    for h in holes:
        drw.polygon(to_px(h), fill=0)

    mask = np.array(img, dtype=bool)
    origin = (minx - pad * scale, miny - pad * scale)
    return mask, origin, scale


# --------------------------------------------------------------------------- #
#  Skeleton -> graph -> polylines
# --------------------------------------------------------------------------- #
_NEIGH = [(-1, -1), (-1, 0), (-1, 1),
          (0, -1),           (0, 1),
          (1, -1),  (1, 0),  (1, 1)]


def _neighbours(r, c, skel):
    out = []
    H, W = skel.shape
    for dr, dc in _NEIGH:
        rr, cc = r + dr, c + dc
        if 0 <= rr < H and 0 <= cc < W and skel[rr, cc]:
            out.append((rr, cc))
    return out


def _trace_polylines(skel):
    """
    Convert a 1-pixel-wide skeleton into a set of polylines (lists of (r, c)).

    Paths are split at nodes (endpoints with 1 neighbour and junctions with >2
    neighbours). Pure loops with no node are emitted as closed polylines.
    """
    skel = skel.copy()
    deg = np.zeros(skel.shape, dtype=np.uint8)
    ys, xs = np.nonzero(skel)
    for r, c in zip(ys, xs):
        deg[r, c] = len(_neighbours(r, c, skel))

    nodes = {(r, c) for r, c in zip(ys, xs) if deg[r, c] != 2}
    polylines = []
    visited_edges = set()

    def walk(start, second):
        path = [start, second]
        prev, cur = start, second
        while cur not in nodes:
            nxt = [p for p in _neighbours(*cur, skel) if p != prev]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            path.append(cur)
            if cur == start:  # safety against tiny loops
                break
        return path

    # Trace edges starting from every node.
    for node in nodes:
        for nb in _neighbours(*node, skel):
            edge = frozenset((node, nb))
            if edge in visited_edges:
                continue
            path = walk(node, nb)
            for a, b in zip(path[:-1], path[1:]):
                visited_edges.add(frozenset((a, b)))
            polylines.append(path)

    # Handle isolated loops (no nodes at all on the component).
    remaining = {(r, c) for r, c in zip(ys, xs)}
    for pl in polylines:
        remaining.difference_update(pl)
    while remaining:
        start = next(iter(remaining))
        nbs = _neighbours(*start, skel)
        if not nbs:
            remaining.discard(start)
            continue
        path = walk(start, nbs[0])
        for p in path:
            remaining.discard(p)
        polylines.append(path)

    return polylines


# --------------------------------------------------------------------------- #
#  Douglas-Peucker polyline simplification
# --------------------------------------------------------------------------- #
def _rdp(points, eps):
    """Ramer-Douglas-Peucker simplification on a list of (x, y)."""
    if len(points) < 3:
        return points
    pts = np.asarray(points, dtype=float)
    start, end = pts[0], pts[-1]
    line = end - start
    llen = np.hypot(*line)
    if llen == 0:
        dists = np.hypot(*(pts - start).T)
    else:
        rel = pts - start
        # 2-D cross product (avoids numpy>=2 np.cross deprecation on 2-D vectors)
        dists = np.abs(line[0] * rel[:, 1] - line[1] * rel[:, 0]) / llen
    idx = int(np.argmax(dists))
    if dists[idx] > eps:
        left = _rdp(points[: idx + 1], eps)
        right = _rdp(points[idx:], eps)
        return left[:-1] + right
    return [points[0], points[-1]]


# --------------------------------------------------------------------------- #
#  Slab straightening  (make top/bottom slabs continuous horizontal lines)
# --------------------------------------------------------------------------- #
def _seg_len(s):
    return float(np.hypot(s[2] - s[0], s[3] - s[1]))


def _seg_angle_h(s):
    """Angle of a segment to the horizontal, in degrees (0..90)."""
    a = abs(np.degrees(np.arctan2(s[3] - s[1], s[2] - s[0])))
    return min(a, 180 - a)


def straighten_slabs(segments, angle_tol_deg=25.0, y_cluster_frac=0.12,
                     min_web_frac=0.05, min_slab_frac=0.03,
                     dist=None, origin=None, scale=None):
    """
    Rebuild a thin-walled-section centerline so that the top and bottom slabs
    are single continuous horizontal lines and the webs are straight lines,
    kept centred in the wall, running between them.

    Only geometry is produced here (thickness is measured separately, along the
    cleaned-up lines). Each returned segment carries a `kind` tag so the caller
    can measure thickness appropriately.

    Parameters
    ----------
    segments : list whose items start with (x1, y1, x2, y2, ...)
        Raw centerline segments from the medial axis (extra fields ignored).
    angle_tol_deg : float
        A segment within this many degrees of horizontal counts as slab.
    y_cluster_frac : float
        Horizontal segments whose mid-height differs by less than
        y_cluster_frac * (section height) are merged into the same slab "rail".
    min_web_frac : float
        Web chains shorter than this fraction of the bounding-box diagonal are
        treated as noise (e.g. skeleton spurs at flange tips) and dropped.
    min_slab_frac : float
        Near-horizontal fragments shorter than this fraction of the diagonal are
        ignored (they are usually skeleton "caps" at the ends of vertical webs).

    dist, origin, scale :
        If provided (the distance transform, raster origin and scale from the
        rasteriser), each returned segment carries two end thicknesses measured
        from the medial axis, i.e. (x1, y1, x2, y2, thk1, thk2). Otherwise only
        geometry + a kind tag is returned: (x1, y1, x2, y2, kind).

    Returns
    -------
    list of (x1, y1, x2, y2, thk1, thk2)   if dist is given, else
    list of (x1, y1, x2, y2, kind)         with kind in {"slab", "web"}.
    """
    have_thk = dist is not None and origin is not None and scale is not None
    segs = [tuple(s) for s in segments]
    if not segs:
        return []

    P = np.array([[s[0], s[1]] for s in segs] + [[s[2], s[3]] for s in segs])
    W, H = np.ptp(P[:, 0]), np.ptp(P[:, 1])
    diag = float(np.hypot(W, H))
    y_tol = y_cluster_frac * H

    # A short near-horizontal fragment is usually a skeleton "cap" at the end
    # of a (near-)vertical web, not a real slab -- drop it so it does not become
    # a spurious rail.
    min_slab_len = min_slab_frac * diag
    horiz = [s for s in segs
             if _seg_angle_h(s) <= angle_tol_deg and _seg_len(s) >= min_slab_len]
    other = [s for s in segs if _seg_angle_h(s) > angle_tol_deg]

    # --- cluster horizontal segments into rails by mid-height -------------- #
    rails = []
    for _, s in sorted(((0.5 * (s[1] + s[3]), s) for s in horiz),
                       key=lambda t: t[0]):
        ymid = 0.5 * (s[1] + s[3])
        if rails and (ymid - rails[-1]["_lasty"]) <= y_tol:
            rails[-1]["_segs"].append(s)
        else:
            rails.append({"_segs": [s]})
        rails[-1]["_lasty"] = ymid

    rail_specs = []  # [y_rep, xmin, xmax, medial_segments]
    for r in rails:
        ss = r["_segs"]
        L = np.array([_seg_len(s) for s in ss])
        if L.sum() == 0:
            continue
        y_rep = np.average([0.5 * (s[1] + s[3]) for s in ss], weights=L)
        xs = [s[0] for s in ss] + [s[2] for s in ss]
        rail_specs.append([float(y_rep), float(min(xs)), float(max(xs)), ss])

    if not rail_specs:  # nothing horizontal -> leave geometry unchanged
        if have_thk:
            return [(s[0], s[1], s[2], s[3],
                     *_raw_end_thicknesses(s, dist, origin, scale)) for s in segs]
        return [(s[0], s[1], s[2], s[3], "web") for s in segs]

    # --- group the non-horizontal segments into connected web chains ------- #
    tol = 0.01 * diag
    nodes = []

    def nid(x, y):
        for i, (nx, ny) in enumerate(nodes):
            if abs(nx - x) <= tol and abs(ny - y) <= tol:
                return i
        nodes.append((x, y))
        return len(nodes) - 1

    adj = defaultdict(list)
    oe = []
    for s in other:
        a, b = nid(s[0], s[1]), nid(s[2], s[3])
        oe.append((a, b, s))
        adj[a].append(len(oe) - 1)
        adj[b].append(len(oe) - 1)

    seen, comps = set(), []
    for start in range(len(oe)):
        if start in seen:
            continue
        stack, comp = [start], []
        while stack:
            e = stack.pop()
            if e in seen:
                continue
            seen.add(e)
            comp.append(e)
            a, b, _ = oe[e]
            for e2 in adj[a] + adj[b]:
                if e2 not in seen:
                    stack.append(e2)
        comps.append(comp)

    # --- reconstruct each web as a straight, centred line between two rails - #
    webs = []
    for comp in comps:
        pts, tot_len = [], 0.0
        for e in comp:
            s = oe[e][2]
            for t in np.linspace(0, 1, 12):
                pts.append((s[0] + t * (s[2] - s[0]),
                            s[1] + t * (s[3] - s[1])))
            tot_len += _seg_len(s)
        if tot_len < min_web_frac * diag:
            continue
        pts = np.array(pts)
        ys = pts[:, 1]
        ymin_c, ymax_c = ys.min(), ys.max()
        span = ymax_c - ymin_c
        if span <= 0:
            continue

        # Fit direction to the web *trunk* only (middle band). The medial axis
        # is exactly centred between the two walls along the straight trunk, but
        # fans out near the slab junctions -- using the trunk keeps the web line
        # centred instead of leaning inward.
        band = (ys >= ymin_c + 0.25 * span) & (ys <= ymax_c - 0.25 * span)
        trunk = pts[band] if band.sum() >= 4 else pts
        c = trunk.mean(0)
        _, _, vt = np.linalg.svd(trunk - c)
        d = vt[0]
        if abs(d[1]) < 1e-9:
            continue  # (near-)horizontal chain: not a web, skip

        top_i = min(range(len(rail_specs)),
                    key=lambda i: abs(rail_specs[i][0] - ymax_c))
        bot_i = min(range(len(rail_specs)),
                    key=lambda i: abs(rail_specs[i][0] - ymin_c))
        y_top, y_bot = rail_specs[top_i][0], rail_specs[bot_i][0]
        if top_i == bot_i:  # only one rail near this web
            y_top, y_bot = ymax_c, ymin_c

        def at_y(yv):
            t = (yv - c[1]) / d[1]
            return c[0] + t * d[0]

        xt, xb = at_y(y_top), at_y(y_bot)

        if have_thk:
            # thickness from the medial-axis trunk points (2*DT), fitted along
            # the web and extrapolated to the two ends. Trunk points lie in the
            # clear web, so this is unaffected by the junction "blow-up".
            us, vs = [], []
            for px, py in pts:  # full clean strip; _fit_eval drops junction spikes
                v = _dt_thk(px, py, dist, origin, scale)
                if v is not None:
                    us.append((py - y_top) / (y_bot - y_top)
                              if y_bot != y_top else 0.0)
                    vs.append(v)
            thk1, thk2 = _fit_eval(us, vs, [0.0, 1.0])
            webs.append((xt, y_top, xb, y_bot, round(thk1, 6), round(thk2, 6)))
        else:
            webs.append((xt, y_top, xb, y_bot, "web"))

        # extend the attached rails so they actually reach the web
        if top_i != bot_i:
            for ri, xv in ((top_i, xt), (bot_i, xb)):
                rail_specs[ri][1] = min(rail_specs[ri][1], xv)
                rail_specs[ri][2] = max(rail_specs[ri][2], xv)

    out = []
    for y, xmin, xmax, ss in rail_specs:
        if (xmax - xmin) < min_slab_len:
            continue
        if have_thk:
            us, vs = [], []
            for s in ss:
                for t in np.linspace(0.1, 0.9, 7):
                    px = s[0] + t * (s[2] - s[0])
                    py = s[1] + t * (s[3] - s[1])
                    v = _dt_thk(px, py, dist, origin, scale)
                    if v is not None:
                        us.append(px)
                        vs.append(v)
            thk1, thk2 = _fit_eval(us, vs, [xmin, xmax])
            out.append((xmin, y, xmax, y, round(thk1, 6), round(thk2, 6)))
        else:
            out.append((xmin, y, xmax, y, "slab"))
    out.extend(webs)
    return out


def _dt_thk(x, y, dist, origin, scale):
    """Wall thickness at a point ON the medial axis = 2 * distance transform."""
    c = int(round((x - origin[0]) / scale))
    r = int(round((y - origin[1]) / scale))
    H, W = dist.shape
    if 0 <= r < H and 0 <= c < W and dist[r, c] > 0:
        return 2.0 * dist[r, c] * scale
    return None


def _fit_eval(us, vs, at):
    """
    Robust straight-line fit of thickness `vs` vs parameter `us`, evaluated at
    the parameter values in `at`. Junction spikes / dropouts are rejected around
    the median first. Falls back to the median if a fit is not possible.
    """
    us, vs = np.asarray(us, float), np.asarray(vs, float)
    if len(vs) == 0:
        return [0.0 for _ in at]
    med = np.median(vs)
    keep = (vs <= 2.5 * med) & (vs >= 0.4 * med)
    if keep.sum() >= 2:
        us, vs = us[keep], vs[keep]
    if len(vs) >= 2 and np.ptp(us) > 1e-9:
        m, b = np.linalg.lstsq(np.vstack([us, np.ones_like(us)]).T, vs,
                               rcond=None)[0]
        return [max(float(b + m * u), 0.0) for u in at]
    return [max(float(np.median(vs)), 0.0) for _ in at]


def _raw_end_thicknesses(seg, dist, origin, scale):
    """Two-ended thickness for a raw medial-axis segment (samples 2*DT)."""
    x1, y1, x2, y2 = seg[:4]
    dx, dy = x2 - x1, y2 - y1

    def band(a, b):
        vals = [v for t in np.linspace(a, b, 8)
                if (v := _dt_thk(x1 + t * dx, y1 + t * dy, dist,
                                 origin, scale)) is not None]
        return float(np.median(vals)) if vals else None

    mid = band(0.3, 0.7) or 0.0
    t1 = band(0.05, 0.2)
    t2 = band(0.8, 0.95)
    return (round(t1 if t1 is not None else mid, 6),
            round(t2 if t2 is not None else mid, 6))


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
def extract_centerlines(
    outer_points,
    holes=None,
    resolution=1400,
    simplify_tol=1.5,
    prune_frac=0.02,
    straighten=True,
    angle_tol_deg=25.0,
    y_cluster_frac=0.12,
    return_polylines=False,
):
    """
    Compute the wall centerline of a section with holes.

    Parameters
    ----------
    outer_points : list of (x, y)
        Outer boundary polygon (open or closed; order irrelevant).
    holes : None | [(x,y),...] | [[(x,y),...], [(x,y),...], ...]
        A single hole or a list of holes. None / [] means solid section.
    resolution : int
        Raster size (longest side, in pixels). Higher = more accurate centerline
        position & thickness, but slower. 1000-2000 is usually plenty.
    simplify_tol : float
        Douglas-Peucker tolerance, in REAL-WORLD units. Larger -> fewer, longer
        straight segments. Set 0 to keep every pixel step.
    prune_frac : float
        Skeletonisation creates small spurious spurs at junctions. Any leaf
        branch shorter than prune_frac * (bounding-box diagonal) is removed.
        Set 0 to disable pruning.
    straighten : bool
        If True (default), post-process the raw medial axis so the top and
        bottom slabs become single continuous HORIZONTAL lines and the webs
        become straight lines running between them (matches the reference
        "stick model" look). Set False to return the raw medial axis.
    angle_tol_deg, y_cluster_frac :
        Passed to straighten_slabs (see that function). angle_tol_deg is how
        close to horizontal a segment must be to count as slab; y_cluster_frac
        controls how slab pieces at slightly different heights are merged.
    return_polylines : bool
        If True, also return the connected polylines (list of list of (x, y))
        for plotting / further processing. (Polylines are the RAW medial axis,
        before straightening.)

    Returns
    -------
    segments : list of (x1, y1, x2, y2, thk1, thk2)
        One entry per straight centerline segment. `thk1` / `thk2` are the wall
        thickness (real-world units) at end 1 / end 2, so a tapered member is
        described by its two end thicknesses.
    polylines : list of list of (x, y)      (only if return_polylines=True)
    """
    holes = _normalise_holes(holes)
    mask, origin, scale = _rasterise(outer_points, holes, resolution)

    # Distance transform: value at a pixel = distance (px) to nearest background.
    # Along the skeleton this equals HALF the local wall thickness.
    dist = ndimage.distance_transform_edt(mask)

    skel = skeletonize(mask)

    # --- prune tiny spurs -------------------------------------------------- #
    if prune_frac and prune_frac > 0:
        pts = np.asarray(outer_points, float)
        diag = np.hypot(np.ptp(pts[:, 0]), np.ptp(pts[:, 1]))
        min_len_px = (prune_frac * diag) / scale
        skel = _prune_spurs(skel, min_len_px)

    polylines_px = _trace_polylines(skel)

    ox, oy = origin
    segments = []
    polylines_xy = []

    raw_geo = []  # (x1, y1, x2, y2) medial-axis segments
    for path in polylines_px:
        if len(path) < 2:
            continue
        xy = [(c * scale + ox, r * scale + oy) for (r, c) in path]
        polylines_xy.append(xy)
        simp = _rdp(xy, simplify_tol) if (simplify_tol and simplify_tol > 0) else xy
        for k in range(len(simp) - 1):
            (x1, y1), (x2, y2) = simp[k], simp[k + 1]
            raw_geo.append((x1, y1, x2, y2))

    if straighten:
        # straighten_slabs measures the two end thicknesses itself (from the
        # medial axis) when given the distance transform.
        segments = straighten_slabs(raw_geo, angle_tol_deg=angle_tol_deg,
                                    y_cluster_frac=y_cluster_frac,
                                    dist=dist, origin=origin, scale=scale)
    else:
        segments = [(x1, y1, x2, y2,
                     *_raw_end_thicknesses((x1, y1, x2, y2), dist, origin, scale))
                    for (x1, y1, x2, y2) in raw_geo]

    if return_polylines:
        return segments, polylines_xy
    return segments


def _prune_spurs(skel, min_len_px):
    """Iteratively remove short leaf branches (spurs) from a skeleton."""
    skel = skel.copy()
    changed = True
    while changed:
        changed = False
        ys, xs = np.nonzero(skel)
        endpoints = [
            (r, c) for r, c in zip(ys, xs) if len(_neighbours(r, c, skel)) == 1
        ]
        for ep in endpoints:
            if not skel[ep]:
                continue
            # walk from the endpoint until we hit a junction (>2) or another end
            path = [ep]
            prev, cur = None, ep
            while True:
                nbs = [p for p in _neighbours(*cur, skel) if p != prev]
                if len(nbs) != 1:
                    break
                prev, cur = cur, nbs[0]
                if len(_neighbours(*cur, skel)) > 2:
                    break
                path.append(cur)
            if len(path) < min_len_px:
                for p in path:
                    skel[p] = False
                changed = True
    return skel


# --------------------------------------------------------------------------- #
#  Display
# --------------------------------------------------------------------------- #
def plot_centerlines(outer_points, holes, segments, ax=None, title=None,
                     show_thickness=True, show_labels=True, show=False,
                     savepath=None):
    """
    Draw the section outline (outer polygon + holes) and the extracted
    centerline, showing each segment's taper as a shaded band with its two end
    thickness values labelled.

    Parameters
    ----------
    outer_points, holes : same inputs you passed to extract_centerlines.
    segments : list of (x1, y1, x2, y2, thk1, thk2) from extract_centerlines.
    ax : an existing matplotlib Axes to draw on (a new figure is made if None).
    show_thickness : shade a band of the local thickness around each segment.
    show_labels : print the thk1 / thk2 value at each segment end.
    show : call plt.show() at the end.
    savepath : if given, save the figure to this path.

    Returns the matplotlib Axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(11, 5))

    # --- section outline ------------------------------------------------- #
    op = np.asarray(list(outer_points) + [outer_points[0]], float)
    ax.plot(op[:, 0], op[:, 1], "k-", lw=1.3)
    hs = _normalise_holes(holes)
    for h in hs:
        hp = np.asarray(list(h) + [h[0]], float)
        ax.plot(hp[:, 0], hp[:, 1], "k-", lw=1.3)

    # --- centerline segments --------------------------------------------- #
    for x1, y1, x2, y2, t1, t2 in segments:
        dx, dy = x2 - x1, y2 - y1
        L = np.hypot(dx, dy)
        if L == 0:
            continue
        if show_thickness:
            nx, ny = -dy / L, dx / L            # unit normal
            band = np.array([
                [x1 + nx * t1 / 2, y1 + ny * t1 / 2],
                [x2 + nx * t2 / 2, y2 + ny * t2 / 2],
                [x2 - nx * t2 / 2, y2 - ny * t2 / 2],
                [x1 - nx * t1 / 2, y1 - ny * t1 / 2],
            ])
            ax.fill(band[:, 0], band[:, 1], color="deeppink", alpha=0.15,
                    zorder=2, lw=0)
        ax.plot([x1, x2], [y1, y2], "-", color="deeppink", lw=2, zorder=4)
        ax.plot([x1, x2], [y1, y2], "o", color="deeppink", ms=4, zorder=5)
        if show_labels:
            ax.text(x1 + 0.12 * dx, y1 + 0.12 * dy, f"{t1:.1f}",
                    fontsize=7, color="navy", ha="center", va="center", zorder=6)
            ax.text(x2 - 0.12 * dx, y2 - 0.12 * dy, f"{t2:.1f}",
                    fontsize=7, color="navy", ha="center", va="center", zorder=6)

    ax.set_aspect("equal")
    ax.autoscale()
    if title:
        ax.set_title(title)
    if savepath:
        ax.figure.tight_layout()
        ax.figure.savefig(savepath, dpi=120)
    if show:
        plt.show()
    return ax


# --------------------------------------------------------------------------- #
#  Demo / self-test
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Single-cell trapezoidal box girder (left figure)
    outer = [
        (0, 100), (600, 100),          # top flange top edge
        (600, 0), (0, 0),          # right cantilever underside
    ]
    hole = [
        (250, 70), (350, 70),
        (350, 20), (250, 20),
    ]

    segs = extract_centerlines(outer, hole, resolution=1400,
                               simplify_tol=3.0, prune_frac=0.03)
    print(f"{len(segs)} centerline segments  (x1, y1, x2, y2, thk1, thk2)")
    for s in segs:
        print("  ({:.1f}, {:.1f}) -> ({:.1f}, {:.1f})  "
              "thk1={:.2f}  thk2={:.2f}".format(*s))

    # Display the result
    plot_centerlines(outer, hole, segs, title="Box-girder centerline",
                     savepath="centerline_demo.png", show=True)
    print("Saved plot to centerline_demo.png")