import socket
import os

if __name__ == '__main__':
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if os.path.exists("/tmp/test.sock"):
        os.unlink("/tmp/test.sock")
    server.bind("/tmp/test.sock")
    server.listen(0)
    while True:
        connection, address = server.accept()
        connection.send("test: %s"% connection.recv(1024))
    connection.close()