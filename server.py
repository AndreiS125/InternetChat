import socket
from threading import Thread
import struct

messages = []
users= {}

def send(conn, text):
    text = text.encode("utf-8")
    size = struct.pack("<I", len(text))
    conn.send(size)
    conn.send(text)


def recv(conn, logen):
    while True:
        a=conn.recv(4)
        print(a)
        size = struct.unpack("<I", a)[0]
        m=conn.recv(size).decode("utf-8")
        print(m)
        m=logen+": "+m
        messages.append(m)
        for user in users.keys():
            if(logen!=user):
                send(users[user],m)

sock = socket.socket()
sock.bind(("127.0.0.1", 9090))

sock.listen(10)


while True:
    conn, addr = sock.accept()
    a = conn.recv(4)
    print(a)
    size = struct.unpack("<I", a)[0]
    logen = conn.recv(size).decode("utf-8")

    users[logen]=conn



    th = Thread(target=recv, args=(conn,logen,))
    th.start()
