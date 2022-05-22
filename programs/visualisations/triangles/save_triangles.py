# Pyramide
A = [1, 1, 1]
B = [6, 1, 1]
E = [1, 6, 1]
D = [6, 6, 1]
C = [3, 3, 5.5]
polygon = [
    [A, B, C],
    [A, C, E],
    [A, E, D],
    [A, D, B],
    [B, D, C],
    [E, D, C]
]

# Pyramide um 0 Punkt
A = [-1, -1, -1]
B = [1, -1, -1]
C = [1, -1, 1]
D = [-1, -1, 1]
E = [0, 1, 0]
polygon = [
    [A, B, C],
    [A, C, D],
    [A, B, E],
    [B, C, E],
    [C, D, E],
    [D, A, E],
]


# Pyramide um 0 Punkt
points = [
    ('A', [-1, -1, -1]),
    ('B', [1, -1, -1]),
    ('C', [1, -1, 1]),
    ('D', [-1, -1, 1]),
    ('E', [0, 1, 0]),
]
polygon = [
    ['A', 'B', 'C'],
    ['A', 'C', 'D'],
    ['A', 'B', 'E'],
    ['B', 'C', 'E'],
    ['C', 'D', 'E'],
    ['D', 'A', 'E'],
]


# Memory:
# [amount points, size per point, ...points..., amount triangles, ...triangles...]
out_a = []
for name, point in points:
    out_a.append(point)

out_b = []
for triangle in polygon:
    pointers = []
    for p_name in triangle:
        for i, tpl in enumerate(points):
            name, _ = tpl
            if name == p_name:
                pointers.append(i)
    out_b.append(pointers)


print("set cell cell1")
print(f"write {len(out_a)} cell 0")
i = 1
for pp in out_a:
    for p in pp:
        print(f"write {p} cell {i}")
        i += 1
print(f"write {len(out_b)} cell {i}")
i += 1
for pp in out_b:
    for p in pp:
        print(f"write {p} cell {i}")
        i += 1
