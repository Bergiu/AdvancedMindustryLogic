# How to
1. Create folder for every day
2. Copy your puzzle input into a file
3. **Verify** that the input only has **< 511 lines**
4. Execute `python3 aoc/write_array_to_cell.py input_filename|xclip -selection c`
5. Open Mindustry and create one "[L] AOC" schematic
6. Paste the code into the small processor
7. When the message block above the processor displays "Finished" the file is written into the memory bank

Index 1: LEN, length of the file
Index 2-LEN: contains the file


# Notices
memory_cell = 64  # slots
memory_bank = 512 # slots

Micro Processor = 120/sec
Logic Processor = 480/sec
Hyper Processor = 1500/sec
