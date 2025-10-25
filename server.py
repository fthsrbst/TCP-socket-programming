
#TCP soket kütüphanesi import ediyoruz
import socket
import sys
import select
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
messages = []

#socket değişkeni yaratılıyor
s = socket.socket()
print("Socket succesfully created.")

#dinlenecek port numarası 8080 olarak belirliyoruz.
port = 9999

#soketi yerel IP ve Porta bağla. '' parametresi tüm ağ arayüzlerini temsil eder (0.0.0.0)
s.bind(('',port))
print ("Socket binded to %s" %(port)) 

#dinleme modu
s.listen(5) #buradaki 5 backlog yani bağlantı kuyruğunun maksimum uzunluğu
print("Socket is listening")
try:
    c, addr = s.accept()
    print("Got connection from", addr)
    c.send("Thank you for connecting".encode())
    print("------------Welcome to TCP Chat------------")
    print("Server : ", end="", flush=True)

    inputs = [c, sys.stdin]  # soket + klavye
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for r in readable:
            if r is c:
                data = c.recv(4096)
                if not data:
                    print("\nClient disconnected.")
                    raise SystemExit
                msg = data.decode().rstrip("\n")
                # Alınan mesaj, mevcut promptu bozmadan yazılsın
                print(f"\rClient : {msg}\nServer : ", end="", flush=True)
                if msg.strip().lower() == "quit":
                    print("\nClient ended the chat.")
                    raise SystemExit
            else:  # sys.stdin
                line = sys.stdin.readline()
                if not line:
                    continue
                msg = line.rstrip("\n")
                c.send((msg + "\n").encode())
                if msg.strip().lower() == "quit":
                    print("\nYou ended the chat.")
                    raise SystemExit
                # tekrar prompt göster
                print("Server : ", end="", flush=True)



except KeyboardInterrupt:
    print("Server interrupted, shutting down.")
finally:
    c.close
    s.close

    