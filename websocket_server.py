import asyncio
from websockets.server import serve
import websockets as ws

messages_buffer = ['','']

async def echo(websocket: ws.WebSocketServerProtocol):
    async for message in websocket:
        print(message)
        if message[0] == "1": i = 0
        else: i = 1
        messages_buffer[i] = message
        await websocket.send('-'.join(messages_buffer))

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())