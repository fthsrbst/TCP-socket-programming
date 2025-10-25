
#TCP soket kütüphanesi import ediyoruz
import socket
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
messages = []

#socket değişkeni yaratılıyor
s = socket.socket()
print("Socket succesfully created.")

#dinlenecek port numarası 8080 olarak belirliyoruz.
port = 8080

#soketi yerel IP ve Porta bağla. '' parametresi tüm ağ arayüzlerini temsil eder (0.0.0.0)
s.bind(('',port))
print ("Socket binded to %s" %(port)) 

#dinleme modu
s.listen(5) #buradaki 5 backlog yani bağlantı kuyruğunun maksimum uzunluğu
print("Socket is listening")
try:
    while True:
        c, addr = s.accept()
        print("Got connection from", addr)
        c.send("Thank you for connecting".encode())
        
        print("------------Welcome to TCP Chat------------")

        while True:
            data = c.recv(1024)
            print("Client : ",data.decode())

            while True:
                message = input("Server : ")
                c.send(message.encode())


except KeyboardInterrupt:
    print("Server interrupted, shutting down.")
finally:
    c.close
    s.close

    