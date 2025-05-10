import chess
import copy
import queue
from engine.opening import get_opening

# Global queue for board updates
board_update_queue = queue.Queue()

# GRID ORIENTATION
# [0][0]         [0][7]
# r n b k q b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B K Q B N R
# [7][0]         [7][7]

# [rank][file]
# [y][x]

# a8 = [0][0]
# h8 = [0][7]
# a1 = [7][0]
# h1 = [7][7]

class ChessBoard:
    def __init__(self, starting="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = chess.Board(starting)
        self.movelist = []
        self.last_grid = [["W" if r >= 6 else "B" if r <= 1 else None for _ in range(8)] for r in range(8)]
        self.pending_capture_square = None

    def queue_board_state(self):
        """Queue a board state update to be sent by the network thread"""
        state = {
            "fen": self.board.fen(),
            "movelist": self.movelist,
            "last_move": self.movelist[-1] if self.movelist else None,
            "is_game_over": self.board.is_game_over(),
            "opening": get_opening(self.movelist)
        }
        board_update_queue.put(state)

    # [0, 0] -> a8
    # [0, 7] -> h8
    # [7, 7] -> h1
    def __point_to_chess(self, point) -> str:
        return f"{chr(point[1]+65).lower()}{8-point[0]}"
    
    def update_state(self, grid) -> None:
        # Detect changes between the current grid and the last grid
        removed_piece = None
        added_piece = None
        removed_pos = None
        added_pos = None

        for r in range(8):
            for c in range(8):
                if self.last_grid[r][c] != grid[r][c]:
                    if self.last_grid[r][c] is not None and grid[r][c] is None:
                        # A piece was removed
                        removed_piece = self.last_grid[r][c]
                        removed_pos = (r, c)
                    elif self.last_grid[r][c] is None and grid[r][c] is not None:
                        # A piece was added
                        added_piece = grid[r][c]
                        added_pos = (r, c)

        # Ensure we detected a valid move
        if removed_piece and added_piece and removed_pos and added_pos:
            # Convert positions to chess notation
            from_square = self.__point_to_chess(removed_pos)
            to_square = self.__point_to_chess(added_pos)

            # Make the move on the chess board
            move = chess.Move.from_uci(f"{from_square}{to_square}")
            if move in self.board.legal_moves:
                self.movelist.append(self.board.san(move))
                print(get_opening(self.movelist))
                self.board.push(move)
                # Queue board state update after move
                self.queue_board_state()
            else:
                raise ValueError("Illegal move detected")

        # Update the last grid state
        self.last_grid = copy.deepcopy(grid)