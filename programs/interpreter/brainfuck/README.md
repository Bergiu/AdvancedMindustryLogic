# Brainfuck Interpreter

Save your brainfuck code into a file and execute: `./transpiler.py FILENAME | xclip -selection c`. This returns a code for mindustry that will save the brainfuck code into a memory bank.

In mindustry place down the schematic and insert the transpiled code into the micro processor. The switch next to it should get enabled then. Wait until it's disabled. Now your code is written into the memory bank.

Now press the start switch to start the brainfuck interpreter.

## Extended Mode

I've added a command `:` to this brainfuck implementation. This command will execute the `printflush` command. If you enable the extended mode, you need to manually flush the output after writing text with `.`. If you disable extended mode flush will be executed after every `.` output.
