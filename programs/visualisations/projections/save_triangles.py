# Pyramide um 0 Punkt
points = [
    ('A', [-1, -1, -1]),
    ('B', [1, -1, -1]),
    ('C', [1, -1, 1]),
    ('D', [-1, -1, 1]),
    ('E', [0, 1, 0]),
]
colors = [
    ('darkgray', [128, 128, 128, 128]),
    ('lightgray', [240, 240, 240, 128]),
    ('white', [255, 255, 255, 128]),
]
polygon = [
    ['A', 'B', 'C', 'darkgray'],
    ['A', 'C', 'D', 'darkgray'],
    ['A', 'B', 'E', 'lightgray'],
    ['B', 'C', 'E', 'white'],
    ['C', 'D', 'E', 'lightgray'],
    ['D', 'A', 'E', 'white'],
]


# Memory:
# [amount points, size per point, ...points..., amount triangles, ...triangles...]
out_a = []
for name, point in points:
    out_a.append(point)

out_c = []
for name, point in colors:
    out_c.append(point)

out_b = []
for triangle in polygon:
    pointers = []
    for p_name in triangle[:3]:
        for i, tpl in enumerate(points):
            name, _ = tpl
            if name == p_name:
                pointers.append(i)
    for color in triangle[3:]:
        for i, tpl in enumerate(colors):
            name, _ = tpl
            if name == color:
                pointers.append(i)
    out_b.append(pointers)


print("set cell cell1")
# points
print(f"write {len(out_a)} cell 0")
i = 1
for pp in out_a:
    for p in pp:
        print(f"write {p} cell {i}")
        i += 1
# colors
print(f"write {len(out_c)} cell {i}")
i += 1
for pp in out_c:
    for p in pp:
        print(f"write {p} cell {i}")
        i += 1
# triangles
print(f"write {len(out_b)} cell {i}")
i += 1
for pp in out_b:
    for p in pp:
        print(f"write {p} cell {i}")
        i += 1
