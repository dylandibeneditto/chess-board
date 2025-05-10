import pygame
import sys
import asyncio
import json
import threading
import queue
from board import ChessBoard, board_update_queue
from networking.client import ChessClient
from engine.opening import get_opening

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIECE_COLOR = (200, 0, 0)

class ChessEmulator:
    def __init__(self):
        self.board = [["W" if r >= 6 else "B" if r <= 1 else None for _ in range(COLS)] for r in range(ROWS)]
        self.selected_piece = None
        self.chess_board = ChessBoard()
        self.client = ChessClient(client_id="emulator")
        
        # Initialize pygame
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Board Emulator")
        self.clock = pygame.time.Clock()

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.board[row][col]:
                    piece_color = (100, 100, 100) if self.board[row][col] == "W" else (50, 50, 50)
                    pygame.draw.circle(self.win, piece_color, 
                                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                    SQUARE_SIZE // 3)

    def get_square_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    async def send_board_update(self):
        state = {
            "board": self.board,
            "fen": self.chess_board.board.fen(),
            "movelist": self.chess_board.movelist,
            "last_move": self.chess_board.movelist[-1] if self.chess_board.movelist else None,
            "is_game_over": self.chess_board.board.is_game_over()
        }
        await self.client.send_message("board_update", state)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = self.get_square_from_mouse(pygame.mouse.get_pos())
                if self.selected_piece is None and self.board[row][col]:
                    self.selected_piece = (row, col)
                    print(f"Selected piece at {row}, {col}")  # Debug print
                elif self.selected_piece and (row, col) != self.selected_piece:
                    print(f"Moving piece from {self.selected_piece} to {row}, {col}")  # Debug print
                    # Move the piece
                    self.board[row][col] = self.board[self.selected_piece[0]][self.selected_piece[1]]
                    self.board[self.selected_piece[0]][self.selected_piece[1]] = None
                    self.selected_piece = None
                    
                    # Update chess board and directly queue an update
                    try:
                        self.chess_board.update_state(self.board)
                        # Queue a direct update with the current board state
                        state = {
                            "board": self.board,
                            "fen": self.chess_board.board.fen(),
                            "movelist": self.chess_board.movelist,
                            "last_move": self.chess_board.movelist[-1] if self.chess_board.movelist else None,
                            "is_game_over": self.chess_board.board.is_game_over(),
                            "opening": get_opening(self.chess_board.movelist)
                        }
                        board_update_queue.put(state)
                        print("Queued board update:", state)  # Debug print
                    except ValueError as e:
                        print(f"Invalid move: {e}")
                        # Revert the move if it's invalid
                        self.board = [[piece for piece in row] for row in self.chess_board.last_grid]
        
        return True

    async def network_loop(self):
        """Network communication loop"""
        print("Starting network loop...")  # Debug print
        try:
            # Start the connection
            connect_task = asyncio.create_task(self.client.connect())
            
            # Start the message sending loop
            while True:
                try:
                    # Check for updates to send from the board
                    if not board_update_queue.empty():
                        state = board_update_queue.get_nowait()
                        # Add the current board state to the update
                        state["board"] = self.board
                        print(f"Network: Sending board update")  # Debug print
                        await self.client.send_message("board_update", state)
                except queue.Empty:
                    pass
                except Exception as e:
                    print(f"Error sending message: {e}")  # Debug print
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Network loop error: {e}")  # Debug print

    def run_network(self):
        """Run the network loop in a separate thread"""
        asyncio.run(self.network_loop())

    def run(self):
        """Main game loop"""
        # Start network thread
        network_thread = threading.Thread(target=self.run_network, daemon=True)
        network_thread.start()
        
        running = True
        while running:
            self.clock.tick(60)
            running = self.process_events()
            
            self.draw_board()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

def main():
    emulator = ChessEmulator()
    emulator.run()


if __name__ == "__main__":
    main()