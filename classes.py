class Connection:
    id: str | None = None
    taken: bool = False
    perfil: str = ""
    group: str = None
    message_buffer: str | None = None

    def __init__(self, id, taken, perfil, group = "1"):
        self.id = id
        self.taken = taken
        self.perfil = perfil
        self.group = group

    def add_message(self, message):
        if self.message_buffer: self.message_buffer = self.message_buffer + "/?" + message
        else: self.message_buffer = message

    def get_message(self):
        message_aux = self.message_buffer
        self.message_buffer = None
        return message_aux

class Client:
    id: str | None = None
    perfil: str | None = None
    group: str = None
    last_message_rcv: str | None = None

    def __init__(self, id, perfil, group = "1"):
        self.id = id
        self.perfil = perfil
        self.group = group
        self.message_send: list[str] = []

    def change_perfil(self, perfil):
        self.perfil = perfil

    def add_message(self, message):
        self.message_send.append(message)

class Group:
    message_buffer: str | None = None
    lider_id: str | None = None

    def __init__(self, id):
        self.id = id
        self.id_clients: list[str] = []

    def add_client(self, id_client):
        self.id_clients.append(id_client)

    def add_message(self, message): # /? used as separator between multiple messages
        if self.message_buffer: self.message_buffer = self.message_buffer + "/?" + message
        else: self.message_buffer = message

    def clear_message(self):
        self.message_buffer = None

    def get_message(self):
        return self.message_buffer