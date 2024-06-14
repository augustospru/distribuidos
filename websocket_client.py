import asyncio
from websockets.sync.client import connect

async def hello():
    while True:
        with connect("ws://localhost:8765") as websocket:
            # websocket.send("Hello world!")
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(hello())