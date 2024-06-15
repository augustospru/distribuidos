class Connection:
    id: str | None = None
    taken: bool = False
    perfil: str = ""
    group: str = None

    def __init__(self, id, taken, perfil, group = "1"):
        self.id = id
        self.taken = taken
        self.perfil = perfil
        self.group = group

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