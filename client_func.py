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