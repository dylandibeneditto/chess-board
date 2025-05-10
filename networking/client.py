import asyncio
import json
import websockets

class ChessClient:
    def __init__(self, uri="ws://localhost:8765", client_id=None):
        self.uri = uri
        self.client_id = client_id
        self.websocket = None
        self.message_handlers = {}

    def on_message(self, message_type):
        def decorator(handler):
            self.message_handlers[message_type] = handler
            return handler
        return decorator

    async def send_message(self, message_type, content):
        if self.websocket:
            message = {
                "type": message_type,
                "content": content,
                "client_id": self.client_id
            }
            print(f"Sending message: {message_type} from {self.client_id}")  # Debug print
            await self.websocket.send(json.dumps(message))

    async def receive_handler(self):
        try:
            print(f"Started receive handler for {self.client_id}")  # Debug print
            async for message in self.websocket:
                data = json.loads(message)
                message_type = data.get("type")
                content = data.get("content")
                print(f"Received message: {message_type} for {self.client_id}")  # Debug print

                if message_type in self.message_handlers:
                    try:
                        await self.message_handlers[message_type](content)
                    except Exception as e:
                        print(f"Error handling message {message_type}: {e}")  # Debug print
                else:
                    print(f"Unhandled message type: {message_type}")
        except websockets.ConnectionClosed:
            print(f"Connection closed for {self.client_id}")  # Debug print
        except Exception as e:
            print(f"Error in receive handler: {e}")  # Debug print

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to server at {self.uri}")
            # Start receive handler as a separate task
            receive_task = asyncio.create_task(self.receive_handler())
            await receive_task
        except Exception as e:
            print(f"Connection error: {e}")

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
