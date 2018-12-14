import socket
import urllib.request as browser
import sys, time, os

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

def write_file(file, byte_data):
    if os.path.exists(os.getcwd()+'/'+file):
        f = open(file, 'ab')
    else:
        f = open(file, 'wb')
    f.write(byte_data)
    f.close()
  
while True:
    try:
        urlf = open("url.txt")
        url = urlf.read()
        urlf.close()
        file = url.split('/')[-1]
        
        if url == last_url:
            print(url, "--", last_url)
            raise Exception
        
        try:
            b, cont = open_url(url)
            
            if b:
##                contents = cont.read()
##                write_file(file, contents)
                raise Exception
            
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
                contents = recieve(client, length)

                if contents != b"failed":
                    write_file(file, contents)
                    
    except Exception as e:
        print(e)

    last_url = url
    time.sleep(0.1)        
client.close()
