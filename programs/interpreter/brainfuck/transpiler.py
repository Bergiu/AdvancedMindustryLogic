import sys

if len(sys.argv) < 2:
    print("Missing filename:")
    print(f"python3 {sys.argv[0]} FILENAME.bf")
    sys.exit(1)

filename = sys.argv[1]
code = open(filename).read()

codepoints = []
for c in code:
    if c == "+":
        codepoints.append(43)
    if c == "-":
        codepoints.append(45)
    if c == "<":
        codepoints.append(60)
    if c == ">":
        codepoints.append(62)
    if c == "[":
        codepoints.append(91)
    if c == "]":
        codepoints.append(93)
    if c == ",":
        codepoints.append(44)
    if c == ".":
        codepoints.append(46)
    if c == ":":
        codepoints.append(58)


print("control enabled switch1 1 0 0 0")
print("set mem bank1")
for i, codepoint in enumerate(codepoints):
    print(f"write {codepoint} mem {i}")
# reset every other cell
for i in range(len(codepoints), 512):
    print(f"write 0 mem {i}")
print("control enabled switch1 0 0 0 0")
print("op sub @counter @counter 1")
