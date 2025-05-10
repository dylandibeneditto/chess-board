#!/usr/bin/env python3
import os
import sys
import asyncio

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the emulator
from emulator import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running emulator: {e}")
