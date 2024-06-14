class Connection:
    id: str | None = None
    taken: bool = False

    def __init__(self, id, taken):
        self.id = id
        self.taken = taken

class Client:
    id: str | None = None
    message_send: str | None = None
    last_message_rcv: str | None = None

    def __init__(self, id):
        self.id = id