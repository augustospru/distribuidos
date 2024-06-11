# Echo server program
import socket
import _thread as thread

def on_new_client(conn: socket.socket, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                continue
            data = data + b' rcvd'
            conn.sendall(data)
        conn.close()


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("new connection: ", addr)
        thread.start_new_thread(on_new_client,(conn, addr))