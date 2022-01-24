# Advanced Mindustry Logic

## Additions
- function: defines a function
- exec: executes a function
- easy operations:
  - `op add x 1 2`: `x = 1 + 2`
  - `op sub x 1 2`: `x = 1 - 2`
  - `op mul x 1 2`: `x = 1 * 2`
  - `op div x 1 2`: `x = 1 / 2`
  - `op equal x 1 2`: `x = 1 == 2`
- easy set:
  - `set x 1`: `x = 1`


# NeoVim

You can use this program as linter for neovim ale.

Copy the file `vim/ale_linters/amnd.vim` to `~/.config/nvim/ftdetect/amnd.vim`.

Copy the file `vim/ftdetect/amnd.vim` to `~/.config/nvim/ftdetect/amnd.vim`.

Copy `vim/syntax/amnd.vim` to `~/.config/nvim/syntax/amnd.vim`.

This file is inspired by: https://github.com/purofle/vim-mindustry-logic


# Notes
Numbers have 64 bit.
