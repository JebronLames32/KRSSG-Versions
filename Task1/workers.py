import socket
import numpy as np
import time


reached=['1',]
host='127.0.0.1'
port= 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
while True:
    #l, h = [int(i) for i in s.recv(8).decode('utf-8').split('\n')]
    p=s.recv(8).decode('utf-8')
    l=p[0]
    h=p[2]
    print(l)
    print(h)
    print(type(l))
    break
l=int(l)
h=int(h)
w='1'
while(w=='1'or w=='A' or w=='B' or w=='C' or w=='D'):
    r=np.random.randint(l,h)
    #print(r)
    if w not in reached:
        reached.append(w)
        print(w,"HAS SUCCESSFULLY ESCAPED")
    s.send(str(r).encode("utf-8"))
    time.sleep(1)
    w=s.recv(1).decode('utf-8')
time.sleep(2)
s.close()
