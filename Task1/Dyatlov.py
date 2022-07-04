import socket
import threading
import time
import os


(rows,cols)=(10,10)
grid=[[None]*10 for i in range(10)]
#stepsize=[[None]for i in range(4)]
posclient=[0,0,0,0]             #maintains position of all clients. A value using which coordinates are computed
clients=['A','B','C','D']       #naming the clients
escapeorder=[]
count=0
countingstep=0
lastout='1'
t=[[None]for i in range(4)]

def printgrid():
    for i in range(rows):
        for j in range(cols):
            print(grid[i][j], " ", end="")      #
        print("\n")

bombcord={(0,9),(1,1),(1,3),(1,9),(2,5),(2,8),(4,0),(4,7),(5,4),(7,0),(7,7),(8,4),(9,2),(9,7)}

def setbacktonormal():
    for i in range(rows):
        for j in range(cols):
            if (i,j) in bombcord:
                grid[i][j]='#'
            else:
                grid[i][j]='.'

setbacktonormal()
printgrid()


def calculateXandY(i):
    rem1=(posclient[i]-1)//10
    x=9-rem1
    rem=(posclient[i]-1)%10
    if(rem1%2==1):
        y=9-rem
    else:
        y=rem
    return(x,y)

def stepchanges():
    for i in range(4):
        (x,y)=calculateXandY(i)
        print("client",i,x,y)
        if(grid[x][y]!='#'):
            grid[x][y]=clients[i]
        elif (x,y) in bombcord:
            print("BOMB")
            if(posclient[i]>10):
                while(grid[x][y]=='#' and posclient[i]>10):
                    posclient[i]=posclient[i]-8
                    (x,y)=calculateXandY(i)
                
            
            
            grid[x][y]=clients[i]
    printgrid()


def threaded(c,z):
    global count
    global countingstep
    global lastout
    while True:
        c.send(str(l).encode())
        c.send("\n".encode())
        c.send(str(r).encode())
        w=0
        while True:   
            step=c.recv(1).decode('utf-8')
            step=int(step)
            print("stepsize",z,":",step,"w",w)
            
            #stepsize[count%4]=step
            #sum=posclient[count]
            #sum=sum+step
            posclient[z]+=step
            lock.acquire()
            count+=1
            lock.release()
            print("count",count,"z",z)
            if(posclient[z]>99):
                print("I'm out")
                posclient[z]=100
                c.send('0'.encode())
                break
            c.send(lastout.encode())
            
            if(count%4==0):
                stepchanges()
                setbacktonormal()
            #while(count%4!=0):
                #time.sleep(0.1)


            # wait until count is 4 or multiple of 4.. this is to ensure that all 4 clients have responded.
            # each client will wait till other clients have responded before talking back again.

            #print("stepsize:",stepsize[count%4])
        
        lastout=clients[z]  
        escapeorder.append(lastout)  
        break
 
port = 12345
host=''
l=1
r=7
lock=threading.Lock()

def Main():
    global count
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    print ("Socket successfully created")

    s.bind((host, port))        
    print ("socket binded to %s" %(port))

    s.listen(5)    
    print ("socket is listening")  


    for z in range(4):          #4 clients only
        c, addr = s.accept()    
        print ('Got connection from', addr )
        print(threading.active_count())
            
        
        t[z] = threading.Thread(target=threaded, args=(c,z))
        #t2 = threading.Thread(target=threaded, name='t2', args=(c,1))
        #numclient=threading.activeCount()-1

    for q in range(4):
        t[q].start()
        time.sleep(0.1)
        #t2.start()
        #t1.join()
        #t2.join()
    #while True:
        #time.sleep(.1)
        #if(count%4==0):
            #stepchanges()
        

    
    #c.close()

if __name__=="__main__":
    Main()
    while len(escapeorder)<4:
        time.sleep(.1)
    print(escapeorder[0], "Got out First")
    print(escapeorder[1], "Got out second")
    print(escapeorder[2], "Got out third")
    print(escapeorder[3], "Got out fourth")
