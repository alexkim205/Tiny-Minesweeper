from collections import defaultdict
import sys
import string


def printE(*args, **kwargs):
  print(*args, **kwargs, file=sys.stderr)


class Cell:

  def __init__(self, value, r, c, isBomb=False):
    self.r = r
    self.c = c
    self.isBomb = isBomb
    self.isExposed = False
    self.isFlagged = False
    self.value = value
    self.neighbors = defaultdict(None)

  def __repr__(self):
    return "Cell({})".format(self.value)

  def __str__(self, exposed=False):

    if exposed or self.isExposed:
      return str(self.value)
    elif self.isFlagged:
      return "F"
    else:
      return "X"

  def uncover(self):
    if self.isExposed:
      printE("You already uncovered this cell.")
    # Assume checking happens in grid class
    self.isExposed = True

  def toggle_flag(self):
    self.isFlagged = not self.isFlagged

  def is_correct(self):
    # correct if exposed and not bomb or if not exposed and bomb
    return not self.isBomb and self.isExposed or self.isBomb and not self.isExposed


class Grid:

  def __init__(self, grid):

    self.grid = grid
    self.width = len(grid[0])
    self.height = len(grid)

    def populate(k_r, k_c, cell):
      isBomb = False
      if cell == '*':
        isBomb = True

      tempCell = Cell(cell, k_r, k_c, isBomb)

      self.grid[k_r][k_c] = tempCell

    def findneighbors(k_r, k_c, cell):
      # top
      if k_r > 0:
        self.grid[k_r][k_c].neighbors['top'] = self.grid[k_r - 1][k_c]
      # right
      if k_c < self.width - 1:
        self.grid[k_r][k_c].neighbors['right'] = self.grid[k_r][k_c + 1]
      # bottom
      if k_r < self.height - 1:
        self.grid[k_r][k_c].neighbors['bottom'] = self.grid[k_r + 1][k_c]
      # left
      if k_c > 0:
        self.grid[k_r][k_c].neighbors['left'] = self.grid[k_r][k_c - 1]

    self.traverse(populate)
    self.traverse(findneighbors)

  def __repr__(self):
    return "Grid(w={w}, h={h})".format(w=self.width, h=self.height)

  def __str__(self):
    # Add col numbers
    string = ["   {col:}\n".format(col='  '.join(map(str, range(self.width))))]

    def stringify(k_r, k_c, cell, data):
      # Add row numbers
      if k_c == 0:
        data.append(str(k_r) + ' ')

      data.append(" {} ".format(str(cell)))

      if k_c == self.width - 1:
        data.append("\n")

    self.traverse(stringify, string)

    return ''.join(string)

  def traverse(self, callback, data=None):
    for k_r, r in enumerate(grid):
      for k_c, cell in enumerate(r):
        if data is not None:
          callback(k_r, k_c, cell, data)
        else:
          callback(k_r, k_c, cell)

  def uncover_cell(self, r, c):
    cell = self.grid[r][c]

    if cell.isFlagged:
      printE("You cannot uncover a flagged cell.")
    elif cell.isExposed:
      printE("You already uncovered this cell.")
    elif cell.isBomb:
      printE("You uncovered a bomb.")
      return False
    elif cell.value == 0:
      # Perform DFS visiting all blank cells
      self.bftraverse(cell)
    else:
      # cell is a number
      print("Cell uncovered at r:{} c:{}.".format(r, c))
      cell.uncover()

  def toggle_flag_cell(self, r, c):
    cell = self.grid[r][c]

    if cell.isExposed:
      printE("You cannot flag an uncovered cell.")
    else:
      print("Flag toggled at r:{} c:{}.".format(r, c))
      cell.toggle_flag()

  # Breadth-First Traverse
  def bftraverse(self, node):
    visited = set()
    queue = [node]

    while queue:
      node = queue.pop()
      # Expose this node
      node.uncover()
      # Add to visited
      visited.add(node)

      # If cell value is not 0, then don't add children to node neighbors
      if node.value == 0:
        for child in node.neighbors.values():
          if child not in visited and child not in queue:
            queue.append(child)


class Game:

  def __init__(self, grid):
    self.playGrid = Grid(grid)
    self.help = \
"""To toggle flagging a cell, type `f(r,c)`.
To uncover a cell, type `u(r,c)`.
> """

  def __str__(self):
    return str(self.playGrid)

  def play(self):
    wonGame = True
    while (not self.won_game()):
      print("")
      print(self)
      function = input(self.help)
      try:
        f, r, c = self.error_checking(function)
      except Exception as e:
        printE(e)
        continue

      # Flag
      if f == 'f':
        self.playGrid.toggle_flag_cell(r, c)
      elif f == 'u':
        checkLose = self.playGrid.uncover_cell(r, c)
        if checkLose is False:
          wonGame = False
          break

    print("You won the game!" if wonGame else "Game over!")
    print(self)

  def error_checking(self, function):
    try:
      parsed = function.translate(
          str.maketrans({key: None for key in string.punctuation}))
      parsed_func = parsed[0]

    except:
      raise Exception("Wrong format. Try again.")

    if parsed_func not in 'fu':
      raise Exception("Incorrect action. Try again.")

    try:
      r = int(parsed[1])
      c = int(parsed[2])
      return (parsed_func, r, c)
    except:
      raise Exception("Incorrect indices. Try again.")

  def won_game(self):

    def check_correctness(k_r, k_c, cell, data):
      data.append(cell.is_correct())

    booleans = []
    self.playGrid.traverse(check_correctness, booleans)
    return all(booleans)


if __name__ == "__main__":
  from minefield import grid
  game = Game(grid)
  game.play()
