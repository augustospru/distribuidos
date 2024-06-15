import asyncio
from websockets.sync.client import connect
import sys
from classes import Client

async def main():
    conn = Client(None, None)
    with connect("ws://localhost:8765") as websocket:
        args = sys.argv[1:]
        id_group = ""
        if args and args[0] == '-g': 
            id_group = args[1]
            
        if not conn.id:
            websocket.send("C" + id_group)
            message = websocket.recv()
            conn.id = message[0]
            conn.perfil = message[1]
            conn.group = message[2]

        while True:
            id = conn.id
            group = conn.group
            msg = input(id + group + ":Enter message: ")
            websocket.send(id + msg)
            message = websocket.recv()
            print(f"Received: {message}")

asyncio.run(main())