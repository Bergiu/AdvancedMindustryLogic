# Memory
Memory is a struct that contains the link to the memory cell and its size.

# Memory Mappers
A memory mapper is used to allocate and free space on the memory cell. Other datastructures can for example request 10 cells of space and the memory mapper allocates this space.

There are multiple memory mappers with different benefits:
- Stupid Mapper
    - Works
    - Just returns the next free block
    - Can't be freed
- Heap Mapper
    - WIP
    - Divides the memory into a heap and a stack
    - Saves metadata about the allocated regions in the stack
    - Can use freed space
    - No defragmentation
- Bit Heap Mapper
    - WIP
    - Uses a stack size and saves the allocated regions in a bitmap
    - Can use freed space
    - No defragmentation
- Pointer Mapper
    - WIP
    - Returns the position of a pointer instead of the real block
    - This enables defragmentation of the memory

# Vector
Vector is an example of how the memory mappers can be used.
