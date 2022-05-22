# Pyramide um 0 Punkt
points = [
    ('A', [-1, -1, -1]),
    ('B', [1, -1, -1]),
    ('C', [1, -1, 1]),
    ('D', [-1, -1, 1]),
    ('E', [-1, -0.1, -1]),
    ('F', [1, -0.1, -1]),
    ('G', [1, -0.1, 1]),
    ('H', [-1, -0.1, 1]),
    ('I', [0, 1, 1]),
    ('J', [0, 1, -1]),
]
colors = [
    ('darkgray', [128, 128, 128, 128]),
    ('lightgray', [240, 240, 240, 128]),
    ('lightgray2', [220, 220, 220, 128]),
    ('lightgray3', [210, 210, 210, 128]),
    ('white', [255, 255, 255, 128]),
]
polygon = [
    # bottom
    ['A', 'B', 'C', 'darkgray'],
    ['A', 'C', 'D', 'darkgray'],
    # front
    ['A', 'B', 'E', 'lightgray'],
    ['F', 'B', 'E', 'lightgray'],
    # right
    ['B', 'C', 'F', 'white'],
    ['G', 'C', 'F', 'white'],
    # back
    ['D', 'C', 'G', 'lightgray'],
    ['H', 'D', 'G', 'lightgray'],
    # left
    ['H', 'D', 'A', 'white'],
    ['H', 'E', 'A', 'white'],
    # front roof
    ['E', 'F', 'J', 'lightgray'],
    # right root
    ['F', 'G', 'J', 'lightgray2'],
    ['I', 'G', 'J', 'lightgray2'],
    # back root
    ['H', 'G', 'I', 'lightgray'],
    # left root
    ['E', 'H', 'J', 'lightgray3'],
    ['I', 'H', 'J', 'lightgray3'],
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


print("set cell bank1")
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
