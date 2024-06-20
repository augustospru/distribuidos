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
            conn.add_message(id + msg)
            message = websocket.recv()
            print(f"Received: {message}")
            
            #ressend message if nack
            message_aux = message.split("/?")
            send_message_list: list[str] = []
            nack_received: list[str] = []
            for msg in message_aux:
                if f"N{id}" in msg[1:3]:
                    nack_received.append(msg)

            if nack_received: 
                send_message_list = conn.message_send

                message_list: list[str] = []
                for msg in send_message_list:
                    if "G" in msg[1]:
                        message_list = message_list + msg[3:].split("/?")

                for nack in nack_received:
                    id_message_list = nack[3:]
                    messages_ressend: list[str] = []
                    for msg in message_list:
                        if msg[0] in id_message_list: messages_ressend.append(msg)

                    message_final = f"M{nack[0]}" + "/?".join(messages_ressend)

                    websocket.send(id + message_final)
                    conn.add_message(id + message_final)
                    message = websocket.recv()
                    print(f"Received: {message}")
                    



asyncio.run(main())