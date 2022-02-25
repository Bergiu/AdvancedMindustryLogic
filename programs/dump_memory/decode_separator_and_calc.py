from decode_memory_dump import decode_memory_dumps
import sys

inp = open(sys.argv[1]).read().split("\n")

inputs = []
cur = None
for line in inp:
    if cur is None:
        cur = line
    else:
        inputs.append((cur, line))
        cur = None

counts = {0: 0, 1: 0, 2: 0, 3: 0}
counts_items = {0: "lead", 1: "titanium", 2: "copper", 3: "graphite"}
decoded_list = []
for inp1, inp2 in inputs:
    example_data = decode_memory_dumps([inp1, inp2])

    decoded = []

    for x in example_data:
        filt = 2**52 - 4
        timestamp = x & filt
        timestamp = timestamp >> 2
        itemtype = x & 0b11
        decoded.append((itemtype, timestamp))

    decoded_list.append(decoded)

    counted = []
    for itemtype, timestamp in decoded:
        if itemtype in counts:
            counts[itemtype] += 1
        else:
            counts[itemtype] = 1
        counted.append((timestamp, counts[itemtype], itemtype))


# out_lines = [""] * len(decoded_list[0])
# headers = ""
# for j, decoded_l in enumerate(decoded_list):
#     headers += f"M{j}-Type;M{j}-Timestamp;"
#     for i, data in enumerate(decoded_l):
#         out_lines[i] += f"{data[0]};{data[1]};"

# print(headers)
# print("\n".join(out_lines))


print(counts)


summ = sum([y for y in counts.values()])
for x, y in counts.items():
    print("Propability of {}: {}".format(counts_items[x], y / summ))


print("Calculated Propabilities (x/12) from qmel")
print("Propability of lead:", 3/12)
print("Propability of titanium:", 2/12)
print("Propability of copper:", 5/12)
print("Propability of graphite:", 2/12)
