"""Capture video and stream it to a webpage"""
#pylint: disable=no-name-in-module
from base64 import b64encode
from socket import AF_INET, SOCK_STREAM, socket, gethostbyname, gethostname

from cv2 import (VideoCapture, destroyAllWindows, imencode, imshow, waitKey)

SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind((gethostbyname(gethostname()), 7503))
SOCK.listen(1)

STREAM = VideoCapture(0)


while True:
    RET, FRAME = STREAM.read()
    RETVAL, BUFFER = imencode('.jpg', FRAME)
    CONN, ADDR = SOCK.accept()
    DATA = CONN.recv(512).decode().split(' ')
    if DATA[0] == "GET":
        with open("test.html", "rb") as website:
            CONN.sendall(b"HTTP/1.1 200 OK\n\n" + website.read())
    elif DATA[0] == "VIDEO":
        CONN.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(BUFFER))
    CONN.close()
    imshow('frame', FRAME)
    if waitKey(1) & 0xFF == ord('q'):
        break
STREAM.release()
destroyAllWindows()
