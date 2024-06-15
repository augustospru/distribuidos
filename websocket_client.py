import asyncio
from websockets.sync.client import connect
import time
import random
from connection import Client

async def main():
    conn = Client(None, None)
    with connect("ws://localhost:8765") as websocket:
        if not conn.id:
            websocket.send("C")
            message = websocket.recv()
            conn.id = message[0]
            conn.perfil = message[1]

        while True:
            num = str(random.randrange(20))
            id = str(conn.id)
            websocket.send(id + "/" + num)
            message = websocket.recv()
            print(f"Received: {message}")
            time.sleep(3)

asyncio.run(main())