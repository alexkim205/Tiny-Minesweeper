# A mini ASCII minesweeper game

## What?

A quick and dirty implementation of a text based minesweeper game that you can play in your terminal.

## Why?

To practice object oriented programming.

## How?

To play this game, run the `minesweeper.py` file with Python 3. It will load the hardcoded minefield from `minefield.py`. Feel free to paste your own fields in.

```
python minesweeper.py
```

### Flagging and Uncovering a cell

When prompted, type `u(r,c)` to uncover the cell at row `r` and column `c`. Type `f(r,c)` to toggle the flag on the cell.

```
$ python minesweeper.py

To toggle flagging a cell, type `f(r,c)`.
To uncover a cell, type `u(r,c)`.
> u(0,0)

   0  1  2  3  4  5  6
0  0  1  X  X  X  X  X
1  0  1  X  X  X  X  X
2  0  2  X  X  X  X  X
3  0  1  X  X  X  X  X
4  0  1  1  X  X  X  X
5  0  0  0  1  X  X  X
6  0  0  0  1  X  X  X

To toggle flagging a cell, type `f(r,c)`.
To uncover a cell, type `u(r,c)`.
> f(1,2)
Flag toggled at r:1 c:2.

   0  1  2  3  4  5  6
0  0  1  X  X  X  X  X
1  0  1  F  X  X  X  X
2  0  2  X  X  X  X  X
3  0  1  X  X  X  X  X
4  0  1  1  X  X  X  X
5  0  0  0  1  X  X  X
6  0  0  0  1  X  X  X
```

Flags = `F`
Unexposed = `X`
Exposed = `(int)`

## More information

Tested on Python 3.6.6. Only standard libraries were used.
