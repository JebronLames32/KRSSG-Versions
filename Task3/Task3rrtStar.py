import cv2
import numpy as np
import math
import time

##Global variables 
path=[]
img = cv2.imread('task3.1.png', 0)
img2=cv2.imread('task3.1.png', 0)
(m, n) = (img.shape)
a, b = (45, 50)
endcolor=82     #start
##

##Thresholding
for i in range(m):
    for j in range(n):
        if(img[i,j]<10):
            img[i,j]=0
        elif(img[i,j]>245):
            img[i,j]=255
        elif(img[i,j]>115 and img[i,j]<150):
            img[i,j]=134
        elif(img[i,j]>70 and img[i,j]<95):
            img[i,j]=endcolor
##

##initialization
img[a, b] = 170
path.append((a,b))
print(a,b)
print(img.shape)
xrand=a
yrand=b


cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', img)
cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
cv2.imshow('Image2', img2)


##distance between two points
def dist(x1,y1,x2,y2):
    k1 = (x1-x2)*(x1-x2)
    k2 = (y1 - y2) * (y1 - y2)
    u = (k1+k2)     
    u=math.sqrt(u)
    return u

def addcoordinate(xmin,ymin,xrand,yrand):
    dist2Pix=4          # change this variable to vary distance between two adjacent pixels in path
    if(xrand>xmin):
        xadd=xmin+dist2Pix
    elif(xrand<xmin):
        xadd=xmin-dist2Pix
    else:
        xadd=0
    if(yrand>ymin):
        yadd=ymin+dist2Pix
    elif(yrand<ymin):
        yadd=ymin-dist2Pix
    else:
        yadd=0
    return(xadd,yadd)

def displayimage():
    cv2.imshow('Image', img.astype(np.uint8))
    cv2.waitKey(5)


##Reccursive function that traverses the list once to find the ultimate path
def pathneighbours(x,y,i):
    global count2
    
    #print("here")
    neighbours=neighbourInPathPixelsList(x,y)
    #print(neighbors)
    j=0
    for p in path[i::-1]:
        j+=1
        if p in neighbours:
            if(p==(a,b)):
                print("reached start")
                time.sleep(1)
                return
            
            img2[p]=250
            cv2.imshow('Image2', img2.astype(np.uint8))
            cv2.waitKey(5)
            print(p)
            (x,y)=p
            count2+=1
            print("i,j = ", i, j)
            pathneighbours(x,y,i-j)
            return


def neighbourInPathPixelsList(x,y):
    neighbours=[]
    for cord1 in range (-4,5,4):
        for cord2 in range (-4,5,4):
            if(img[cord1+x,cord2+y]==170 and (cord1,cord2)!=(0,0)):
                neighbours.append((x+cord1,y+cord2))                 ##will find all the neighbors in the path
    return(neighbours)

def newStartLinks(xnew,ynew,minx,miny):
    mindist=dist(minx,miny,xnew,ynew)
    (minNx,minNy)=(minx,miny)
    neighbors=neighbourInPathPixelsList(xnew,ynew)
    for (xneigh,yneigh) in neighbors:
        if(dist(xneigh,yneigh,xnew,ynew)<mindist):
            print("yes it got changed",(xnew,ynew))         ##almost no change is happening every time. Suggests that initial dist is mindist nearly all the time
            mindist=dist(xneigh,yneigh,xnew,ynew)
            (minNx,minNy)=(xneigh,yneigh)
    
            
    ind=path.index((minNx,minNy))
    path.insert(ind+1,(xnew,ynew))
    return(minNx,minNy)

                                                                                  ##neighbours
def ConvertsteptoRRTstar(x,y,xorigin,yorigin):                                  #       #       #
    neighbours=neighbourInPathPixelsList(x,y)                                   
    costNeighbour=[]                                                   #(origin)#------>#       #
    for particularNeighbour in neighbours:                                           #(x,y)
        cost=0                                                                  #       #       #
        (intermediateNodex,intermediateNodey)=(xorigin,yorigin)                                                
        for p in path[path.index(particularNeighbour):]:
            if(p in neighbours):                                               #only cost to elements in the path coming after the origin will be found
                if(p!=particularNeighbour):
                    (x1,y1)=p
                    cost+=dist(x1,y1,intermediateNodex,intermediateNodey)       #x1,y1 made to pass p as arguement into dist function
                    (intermediateNodex,intermediateNodey)=p
                elif(p==particularNeighbour):
                    (x1,y1)=p
                    cost+=dist(x1,y1,intermediateNodex,intermediateNodey)       #### jooks like jargon, hard to understand, gotta change ####
                    costNeighbour.append((neighbours.index(particularNeighbour),cost))  
                    break
    #found cost to nodes in neighbourhood (reference origin)
    #now making necessary changes
    OriginToCenter=dist(xorigin,yorigin,x,y)
    #print(OriginToCenter)          #?? why is this constant and equal to 5.5...
    for node in costNeighbour:
        (x1,y1)=neighbours[node[0]]
        
        CenterToNode=dist(x1,y1,x,y)                            #since 0 contains index of neighbour and 1 contains cost of neighbour
        #print(node[1],OriginToCenter+CenterToNode,neighbours[node[0]])
        #time.sleep(1)
        if (node[1]>OriginToCenter+CenterToNode):
            print("i'm changing")
            



##create a main function and initialize a,b as starting point
count2=0
def Main():
    count=0
    (xadd,yadd)=(a,b)
    while (True) :
        xrand = np.random.randint(0, n)
        yrand = np.random.randint(0, m)
        #print(xrand,yrand)
        min=100000
        #checking that it is a valid path
        if (img[xrand,yrand] == 0 or img[xrand,yrand]==82):    
            ##finds the nearest node in the tree to the random point
            for (x,y) in path:
                #print(dist(x, y, xrand, yrand))
                if (dist(x, y, xrand, yrand) < min):
                    min = dist(x, y , xrand, yrand)
                    xmin=x
                    ymin=y
                    
            (xadd,yadd)=addcoordinate(xmin,ymin,xrand,yrand)
            if(img[xadd,yadd]!=255 and img[xadd,yadd]!=170 and xadd>0 and yadd>0):
                
                (xmin,ymin)=newStartLinks(xadd,yadd,xmin,ymin)
                ConvertsteptoRRTstar(xadd,yadd,xmin,ymin)
                        
                displayimage()
                #print("here",(yadd,xadd),count,min,img[xadd,yadd])
                if(img[xadd,yadd]==endcolor and xadd>500 and yadd>500):     #check condition
                    print("reached")
                    break
                img[xadd,yadd]=170          #170 is just being used as a colour to denote the traversed path
                
                count+=1
    ##end of traversing

    ##path tracking give i = count as arguement
    #print(path)
    #cv2.waitKey(0)
    pathneighbours(xadd,yadd,count)
    print(count2,"total steps")

#end = time.time()
#print(end-begin)

if __name__=="__main__":
    Main()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
