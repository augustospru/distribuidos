import asyncio
from websockets.server import serve
import websockets as ws
from classes import Connection, Group
from server_func import add_connection, group_messages, assert_messages, has_messages, nack_messages, peer_2_peer_messages

connections_buff: list[Connection] = []
has_lider = False
group_list: list[Group] = [Group("1"), Group("2"), Group("3")]

async def echo(websocket: ws.WebSocketServerProtocol):
    global has_lider
    async for message in websocket:
        print(message)

        #new connection
        if message == "C":
            has_lider = await add_connection(websocket, connections_buff, has_lider)

        else:
            id_client = int(message[0])
            message_func = message[1]

            try:
                match message_func:
                    case "G":
                        await group_messages(message, websocket, group_list)
                    
                    case "H":
                        await has_messages(message, websocket, connections_buff, group_list)

                    case "A":
                        await assert_messages(message, websocket, connections_buff, has_lider)

                    case "N":
                        await nack_messages(message, websocket, connections_buff, has_lider)

                    case "M":
                        await peer_2_peer_messages(message, websocket, connections_buff, has_lider)
                            
                    case _:
                        # messages_buffer[id_message - 1] = message
                        # await websocket.send('-'.join(messages_buffer))
                        await websocket.send("T")
            except:
                await websocket.send("F")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())