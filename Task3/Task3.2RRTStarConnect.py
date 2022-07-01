import cv2
import numpy as np
import math
import time

##Global variables 
path1=[]
path2=[]
img = cv2.imread('task3.2.png', 0)
img2=cv2.imread('task3.2.png', 0)
(m, n) = (img.shape)
a, b = (56, 52)
c, d = (516,616)
endcolor=82     #start
totalRRTStarchanges=0
##

##Thresholding
for i in range(m):
    for j in range(n):
        if(img[i,j]<10):
            img[i,j]=0
        elif(img[i,j]>220):
            img[i,j]=255
        elif(img[i,j]>115 and img[i,j]<150):
            img[i,j]=134
        elif(img[i,j]>70 and img[i,j]<95):
            img[i,j]=endcolor
##

##initialization
img[a, b] = 170
img[c, d] = 170
path1.append((a,b))
path2.append((c,d))
print(a,b)
print(c,d)
print(img.shape)
#time.sleep(5)

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

tracepathcount=0
##Reccursive function that traverses the list once to find the ultimate path
def pathneighbours(x,y,i,path):
    global count2,tracepathcount
    
    #print("here")
    neighbours=neighbourInPathPixelsList(x,y)
    #print(neighbors)
    j=0
    for p in path[:i]:
        j+=1
        if p in neighbours:
            if(p==(a,b) or p==(c,d)):
                print("reached an end")
                time.sleep(1)
                tracepathcount+=1
                return
            
            img2[p]=250
            cv2.imshow('Image2', img2.astype(np.uint8))
            cv2.waitKey(5)
            #print(p)
            (x,y)=p
            count2+=1
            #print("i , j = ", i, j)
            pathneighbours(x,y,j,path)
            if(tracepathcount>0):
                return


def neighbourInPathPixelsList(x,y):
    neighbours=[]
    for cord1 in range (-4,5,4):
        for cord2 in range (-4,5,4):
            if(img[cord1+x,cord2+y]==170 and (cord1,cord2)!=(0,0)):
                neighbours.append((x+cord1,y+cord2))                 ##will find all the neighbors in the path
    return(neighbours)

def neighbourInPathPixelsListBigrange(x,y,path):
    neighbours=[]
    for cord1 in range (-8,9,4):
        for cord2 in range (-8,9,4):
            if((cord1+x,cord2+y) in path):
                neighbours.append((x+cord1,y+cord2))                 ##will find all the neighbors in the path
    return(neighbours)


def newStartLinks(xnew,ynew,minx,miny,path):
    mindist=dist(minx,miny,xnew,ynew)
    (minNx,minNy)=(minx,miny)
    neighbors=neighbourInPathPixelsListBigrange(xnew,ynew,path)
    for (xneigh,yneigh) in neighbors:
        if(dist(xneigh,yneigh,xnew,ynew)<mindist):
            print("yes it got changed",(xnew,ynew))         ##almost no change is happening every time. Suggests that initial dist is mindist nearly all the time
            mindist=dist(xneigh,yneigh,xnew,ynew)
            (minNx,minNy)=(xneigh,yneigh)
    
            
    ind=path.index((minNx,minNy))
    path.insert(ind+1,(xnew,ynew))
    return(minNx,minNy)

                                                                                  ##neighbours
def ConvertsteptoRRTstar(x,y,xorigin,yorigin,path):                             #       #       #
    global totalRRTStarchanges
    neighbours=neighbourInPathPixelsListBigrange(x,y,path)                                   
    costNeighbour=[]                                                   #(origin)#------>#       #
    for particularNeighbour in neighbours:                                           #(x,y)

        cost=0                                                                  #       #       #
        (intermediateNodex,intermediateNodey)=(xorigin,yorigin) 
        #print("Origin index:",path.index((xorigin,yorigin)),"particularNeighbour index:",path.index(particularNeighbour))                                               
        for p in path[path.index((xorigin,yorigin)):]:
            if(p in neighbours):                                               #only cost to elements in the path coming after the origin will be found
                if(p!=particularNeighbour):
                    (x1,y1)=p
                    #print("adding distance")
                    cost+=dist(x1,y1,intermediateNodex,intermediateNodey)       #x1,y1 made to pass p as arguement into dist function
                    (intermediateNodex,intermediateNodey)=p
                elif(p==particularNeighbour):
                    (x1,y1)=p
                    cost+=dist(x1,y1,intermediateNodex,intermediateNodey)       
                    #print("COST:",cost)
                    costNeighbour.append((neighbours.index(particularNeighbour),cost))  
                    break
    #found cost to nodes in neighbourhood (reference origin)
    #now making necessary changes
    OriginToCenter=dist(xorigin,yorigin,x,y)
    #print(OriginToCenter)          #?? why is this constant and equal to 5.5...
    for node in costNeighbour:
        (x1,y1)=neighbours[node[0]]
        
        CenterToNode=dist(x1,y1,x,y)                            #since 0 contains index of neighbour and 1 contains cost of neighbour
        if((x1,y1)!=(xorigin,yorigin)):
            print(node[1],OriginToCenter+CenterToNode,neighbours[node[0]])
            #time.sleep(0.1)
        if (node[1]>OriginToCenter+CenterToNode):
            print("i'm changing")
            totalRRTStarchanges+=1
            #path.remove((intermediateNodex,intermediateNodey))      ##removing old conneciton
            path.insert(path.index((x,y)),(x1,y1))            ##adding new connection
            #path.insert(path.index((x1,y1)),(intermediateNodex,intermediateNodey))      ##adding back the old node to path but without connection to the next node

            



##create a main function and initialize a,b as starting point
count2=0
def Main():
    global tracepathcount
    counta=0
    countb=0
    (x1add,y1add)=(a,b)
    (x2add,y2add)=(c,d)
    while (True) :
        x1rand = np.random.randint(0, m-1)
        y1rand = np.random.randint(0, n-1)
        x2rand = np.random.randint(0, m-1)
        y2rand = np.random.randint(0, n-1)
        #print((x1rand,y1rand),(x2rand,y2rand))
        min=100000
        #checking that it is a valid path
        if (img[x1rand,y1rand] == 0 or img[x1rand,y1rand]==82):    
            ##finds the nearest node in the tree to the random point
            for (x,y) in path1:
                #print(dist(x, y, xrand, yrand))
                if (dist(x, y, x1rand, y1rand) < min):
                    min = dist(x, y , x1rand, y1rand)
                    xmin=x
                    ymin=y
                    
            (x1add,y1add)=addcoordinate(xmin,ymin,x1rand,y1rand)
            if(img[x1add,y1add]!=255 and x1add>0 and y1add>0 and x1add<582 and y1add<660):
                
                (xmin,ymin)=newStartLinks(x1add,y1add,xmin,ymin,path1)
                ConvertsteptoRRTstar(x1add,y1add,xmin,ymin,path1)
                        
                displayimage()
                #print("here",(y1add,x1add),counta,min,img[x1add,y1add])
                if (x1add,y1add) in path2:     #check condition
                    (xend,yend)=(x1add,y1add)
                    print("reached")
                    break
                img[x1add,y1add]=170 #170 is just being used as a colour to denote the traversed path
                
                counta+=1

        min=100000
        if (img[x2rand,y2rand] == 0 or img[x2rand,y2rand]==82):                 ###redundant code, make function###
            ##finds the nearest node in the tree to the random point
            for (x,y) in path2:
                #print(dist(x, y, xrand, yrand))
                if (dist(x, y, x2rand, y2rand) < min):
                    min = dist(x, y , x2rand, y2rand)
                    xmin=x
                    ymin=y
                    
            (x2add,y2add)=addcoordinate(xmin,ymin,x2rand,y2rand)
            if(img[x2add,y2add]!=255 and x2add<582 and y2add<660 and x2add>0 and y2add>0):
                
                (xmin,ymin)=newStartLinks(x2add,y2add,xmin,ymin,path2)
                ConvertsteptoRRTstar(x2add,y2add,xmin,ymin,path2)
                        
                displayimage()
                #print("here",(y2add,x2add),countb,min,img[x2add,y2add])
                if (x2add,y2add) in path1:     #check condition2
                    (xend,yend)=(x2add,y2add)
                    print("reached")
                    break
                img[x2add,y2add]=170 #170 is just being used as a colour to denote the traversed path
                
                countb+=1
    ##end of traversing

    ##path tracking give i = count as arguement
    
    pathneighbours(xend,yend,counta,path1)
    tracepathcount=0
    pathneighbours(xend,yend,countb,path2)
    print("connecting point=",(yend,xend))      ##to spot in inage, given as (y,x)
    print(count2,"total steps")
    
    print("total Changes due to RRTStar: ",totalRRTStarchanges)
    

#end = time.time()
#print(end-begin)

if __name__=="__main__":
    Main()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
