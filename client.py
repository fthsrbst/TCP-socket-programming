import socket
import select
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

s=socket.socket()
print("socket connected.")

port=9999
s.connect(('127.0.0.1',port))

print("------------Welcome to TCP Chat------------")
try:
    inputs = [s, sys.stdin]
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for r in readable:
            if r is s:
                data = s.recv(4096)
                if not data:
                    print("\nServer disconnected.")
                    raise SystemExit
                msg = data.decode().rstrip("\n")
                print(f"\rServer : {msg}\nClient : ", end="", flush=True)
                if msg.strip().lower() == "quit":
                    print("\nServer ended the chat.")
                    raise SystemExit
            else:  # sys.stdin
                line = sys.stdin.readline()
                if not line:
                    continue
                msg = line.rstrip("\n")
                s.send((msg + "\n").encode())
                if msg.strip().lower() == "quit":
                    print("\nYou ended the chat.")
                    raise SystemExit
                print("Client : ", end="", flush=True)

finally:
    s.close()