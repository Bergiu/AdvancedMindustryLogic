# Advanced Mindustry Logic

## TODO:
- HEX numbers


## Additions
- function: defines a function
    - scoped / overwrite parameters
- exec: executes a function
- easy operations:
  - `op add x 1 2`: `x = 1 + 2`
  - `op sub x 1 2`: `x = 1 - 2`
  - `op mul x 1 2`: `x = 1 * 2`
  - `op div x 1 2`: `x = 1 / 2`
  - `op equal x 1 2`: `x = 1 == 2`
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

#### Scopes

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
