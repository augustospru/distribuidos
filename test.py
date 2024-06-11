# Echo client program
import socket, time

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    i = 0
    while True:
        i += 1
        s.sendall(b'AAAAAAAHello, world ' + str(i).encode())
        data = s.recv(1024)
        print('Received', repr(data))
        time.sleep(3)