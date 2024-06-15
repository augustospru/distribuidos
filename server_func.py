import websockets as ws
from classes import Connection, Group

#add new client to list of connections
async def add_connection(
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    has_lider: bool
):
    last_id = 1
    if connections_buff:
        last_id = max(int(conn.id) for conn in connections_buff) + 1

    perfil = "S"
    if not has_lider: 
        perfil = "L"
        has_lider = True

    await websocket.send(str(last_id) + perfil)

    connections_buff.append(Connection(str(last_id), True, perfil))

    return has_lider

#send messages to a group
async def group_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    group_list: list[Group]
):
    if len(message) < 5: await websocket.send("F")

    id_emissor = message[0]
    id_group = int(message[2])
    message_to = message[3:]

    group_list[id_group - 1].add_message(id_emissor + message_to)
    
    await websocket.send("T")
    return 

#check if server has messages to client
async def has_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    group_list: list[Group]
):
    if len(message) < 3: await websocket.send("F")

    id_client = int(message[0])
    get_type = message[2]

    client = connections_buff[id_client - 1]

    if get_type == "G":
        group_message = group_list[int(client.group) - 1].get_message()

        if group_message: await websocket.send(group_message)
        else: await websocket.send("F")


    if get_type == "P":
        peer_message = client.get_message()
        if peer_message: await websocket.send(peer_message)
        else: await websocket.send("F")
    
    return 

#assert with group if all messages were gotten
async def assert_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    has_lider: bool
):
    print(message)
    
    await websocket.send("T")
    return 

#send nack response
async def nack_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol,  
    connections_buff: list[Connection],
    has_lider: bool
):
    print(message)
    
    await websocket.send("T")
    return 

#send peer 2 peer messages
async def peer_2_peer_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    has_lider: bool
):
    if len(message) < 4: await websocket.send("F")

    id_emissor = message[0]
    id_client = int(message[2])
    message_to = message[3:]

    connections_buff[id_client - 1].add_message(id_emissor + message_to)
    
    await websocket.send("T")
    return 