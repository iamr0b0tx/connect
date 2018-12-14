import socket, time
import urllib.request as browser

server = socket.socket()
server.bind(("127.0.0.1",5000))
server.listen(1)
client, address = server.accept()
client.send("connection made".encode())
        
while True:
    length = client.recv(1024)
    client.send(length)
    print(length)
    msg = client.recv(int(length.decode())+1024)
    
    if msg.startswith(b'ok'):
        print(msg)
        
    elif msg.startswith(b'url:'):
        url = msg.replace(b'url:', b'', 1).decode()#[:-1]
        print(url)
        try:
            cont = browser.urlopen(url)
            contents = cont.read()

            client.send(str(len(contents)+1024).encode())
            if client.recv(5000) == str(len(contents)+1024).encode():
                send(client, contents)
                
            else:
                client.send("failed".encode())

        except Exception as e:
            print("server can't read url")
            contents = b"failed"
            client.send(str(len(contents)+1024).encode())
            if client.recv(5000) == str(len(contents)+1024).encode():
                send(client, contents)
               
    else:
        print(msg)
        
##    if 1 == 1: break
client.close()
