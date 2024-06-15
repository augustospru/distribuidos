import asyncio
from websockets.server import serve
import websockets as ws
from connection import Connection
from server_func import add_connection

messages_buffer: list[str] = []
connections_buff: list[Connection] = []
has_lider = False

async def echo(websocket: ws.WebSocketServerProtocol):
    global has_lider
    async for message in websocket:
        print(message)

        #new connection
        if message == "C":
            has_lider = await add_connection(websocket, messages_buffer, connections_buff, has_lider)

        else:
            id_message = int(message[0])
            messages_buffer[id_message - 1] = message
            await websocket.send('-'.join(messages_buffer))

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())