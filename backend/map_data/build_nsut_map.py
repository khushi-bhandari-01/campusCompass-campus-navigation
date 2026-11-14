"""Generates campus_map.json for the NSUT campus (schematic, redrawn from the official NSUT map).

Coordinates below are written in the pixel space of the NSUT map image, then scaled to the SVG canvas.
Run:  python map_data/build_nsut_map.py     (re-creates campus_map.json)
Calibrate real-world distances by changing METERS_PER_UNIT.
"""
import json, math, random
from pathlib import Path

SX, SY, OX, OY = 1.22, 1.15, 10, 195          # image px -> canvas units
METERS_PER_UNIT = 0.8                          # approximate; adjust to your real campus scale
W, H = 900, 640

def P(x, y):  return (round((x - OX) * SX), round((y - OY) * SY))
def R(x, y, w, h):
    x1, y1 = P(x, y); x2, y2 = P(x + w, y + h)
    return x1, y1, x2 - x1, y2 - y1

nodes_src = [
    # id, name, type, image x, y
    ("G_NORTH", "North Gate", "gate", 72, 205), ("G_MAIN", "Main Gate", "gate", 72, 595),
    ("J1", "Junction 1", "junction", 75, 240), ("J2", "Junction 2", "junction", 88, 360),
    ("J3", "Junction 3", "junction", 95, 515), ("J4", "Junction 4", "junction", 100, 640),
    ("J5", "Junction 5", "junction", 215, 358), ("J6", "Junction 6", "junction", 215, 492),
    ("J7", "Junction 7", "junction", 300, 632), ("J8", "Junction 8", "junction", 530, 620),
    ("J9", "Junction 9", "junction", 580, 612), ("J10", "Junction 10", "junction", 575, 470),
    ("J11", "Junction 11", "junction", 470, 468), ("J12", "Junction 12", "junction", 440, 218),
    ("J13", "Junction 13", "junction", 262, 218), ("J14", "Junction 14", "junction", 140, 225),
    ("J15", "Junction 15", "junction", 455, 380), ("J16", "Junction 16", "junction", 575, 385),
    ("J17", "Junction 17", "junction", 255, 328), ("J18", "Junction 18", "junction", 330, 308),
    ("J19", "Junction 19", "junction", 375, 302), ("J20", "Junction 20", "junction", 235, 568),
    ("E_AMUL", "Amul Ground entrance", "entrance", 200, 222), ("E_APJ", "APJ Halls entrance", "entrance", 307, 218),
    ("E_SMART", "Smart Block entrance", "entrance", 390, 218), ("E_CLINIC", "Clinic entrance", "entrance", 448, 300),
    ("E_N1", "NESCII 1 entrance", "entrance", 215, 432), ("E_N2", "NESCII 2 entrance", "entrance", 200, 497),
    ("E_ADM", "Admin entrance", "entrance", 262, 476), ("E_AUDI", "Main Auditorium entrance", "entrance", 300, 476),
    ("E_B6", "Block 6 entrance", "entrance", 360, 474), ("E_B4", "Block 4 entrance", "entrance", 396, 476),
    ("E_FNT", "Fountain entrance", "entrance", 434, 474), ("E_B5", "Block 5 entrance", "entrance", 490, 468),
    ("E_LIB", "SAC Library entrance", "entrance", 524, 462), ("E_BB", "Basketball Court entrance", "entrance", 582, 505),
    ("E_TRACK", "Running Track entrance", "entrance", 585, 590), ("E_CBT", "CBT & Mini Auditorium entrance", "entrance", 476, 626),
    ("E_CRICKET", "Cricket Ground entrance", "entrance", 610, 388),
]
nodes = [{"id": i, "name": n, "type": t, "x": P(x, y)[0], "y": P(x, y)[1]} for i, n, t, x, y in nodes_src]
pos = {n["id"]: (n["x"], n["y"]) for n in nodes}

roads = """G_NORTH-J1 J1-J2 J2-J3 J3-G_MAIN G_MAIN-J4
J1-J14 J14-E_AMUL E_AMUL-J13 J13-E_APJ E_APJ-E_SMART E_SMART-J12
J12-E_CLINIC E_CLINIC-J15 J2-J5 J5-E_N1 E_N1-J6 J3-E_N2 E_N2-J6
J6-E_ADM E_ADM-E_AUDI E_AUDI-E_B6 E_B6-E_B4 E_B4-E_FNT E_FNT-J11 J11-E_B5 E_B5-E_LIB E_LIB-J10
J11-J15 J15-J16 J16-J10 J16-E_CRICKET J10-E_BB E_BB-E_TRACK E_TRACK-J9
J4-J7 J7-E_CBT E_CBT-J8 J8-J9""".split()
ring = "J5-J17 J17-J18 J18-J19 J19-J15".split()          # curved ring road: weight x1.1
shortcuts = "J6-J20 J20-J7".split()                      # footpaths

edges = []
def add(pair, kind, factor):
    a, b = pair.split("-")
    d = math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1])
    edges.append({"id": f"e{len(edges)+1}", "source": a, "target": b, "weight": round(d * factor + 1e-6, 1) if factor > 1 else round(math.ceil(d * 10) / 10, 1), "kind": kind})
for p in roads: add(p, "road", 1.0)
for p in ring: add(p, "road", 1.1)
for p in shortcuts: add(p, "shortcut", 1.05)

# id, name, label lines, description, rect (image px), entrance, kind
b_src = [
    ("amul", "Amul Ground", ["Amul", "Ground"], "Open ground", (142, 242, 116, 108), "E_AMUL", "ground"),
    ("apj_halls", "APJ Halls", ["APJ", "Halls"], "APJ Halls", (268, 238, 78, 52), "E_APJ", None),
    ("smart_block", "Smart Block", ["Smart", "Block"], "Smart Block", (362, 238, 56, 44), "E_SMART", None),
    ("clinic", "Clinic", ["Clinic"], "Campus clinic", (468, 282, 48, 26), "E_CLINIC", None),
    ("nescii1", "NESCII 1", ["NESCII 1"], "NESCII 1", (105, 380, 95, 105), "E_N1", None),
    ("nescii2", "NESCII 2", ["NESCII 2"], "NESCII 2", (172, 515, 56, 34), "E_N2", None),
    ("admin", "Admin", ["Admin"], "Administrative offices", (240, 425, 46, 36), "E_ADM", None),
    ("main_audi", "Main Auditorium", ["Main", "Audi"], "Main auditorium", (278, 498, 44, 38), "E_AUDI", None),
    ("block6", "Block 6", ["Block 6"], "Academic Block 6", (318, 398, 84, 50), "E_B6", None),
    ("block4", "Block 4", ["Block 4"], "Academic Block 4", (350, 500, 92, 66), "E_B4", None),
    ("fountain", "Fountain", ["Fountain"], "Central fountain", (412, 442, 44, 22), "E_FNT", None),
    ("block5", "Block 5", ["Block 5"], "Academic Block 5", (448, 498, 84, 60), "E_B5", None),
    ("library", "SAC Library", ["SAC", "Library"], "Student Activity Centre and library", (488, 402, 72, 44), "E_LIB", None),
    ("basketball", "Basketball Court", ["Basketball", "Court"], "Basketball court", (606, 470, 60, 62), "E_BB", None),
    ("running_track", "Running Track", ["Running", "Track"], "Running track", (606, 548, 100, 140), "E_TRACK", "ground"),
    ("cbt", "CBT & Mini Auditorium", ["CBT &", "Mini Audi"], "CBT centre and mini auditorium", (445, 566, 62, 30), "E_CBT", None),
    ("cricket", "Cricket Ground", ["Cricket", "Ground"], "Cricket ground", (632, 300, 90, 100), "E_CRICKET", "ground"),
]
buildings = []
for i, name, lines, desc, rect, ent, kind in b_src:
    x, y, w, h = R(*rect)
    b = {"id": i, "name": name, "label_lines": lines, "description": desc, "x": x, "y": y, "w": w, "h": h, "entrance": ent}
    if kind: b["kind"] = kind
    buildings.append(b)

locations = []
for n in nodes:
    if n["type"] == "gate":
        locations.append({"id": "main_gate" if n["id"] == "G_MAIN" else "north_gate", "name": n["name"], "type": "gate", "node": n["id"], "x": n["x"], "y": n["y"]})
for b in buildings:
    locations.append({"id": b["id"], "name": b["name"], "type": "ground" if b.get("kind") == "ground" else "building", "node": b["entrance"], "x": pos[b["entrance"]][0], "y": pos[b["entrance"]][1]})

fx, fy, fw, fh = R(410, 640, 175, 85)
green = [{"id": "south_field", "name": "South Field", "x": fx, "y": fy, "w": fw, "h": fh, "label_x": fx + fw // 2, "label_y": fy + fh - 10}]

rng = random.Random(7)
trees = []
def scatter(rect, n, rmin=6, rmax=9, avoid_label=False):
    x, y, w, h = rect
    for _ in range(n):
        trees.append({"x": rng.randint(x + 10, x + w - 10), "y": rng.randint(y + 10, y + h - 24 if avoid_label else y + h - 10), "r": rng.randint(rmin, rmax)})
scatter((fx, fy, fw, fh), 9, avoid_label=True)
for (x, y) in [(28, 70), (30, 300), (34, 420), (40, 560), (800, 40), (860, 120), (700, 70), (870, 470), (840, 590), (24, 610), (760, 215), (180, 600), (250, 20), (560, 40)]:
    trees.append({"x": x, "y": y, "r": rng.randint(6, 9)})

out = {
    "meta": {"name": "NSUT Campus (schematic)", "width": W, "height": H, "meters_per_unit": METERS_PER_UNIT,
             "note": "Redrawn from the NSUT campus map. Edge weight = Euclidean length x factor (factor >= 1), so the Euclidean heuristic is admissible and consistent. Distances are approximate."},
    "nodes": nodes, "edges": edges, "locations": locations, "buildings": buildings, "green_spaces": green, "trees": trees,
}
Path(__file__).with_name("campus_map.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(len(nodes), "nodes", len(edges), "edges", len(locations), "locations", len(buildings), "buildings")
