import asyncio
from client import ChessClient

class Display2:
    def __init__(self):
        self.client = ChessClient(client_id="display2")
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on_message("board_update")
        async def handle_board_update(content):
            print(f"Display 2 received board update: {content}")
            # Handle the board update in your UI

        @self.client.on_message("sensor_data")
        async def handle_sensor_data(content):
            print(f"Display 2 received sensor data: {content}")
            # Handle the sensor data in your UI

    async def send_sensor_data(self, sensor_data):
        await self.client.send_message("sensor_data", sensor_data)

if __name__ == "__main__":
    display = Display2()
    display.client.start()
