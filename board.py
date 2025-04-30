import time

class Board:
    def __init__(self, grid, starting_position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.grid = grid
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        self.fen = starting_position
        self.start = time.time()
        self.__board_from_fen()

    def __board_from_fen(self):
        rows = self.fen.split(" ")[0].split("/")
        for row_idx, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    col_idx += int(char)
                else:
                    self.board[row_idx][col_idx] = char
                    col_idx += 1

    def move(self, lift: tuple[int, int], drop: tuple[int, int]):
        if self.board[lift[1]][lift[0]] == " ":
            print("No piece at lift")
        else:
            self.board[drop[1]][drop[0]] = self.board[lift[1]][lift[0]]
            self.board[lift[1]][lift[0]] = " "

    def __str__(self):
        result = ""
        for row in self.board:
            result += " ".join(str(cell) for cell in row) + "\n"

        return result 
        