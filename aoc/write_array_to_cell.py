#! /bin/python3
import sys


# aoc/write_array_to_cell_pre_program.amnd
PRE_PROGRAM = '''set cell bank1
set message message2
set control_switch switch2
set finish_switch switch1
sensor sw_on control_switch @enabled
op notEqual var_8778676585855 sw_on true
op notEqual if_skip var_8778676585855 1
op mul if_skip if_skip 3
op add @counter @counter if_skip
print "Disabled"
printflush message
end
print "Starting write..."
printflush message
'''


def main():
    filename = sys.argv[1]
    print(PRE_PROGRAM)

    lines = open(filename, "r").read().split("\n")
    amount = len(lines) - 1

    print(f"write {amount} cell 1")

    for i, line in enumerate(lines):
        if line == "":
            continue
        print(f"write {line} cell {i + 2}")

    print('print "Finished"')
    print('printflush message')
    print('control enabled finish_switch 1 0 0 0')
    print('op sub @counter @counter 1')


if __name__ == '__main__':
    main()
