import websockets as ws
from connection import Connection

#add new client to list of connections
async def add_connection(
    websocket: ws.WebSocketServerProtocol, 
    messages_buffer: list[str], 
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
    messages_buffer.append('')

    return has_lider

#send messages to a group
async def group_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    messages_buffer: list[str], 
    connections_buff: list[Connection],
    has_lider: bool
):
    print(message)
    
    await websocket.send("T")
    return 

#check if server has messages to client
async def has_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    messages_buffer: list[str], 
    connections_buff: list[Connection],
    has_lider: bool
):
    print(message)
    
    await websocket.send("T")
    return 

#assert with group if all messages were gotten
async def assert_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    messages_buffer: list[str], 
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
    messages_buffer: list[str], 
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
    messages_buffer: list[str], 
    connections_buff: list[Connection],
    has_lider: bool
):
    print(message)
    
    await websocket.send("T")
    return 