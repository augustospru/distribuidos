import websockets as ws
from connection import Connection

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