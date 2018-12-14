import socket
import urllib.request as browser
import sys, time

ip = str(sys.argv[1])

def open_url(url):
    t = False
    try:
        c = browser.urlopen(url)
        t = True
        return t, c
    except Exception as e:
        return (False, b'')
    
client = socket.socket()
client.connect((ip, 5000))
print(client.recv(1024).decode())
last_url = ""
while True:
    try:
        urlf = open("url.txt")
        url = urlf.read()
        urlf.close()

##        if url == last_url:
##            print(url, "--", last_url)
##            raise Exception
        
        try:
            b, cont = open_url(url)
            
            if b:
                contents = b"ok" #cont.read()

                client.send(str(len(contents)+1024).encode())
                if client.recv(5000) == str(len(contents)+1024).encode():
                    client.send(contents)
                    print(cont.read())
            else:
                raise Exception
                        
        except Exception as e:
            print("client2 can't read url:"+url)
            client.send(str(len(url)+1024).encode())
            if client.recv(5000) == str(len(url)+1024).encode():
                print("url sent")
                client.send(("url:"+url).encode())

                length = client.recv(5000)
                client.send(length)
                contents = client.recv(int(length.decode()))

                if contents != b"failed":
                    print(contents)
                    fn = open("sprite_all.png","wb")
                    fn.write(contents)
                    fn.close()
    except Exception as e:
        print(e)
        client.send(str(len("ok")+1024).encode())
        if client.recv(5000) == str(len("ok")+1024).encode():
            print("ok")
            client.send(("ok").encode())

    last_url = url
    time.sleep(0.1)        
client.close()
