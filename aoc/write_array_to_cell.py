import sys


def main():
    filename = sys.argv[1]

    print('print "Starting write..."')
    print("printflush message1")

    print("set cell bank1")

    lines = open(filename, "r").read().split("\n")
    amount = len(lines) - 1

    print(f"write {amount} cell 1")

    for i, line in enumerate(lines):
        if line == "":
            continue
        print(f"write {line} cell {i + 2}")

    print('print "Finished"')
    print('printflush message1')
    print('op sub @counter @counter 1')


if __name__ == '__main__':
    main()
