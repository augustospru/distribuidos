import asyncio
from websockets.sync.client import connect
import sys
from classes import Client
from client_func import nack_received, lider_received, send_assert, assert_received
import time

async def main():
    conn = Client(None, None)
    with connect("ws://localhost:8765") as websocket:
        args = sys.argv[1:]
        id_group = ""
        falty = False
        if args and args[0] == '-g': 
            id_group = args[1]

        if args and '-f' in args: 
            falty = True
            
        if not conn.id:
            websocket.send("C" + id_group)
            message = websocket.recv()
            conn.id = message[0]
            conn.perfil = message[1]
            conn.group = message[2]

        group_recv = {}
        while True:
            time.sleep(3)
            id_client = conn.id
            group = conn.group
            msg = "HP" #input("Id" + id_client + "Gp" + group + conn.perfil + ":Enter message: ")
            print("Id" + id_client + "Gp" + group + conn.perfil)
            websocket.send(id_client + msg)
            conn.add_message(id_client + msg)
            message = websocket.recv()
            print(f"Received: {message}")

            if message == "F" or message == "T": continue
            
            #functions when receiving
            message_aux = message.split("/?")
            nack_recv: list[str] = []
            lider_recv: list[str] = []
            assert_recv: list[str] = []
            received_here: bool = False
            for msg in message_aux:
                if f"N{id_client}" in msg[1:3]:
                    nack_recv.append(msg) # save all nack messages
                elif f"L{id_client}" in msg[1:3]:
                    lider_recv.append(msg) # save all lider messages
                elif f"G{group}" in msg[1:3]:
                    received_here = True
                    sender_group = msg[:3]
                    group_recv.setdefault(sender_group,[]).append(msg[3]) #save id_message
                elif f"A{group}" in msg[1:3]:
                    assert_recv.append(msg) #save id_message

            if nack_recv: await nack_received(conn, websocket, nack_recv, id_client)
            if lider_recv: await lider_received(conn, websocket, lider_recv, id_client)
            if received_here and group_recv: await send_assert(conn, websocket, group_recv, id_client) #send_assert()
            if group_recv and assert_recv: await assert_received(conn, websocket, assert_recv, group_recv, id_client, falty) #check messages and send_nack() or ok

asyncio.run(main())