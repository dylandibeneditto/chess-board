import asyncio
from client import ChessClient

class Display1:
    def __init__(self):
        self.client = ChessClient(client_id="display1")
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on_message("board_update")
        async def handle_board_update(content):
            print(f"Display 1 received board update: {content}")
            # Handle the board update in your UI

        @self.client.on_message("sensor_data")
        async def handle_sensor_data(content):
            print(f"Display 1 received sensor data: {content}")
            # Handle the sensor data in your UI

    async def send_board_update(self, board_state):
        await self.client.send_message("board_update", board_state)

if __name__ == "__main__":
    display = Display1()
    display.client.start()
