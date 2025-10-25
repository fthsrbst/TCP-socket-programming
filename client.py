import socket
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

s=socket.socket()
print("socket connected.")

port=8080
s.connect(('127.0.0.1',port))

print("------------Welcome to TCP Chat------------")
while True:
    data = s.recv(1024)
    print("Server : ",data.decode())

    while True:
        message = input("Client : ")
        s.send(message.encode())

print(s.recv(1024).decode())
s.close

