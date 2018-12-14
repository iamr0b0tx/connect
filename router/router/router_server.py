import socket, time
import urllib.request as browser

server = socket.socket()
server.bind(("10.0.0.100",5000))
server.listen(1)
client, address = server.accept()
client.send("connection made".encode())
while True:
    length = client.recv(1024)
    client.send(length)
    msg = client.recv(int(length.decode())+1024)
    
    if msg.startswith(b'ok'):
        print(msg)
        
    elif msg.startswith(b'url:'):
        print("url:"+msg.decode()+" recieved by server")
        print(msg.decode())
        url = msg.replace(b'url:', b'', 1).decode()[:-1]
        print(url)
        try:
            cont = browser.urlopen(url)
            contents = cont.read()

            client.send(str(len(contents)+1024).encode())
            if client.recv(5000) == str(len(contents)+1024).encode():
                print("sending contents...")
                client.send(contents)
                fn = open("page.html","wb")
                fn.write(contents)
                fn.close()
            else:
                client.send("failed".encode())

        except Exception as e:
            print("server can't read url")
            contents = "failed".encode()
##            client.send(str(len(url)).encode())
##            if client.recv(1024) == str(len(url)).encode():
##                client.send(url)

            client.send(str(len(contents)+1024).encode())
            if client.recv(5000) == str(len(contents)+1024).encode():
                client.send(contents)
    else:
        print(msg)
        
##    if 1 == 1: break
client.close()
