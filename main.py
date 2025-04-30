from grid import Grid
from board import Board

# 8x8 grid of booleans
sensors = [[r < 2 or r > 5 for _ in range(8)] for r in range(8)]
grid = Grid(grid=sensors)
board = Board(grid=grid)
board.move([3, 1], [3, 3])
print(board)