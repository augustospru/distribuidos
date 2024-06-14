import asyncio
from websockets.server import serve
import websockets as ws
from connection import Connection

messages_buffer: list[str] = []
connections_buff: list[Connection] = []

async def echo(websocket: ws.WebSocketServerProtocol):
    async for message in websocket:
        print(message)

        #new connection
        if message == "C":
            last_id = 1
            if connections_buff:
                last_id = max(int(conn.id) for conn in connections_buff) + 1

            await websocket.send(str(last_id))
            connections_buff.append(Connection(str(last_id), True))
            messages_buffer.append('')

        else:
            id_message = int(message[0])
            messages_buffer[id_message - 1] = message
            await websocket.send('-'.join(messages_buffer))

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())