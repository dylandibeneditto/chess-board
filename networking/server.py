import asyncio
import json
import websockets

class ChessServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.board_state = None
        self.sensor_data = None

    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")

    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")

    async def broadcast(self, message, sender=None):
        if self.clients:
            print(f"Broadcasting message type: {message['type']} to {len(self.clients)} clients")  # Debug print
            for client in self.clients:
                if client != sender:  # Don't send back to the sender
                    try:
                        print(f"Sending message to client")  # Debug print
                        msg_str = json.dumps(message)
                        await client.send(msg_str)
                        print(f"Successfully sent message to client")  # Debug print
                    except Exception as e:
                        print(f"Error sending to client: {e}")  # Debug print
                        # Remove failed client
                        self.clients.remove(client)

    async def handle_message(self, websocket, message):
        data = json.loads(message)
        message_type = data.get("type")
        content = data.get("content")
        client_id = data.get("client_id")
        print(f"Received {message_type} from {client_id}")  # Debug print

        if message_type == "board_update":
            self.board_state = content
            # Broadcast the board update to all clients except sender
            await self.broadcast({"type": "board_update", "content": content}, websocket)
        elif message_type == "sensor_data":
            self.sensor_data = content
            await self.broadcast({"type": "sensor_data", "content": content}, websocket)

    async def handler(self, websocket):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        finally:
            await self.unregister(websocket)

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"Server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = ChessServer()
    asyncio.run(server.start())
