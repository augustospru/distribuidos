from classes import Client
from websockets.sync.client import ClientConnection

async def nack_received(conn: Client, websocket: ClientConnection, nack_recv: list[str], id_client: str):
    send_message_list = conn.message_send

    message_list: list[str] = []
    for msg in send_message_list:
        if "G" in msg[1]:
            message_list = message_list + msg[3:].split("/?")

    for nack in nack_recv:
        id_message_list = nack[3:]
        messages_ressend: list[str] = []
        for msg in message_list:
            if msg[0] in id_message_list: messages_ressend.append(msg)

        message_final = f"M{nack[0]}" + "/?".join(messages_ressend)

        websocket.send(id_client + message_final)
        conn.add_message(id_client + message_final)
        message = websocket.recv()
        print(f"Received: {message}")

    return

async def lider_received(conn: Client, websocket: ClientConnection, lider_recv: list[str], id_emissor: str):

    websocket.send(f"{id_emissor}S{conn.group}")
    id_clients = websocket.recv()

    if id_clients == "F": return

    for msg in lider_recv:
        for id_client in id_clients:
            mensagem_final = f"{id_emissor}M{id_client}{msg[3:]}"

            websocket.send(mensagem_final)
            conn.add_message(mensagem_final)
            message = websocket.recv()
            print(f"Received: {message}")

    return

async def send_assert(conn: Client, websocket: ClientConnection, group_recv: dict, id_emissor: str):

    for sender_group, message_ids in group_recv.items():
        ids_recv = "".join(message_ids)
        mensagem_final = f"{id_emissor}A{sender_group[2]}{sender_group[0]}{ids_recv}"
        websocket.send(mensagem_final)
        conn.add_message(mensagem_final)
        message = websocket.recv()
        print(f"Received: {message}")

    return

async def assert_received(conn: Client, websocket: ClientConnection, assert_recv: list[str], group_recv: dict, id_emissor: str, falty: bool = False):

    for message in assert_recv:
        id_grupo = message[2]
        id_emissor_original = message[3]
        ids_to_assert = message[4:] 
        ids_received_list = group_recv[f"{id_emissor_original}G{id_grupo}"]
        ids_received = "".join(ids_received_list)

        if falty: ids_received = input("Insira od ids de mensagem 'recebidos':")

        if ids_to_assert == ids_received:
            print("OK")

        else: #test and send nack
            nack_list: list[str] = []

            for id_message in ids_to_assert:
                if id_message not in ids_received:
                    nack_list.append(id_message)

            if nack_list: 
                print(f"NACK ids {nack_list}")
                #send NACK
                ids_nack = "".join(nack_list)
                mensagem_final = f"{id_emissor}N{id_emissor_original}{ids_nack}"
                websocket.send(mensagem_final)
                conn.add_message(mensagem_final)
                message = websocket.recv()
                print(f"Received: {message}")

    return