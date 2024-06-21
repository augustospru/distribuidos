import asyncio
from websockets.server import serve
import websockets as ws
from classes import Connection, Group
from server_func import add_connection, group_messages, assert_messages, has_messages, nack_messages, peer_2_peer_messages, lider_messages, servos_in_group

connections_buff: list[Connection] = []
group_list: list[Group] = [Group("1"), Group("2"), Group("3")]

async def echo(websocket: ws.WebSocketServerProtocol):
    async for message in websocket:
        print(message)

        #new connection
        if message[0] == "C":
            await add_connection(message, websocket, connections_buff, group_list)

        else:
            id_client = int(message[0])
            message_func = message[1]

            try:
                match message_func:
                    case "G":
                        await group_messages(message, websocket, group_list, connections_buff)
                    
                    case "H":
                        await has_messages(message, websocket, connections_buff, group_list)

                    case "A":
                        await assert_messages(message, websocket, connections_buff, group_list)

                    case "N":
                        await nack_messages(message, websocket, connections_buff)

                    case "M":
                        await peer_2_peer_messages(message, websocket, connections_buff)

                    case "L":
                        await lider_messages(message, websocket, connections_buff, group_list)

                    case "S":
                        await servos_in_group(message, websocket, group_list)
                            
                    case _:
                        await websocket.send("F")
            except:
                await websocket.send("F")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())