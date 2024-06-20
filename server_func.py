import websockets as ws
from classes import Connection, Group
import random

#add new client to list of connections
async def add_connection(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    group_list: list[Group],
    has_lider: bool
):
    last_id = 1
    if connections_buff:
        last_id = max(int(conn.id) for conn in connections_buff) + 1

    perfil = "S"
    if not has_lider: 
        perfil = "L"
        has_lider = True

    id_group = ""
    if len(message) > 1: id_group = message[1] #add presend group
    else: id_group = str(random.randrange(3)) #add to random group

    client = Connection(str(last_id), True, perfil, id_group)

    await websocket.send(str(last_id) + perfil + id_group)

    connections_buff.append(client)
    group_list[int(client.group) - 1].add_client(client.id)

    return has_lider

#send messages to a group
async def group_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    group_list: list[Group]
):
    """
    Estrutura da mensagem:
    XGYZ[...](/?[Z[...]])
    X => id_emissor (acoplado pelo cliente)
    G => identificador da funcao
    Y => id_grupo que se quer enviar a(s) mensagem(ns)
    Z => id_mensagem (acoplada pelo nodo)
    [...] => corpo da mensagem
    caso queira se enviar mais de uma mensagem o separador '/?' deve ser usado entre uma mensagem e outra

    exemplo:
    caso 1 uma mensagem, nodo deve enviar G21mensagem
    Será uma mensagem de id 1 e corpo "mensagem" em grupo para o grupo 2

    caso 2 multiplas mensagens, nodo deve enviar G22mensagem1/?3mensagem2/?4mensagem3
    Serao 3 mensagengs de id 2, 3 e 4 e corpos "mensagem1", "mensagem2", "mensagem3" em grupo para o grupo 2
    """
    if len(message) < 5: await websocket.send("F")

    id_emissor = message[0]
    id_group = int(message[2])
    message_to = message[3:]
    message_aux = message_to.split("/?")

    for message in message_aux:
        group_list[id_group - 1].add_message(id_emissor + message)
    
    await websocket.send("T")
    return 

#check if server has messages to client
async def has_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    group_list: list[Group]
):
    """
    Estrutura da mensagem:
    XH(G/P)
    X => id_emissor (acoplado pelo cliente)
    H => identificador da funcao
    G => quero receber mensagem do grupo
    P => quero receber mensagem direta (peer2peer)

    exemplo:
    caso 1 quero receber mensagem do grupo, nodo deve enviar HG

    caso 2 quero receber mensagem que enviaram ao nodo, nodo deve enviar HP
    """
    if len(message) < 3: await websocket.send("F")

    id_client = int(message[0])
    get_type = message[2]

    client = connections_buff[id_client - 1]

    if get_type == "G":
        group_message = group_list[int(client.group) - 1].get_message()

        if group_message: await websocket.send(group_message)
        else: await websocket.send("F")


    elif get_type == "P":
        peer_message = client.get_message()
        if peer_message: await websocket.send(peer_message)
        else: await websocket.send("F")
    
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
    """
    Estrutura da mensagem:
    XNYZ[Z..]
    X => id_emissor (acoplado pelo cliente)
    N => identificador da funcao
    Y => id_emissor_original da mensagem
    Z => id_mensagem perida

    exemplo:
    caso 1 duas mensagens perdidas: 3N116
    Informará ao emissor original de id 1 que as mensagens 1 e 6 nao chegaram ao cliente
    """
    if len(message) < 4: await websocket.send("F")

    id_emissor_original = int(message[2])

    connections_buff[id_emissor_original - 1].add_message(message)
    
    await websocket.send("T")
    return 

#send peer 2 peer messages
async def peer_2_peer_messages(
    message: ws.Data,
    websocket: ws.WebSocketServerProtocol, 
    connections_buff: list[Connection],
    has_lider: bool
):
    """
    Estrutura da mensagem:
    XMYZ[...](/?[Z[...]])
    X => id_emissor (acoplado pelo cliente)
    M => identificador da funcao
    Y => id_mensagem que se quer enviar a(s) mensagem(ns)
    Z => id_mensagem (acoplada pelo nodo)
    [...] => corpo da mensagem
    caso queira se enviar mais de uma mensagem o separador '/?' deve ser usado entre uma mensagem e outra

    exemplo:
    caso 1 uma mensagem, nodo deve enviar M21mensagem
    Será uma mensagem de id 1 e corpo "mensagem" para o cliente de id de 2

    caso 2 multiplas mensagens, nodo deve enviar M22mensagem1/?3mensagem2/?4mensagem3
    Serao 3 mensagengs de id 2, 3 e 4 e corpos "mensagem1", "mensagem2", "mensagem3" para o cliente de id de 2
    """
    if len(message) < 4: await websocket.send("F")

    id_emissor = message[0]
    id_client = int(message[2])
    message_to = message[3:]
    message_aux = message_to.split("/?")

    for message in message_aux:
        connections_buff[id_client - 1].add_message(id_emissor + message)
    
    await websocket.send("T")
    return 