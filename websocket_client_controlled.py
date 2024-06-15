import asyncio
from websockets.sync.client import connect
import time
import random
from classes import Client

async def main():
    conn = Client(None, None)
    with connect("ws://localhost:8765") as websocket:
        if not conn.id:
            websocket.send("C")
            message = websocket.recv()
            conn.id = message[0]
            conn.perfil = message[1]

        while True:
            id = str(conn.id)
            msg = input(id + ":Enter message: ")
            websocket.send(id + msg)
            message = websocket.recv()
            print(f"Received: {message}")

asyncio.run(main())