#!/usr/bin/env python3
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the server
from networking.server import ChessServer
import asyncio

if __name__ == "__main__":
    server = ChessServer()
    asyncio.run(server.start())
