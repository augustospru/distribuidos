import asyncio
from websockets.sync.client import connect
import time
import random

async def hello():
    while True:
        with connect("ws://localhost:8765") as websocket:
            num = str(random.randrange(20))
            websocket.send("1/" + num)
            message = websocket.recv()
            print(f"Received: {message}")
            time.sleep(3)

asyncio.run(hello())