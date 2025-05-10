import tkinter as tk
from tkinter import ttk
import asyncio
import json
from networking.client import ChessClient

class Display1UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Display 1")
        self.root.geometry("800x600")
        
        # Initialize client
        self.client = ChessClient(client_id="display1")
        self.setup_handlers()
        
        # Create UI elements
        self.setup_ui()

    def setup_ui(self):
        # Main board frame
        self.board_frame = ttk.Frame(self.root)
        self.board_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create 8x8 grid of labels for chess board
        self.squares = []
        for row in range(8):
            row_squares = []
            for col in range(8):
                square = ttk.Label(
                    self.board_frame,
                    text='',
                    background='white' if (row + col) % 2 == 0 else 'gray',
                    borderwidth=1,
                    relief='solid'
                )
                square.grid(row=row, column=col, sticky='nsew')
                row_squares.append(square)
            self.squares.append(row_squares)
            
        # Make grid cells expand equally
        for i in range(8):
            self.board_frame.grid_columnconfigure(i, weight=1)
            self.board_frame.grid_rowconfigure(i, weight=1)
            
        # Info frame
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(fill='x', padx=10, pady=5)
        
        self.opening_label = ttk.Label(self.info_frame, text="Opening: Unknown")
        self.opening_label.pack(side='left')
        
        self.last_move_label = ttk.Label(self.info_frame, text="Last Move: None")
        self.last_move_label.pack(side='right')

    def setup_handlers(self):
        @self.client.on_message("board_update")
        async def handle_board_update(content):
            print("Display1: Received board_update message")  # Debug print
            # Update UI with new board state
            self.root.after(0, self.update_display, content)

    def update_display(self, state):
        print("Display1: Received state update:", state)  # Debug print
        
        # Update opening info
        eco, name = state.get("opening", ("?", "Unknown Opening"))
        self.opening_label.config(text=f"Opening: {eco} - {name}")
        print(f"Display1: Updated opening to {eco} - {name}")  # Debug print
        
        # Update last move
        last_move = state.get("last_move", "None")
        self.last_move_label.config(text=f"Last Move: {last_move}")
        print(f"Display1: Updated last move to {last_move}")  # Debug print

        # Update board display
        board_state = state.get("board")
        if board_state:
            print("Display1: Updating board visualization")  # Debug print
            for row in range(8):
                for col in range(8):
                    piece = board_state[row][col]
                    label = self.squares[row][col]
                    if piece == "W":
                        label.configure(text="W", foreground="white", font=("Arial", 24))
                    elif piece == "B":
                        label.configure(text="B", foreground="black", font=("Arial", 24))
                    else:
                        label.configure(text="")

    async def start_network(self):
        await self.client.connect()

    async def run(self):
        """Run the UI and network connection concurrently"""
        network_task = asyncio.create_task(self.start_network())
        
        while True:
            self.root.update()
            await asyncio.sleep(0.01)
            
def main():
    root = tk.Tk()
    app = Display1UI(root)
    
    # Run both the Tkinter event loop and asyncio event loop
    asyncio.run(app.run())

if __name__ == "__main__":
    main()
