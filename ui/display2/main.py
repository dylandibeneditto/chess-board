import tkinter as tk
from tkinter import ttk
import asyncio
import json
from networking.client import ChessClient

class Display2UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Display 2")
        self.root.geometry("800x600")
        
        # Initialize client
        self.client = ChessClient(client_id="display2")
        self.setup_handlers()
        
        # Create UI elements
        self.setup_ui()

    def setup_ui(self):
        # Status frame
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, text="Game Status: Active")
        self.status_label.pack(side='left')
        
        # Move history frame
        self.history_frame = ttk.Frame(self.root)
        self.history_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.history_label = ttk.Label(self.history_frame, text="Move History")
        self.history_label.pack()
        
        self.history_text = tk.Text(self.history_frame, height=20, width=40)
        self.history_text.pack(expand=True, fill='both')
        
        # Sensor data frame
        self.sensor_frame = ttk.Frame(self.root)
        self.sensor_frame.pack(fill='x', padx=10, pady=5)
        
        self.sensor_label = ttk.Label(self.sensor_frame, text="Sensor Status: OK")
        self.sensor_label.pack()

    def setup_handlers(self):
        @self.client.on_message("board_update")
        async def handle_board_update(content):
            print("Display2: Received board_update message")  # Debug print
            # Update UI with new board state
            self.root.after(0, self.update_display, content)
            
        @self.client.on_message("sensor_data")
        async def handle_sensor_data(content):
            print("Display2: Received sensor_data message")  # Debug print
            # Update sensor status
            self.root.after(0, self.update_sensor_status, content)

    def update_display(self, state):
        print("Display2: Received state update:", state)  # Debug print
        
        # Update game status
        is_game_over = state.get("is_game_over", False)
        self.status_label.config(text=f"Game Status: {'Game Over' if is_game_over else 'Active'}")
        print(f"Display2: Updated game status: {'Game Over' if is_game_over else 'Active'}")  # Debug print
        
        # Update move history
        movelist = state.get("movelist", [])
        print(f"Display2: Updating move history with {len(movelist)} moves")  # Debug print
        self.history_text.delete(1.0, tk.END)
        for i, move in enumerate(movelist, 1):
            if i % 2 == 1:
                self.history_text.insert(tk.END, f"{(i+1)//2}. {move} ")
            else:
                self.history_text.insert(tk.END, f"{move}\n")

    def update_sensor_status(self, sensor_data):
        self.sensor_label.config(text=f"Sensor Status: {sensor_data.get('status', 'Unknown')}")

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
    app = Display2UI(root)
    
    # Run both the Tkinter event loop and asyncio event loop
    asyncio.run(app.run())

if __name__ == "__main__":
    main()
