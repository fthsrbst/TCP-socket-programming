#TCP soket kütüphanesi import ediyoruz
import socket
import sys

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
        c.close
except KeyboardInterrupt:
    print("Server interrupted, shutting down.")
finally:
    s.close

    