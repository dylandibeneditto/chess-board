class Grid:
    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        result = ""
        for row in self.grid:
            result += " ".join(str(int(cell)) for cell in row) + "\n"

        return result