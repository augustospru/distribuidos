class Connection:
    id: str | None = None
    taken: bool = False
    perfil: str = ""
    group: str = None
    message_to: list[str] = []

    def __init__(self, id, taken, perfil, group = "1"):
        self.id = id
        self.taken = taken
        self.perfil = perfil
        self.group = group

    def add_message(self, message):
        self.message_to.append(message)

    def get_message(self):
        message_aux = self.message_to.copy()
        self.message_to = []
        return message_aux

class Client:
    id: str | None = None
    perfil: str | None = None
    group: str = None
    message_send: str | None = None
    last_message_rcv: str | None = None

    def __init__(self, id, perfil, group = "1"):
        self.id = id
        self.perfil = perfil
        self.group = group

    def change_perfil(self, perfil):
        self.perfil = perfil

class Group:
    id: str | None = None
    message_buffer: str | None = None
    id_clients: list[str] = []

    def __init__(self, id):
        self.id = id

    def add_client(self, id_client):
        self.id_clients.append(id_client)

    def add_message(self, message):
        self.message_buffer = message

    def get_message(self):
        return self.message_buffer