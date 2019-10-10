"""Capture video and stream it to a webpage"""
# pylint: disable=no-name-in-module, unused-variable
from base64 import b64encode
from socket import AF_INET, SOCK_STREAM, gethostbyname, gethostname, socket
from threading import Thread

from cv2 import VideoCapture, imencode

SOCK = socket(AF_INET, SOCK_STREAM)
HOST = gethostbyname(gethostname())
PORT = int(input("Port: "))
SOCK.bind((HOST, PORT))
print(f"{HOST}:{PORT}")
SOCK.listen(1)

STREAM = VideoCapture(0)


def server():
    """Stream live video"""
    ret, frame = STREAM.read()
    retval, buffer = imencode('.jpg', frame)
    server_thread = Thread(target=server, daemon=True)
    conn, addr = SOCK.accept()
    server_thread.start()
    conn.settimeout(2)
    try:
        data = conn.recv(512).decode().split(' ')
        if data[0] == "GET":
            with open("stream.html", "rb") as website:
                conn.sendall(b"HTTP/1.1 200 OK\n\n" + website.read())
        elif data[0] == "VIDEO":
            conn.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(buffer))
    except ConnectionResetError:
        return
    conn.close()


server()
while True:
    try:
        pass
    except KeyboardInterrupt:
        break
STREAM.release()
