# Advanced Mindustry Logic

## TODO:
- HEX numbers
- BUG: `a = -0.5`: negative floating points don't work
    - this may be a bug of mindustry


## Additions
- function: defines a function
    - scoped / overwrite parameters
- exec: executes a function
- structs
- interfaces
- easy operations:
  - `op add x 1 2`: `x = 1 + 2`
  - `op sub x 1 2`: `x = 1 - 2`
  - `op mul x 1 2`: `x = 1 * 2`
  - `op div x 1 2`: `x = 1 / 2`
  - `op equal x 1 2`: `x = 1 == 2`
  - `op cos x a 0`: `x = cos(a)`
    - max, min, angle, len, noise, abs, log, log10, sin, cos, tan, floor, ceil, sqrt, rand
- easy set:
  - `set x 1`: `x = 1`
- while
- if, if/else
- standard library with reusable code

### Function
```
function add(a, b) {
    out = a + b
}
exec add(8, 4)
print out
```

Has no return value, but variables are public. So if you need the out value just use it.

#### Function Scopes

```
function add(a, b) {
    c = a
    a = b
    b = c
}
x = 8
y = 4
exec add(x, y)
```

Doesn't work. Parameters in a function will not overwrite the original variable.

```
function add(*a, *b) {
    c = a
    a = b
    b = c
}
x = 8
y = 4
exec add(x, y)
```

If you put a `*` infront of the variable name the method will overwrite the global value.

### Structs

```
struct Vec3D(x, y, z)
new A = Vec3D(10, 20, 50)
o = A.x + A.y + A.z
print o
```


### Passing structs to functions

```
struct Vec2D(x, y)
function move(Vec2D *Point, Vec2D dir) {
    Point.x += dir.x
    Point.y += dir.y
}
new A = Vec2D(1, 2)
new B = Vec2D(3, 4)
exec move(A, B)
print A.x
```

This example shows how to use structs in functions. Point is an inplace parameter and chances the outside object.


### Interfaces
```
struct Interface(hello)
function Interface::hello(string) {
    noop
}

function Single::hello(string) {
    print "Single "
    print string
    print "\n"
}
new Single = Interface(Single::hello)

function Double::hello(string) {
    print "Double "
    print string
    print string
    print "\n"
}
new Double = Interface(Double::hello)


function use_interface(Interface interface) {
    exec_ptr interface.hello("ABC")
}

exec use_interface(Single)
exec use_interface(Double)
printflush message1
```

To make in interface you need to add the function names of the interface as attributes to a struct. Then add the functions without content (no operation). The struct name must be the prefix of the function name (`StructName::FunctionName`).

To implement the interface you need to implement each function and prefix it with the name of the implementation struct. In this example it's `Single` and `Double`. After implementing the functions create an object of the interface and pass the function names as attributes. This will save the pointer to the function in the object.

Now you can create another function that takes an interface as parameter. To execute the function of the passed object you need to use `exec_ptr` instead of `exec`. This will resolve the variable to the given interface type to check the function parameters.

## Tips:

### Execute function pointers
Sometimes it can be practical to execute a function that is variable. For example you write a generic plot function that can plot the results of another function. In this case you want to inject the calculate-function into the plot-function:

```
function plot(f, from, to) {
    x = from
    while x < to {
        # This does not work, because f is not defined
        exec f(x)
        print y
        print "\n"
    }
}

function f1(x) {
    y = 2*x
}

exec plot(f1)
```

To solve this issue you can call the function manually without exec. To do this you first need to set the parameters manually, then set the return pointer and then set `@counter` to the function pointer:

```
function plot(f, from, to) {
    i = from
    while i < to {
        # This works
        # set params
        x = i
        # manually set return pointer
        op add retptr @counter 1
        # execute f
        set @counter f
        print y
        print "\n"
    }
}

function f1(x) {
    y = 2*x
}

exec plot(f1)
```

### Exit functions
A return keyword is not implemented and sometimes you want to exit a method directly. To do this just set a label to the end of the method with a noop and jump to it:

```
function example(x) {
    if x > 100 {
        jump exit always 0 0
    }
    # do stuff
    ...
    exit:
    noop
}
```

### Behaviour of -
1. `-` can be used as sign (`8*-5`) and it can be used as arithmetic operation (`8-5`).
2. `-` cannot be used in normal variable names (`surge-alloy`), but it can be used in special variable names that start with `@` (`@surge-alloy`)
3. You don't need spaces between operations (`delta=now-then`)

This leads to a special behaviour if you use `@` variables in combination with arithmetics. For example `x = @time-delta`. The compiler can distinguish if you mean "`x` is `delta` subtracted from `@time`" or "`x` is `@time-delta`". The current behaviour is that there is no subtraction and the `@time-delta` is used as a variable name. So if you want to subtract something from a `@` variable you need to insert spaces: `x = @time - delta`.

### Notes
Numbers have 64 bit.
Cells have float.
Maximum length of a variable name is 36 chars.

## How to use

Install python and the dependencies.

Then run `./main.py your_code.amnd | xclip -selection c` or `./main.py your_code.amnd`.

# NeoVim

You can use this program as linter for neovim ale.

Copy the file `vim/ale_linters/amnd.vim` to `~/.config/nvim/ftdetect/amnd.vim`.

Copy the file `vim/ftdetect/amnd.vim` to `~/.config/nvim/ftdetect/amnd.vim`.

Copy `vim/syntax/amnd.vim` to `~/.config/nvim/syntax/amnd.vim`.

This file is inspired by: https://github.com/purofle/vim-mindustry-logic
