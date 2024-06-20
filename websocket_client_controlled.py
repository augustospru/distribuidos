import asyncio
from websockets.sync.client import connect
import sys
from classes import Client
from client_func import nack_received

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
            id_client = conn.id
            group = conn.group
            msg = input(id_client + group + ":Enter message: ")
            websocket.send(id_client + msg)
            conn.add_message(id_client + msg)
            message = websocket.recv()
            print(f"Received: {message}")
            
            #ressend message if nack
            message_aux = message.split("/?")
            nack_recv: list[str] = []
            for msg in message_aux:
                if f"N{id_client}" in msg[1:3]:
                    nack_recv.append(msg)

            if nack_recv: await nack_received(conn, websocket, nack_recv, id_client)

asyncio.run(main())