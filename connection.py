class Connection:
    id: str | None = None
    taken: bool = False
    perfil: str = ""

    def __init__(self, id, taken, perfil):
        self.id = id
        self.taken = taken
        self.perfil = perfil

class Client:
    id: str | None = None
    perfil: str | None = None
    message_send: str | None = None
    last_message_rcv: str | None = None

    def __init__(self, id, perfil):
        self.id = id
        self.perfil = perfil

    def change_perfil(self, perfil):
        self.perfil = perfil