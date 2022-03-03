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

# Memory:
# [amount points, size per point, ...points..., amount triangles, ...triangles...]
out_a = []
out_a.append(A)
out_a.append(B)
out_a.append(C)
out_a.append(D)
out_a.append(E)

out_b = []
for triangle in polygon:
    pointers = []
    for point in triangle:
        if point == A:
            pointers.append(0)
        if point == B:
            pointers.append(1)
        if point == C:
            pointers.append(2)
        if point == D:
            pointers.append(3)
        if point == E:
            pointers.append(4)
    out_b.append(pointers)


print("set cell cell1")
print("write 5 cell 0")
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
