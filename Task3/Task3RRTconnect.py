import cv2
import numpy as np
import math
import time

##Global variables 
path1=[]
path2=[]
img = cv2.imread('task3.1.png', 0)
img2=cv2.imread('task3.1.png', 0)
(m, n) = (img.shape)
a, b = (45, 50)
c, d = (545,550)
endcolor=82     #start
##

##Thresholding
for q in range(m):
    for r in range(n):
        if(img[q,r]<10):
            img[q,r]=0
        elif(img[q,r]>245):
            img[q,r]=255
        elif(img[q,r]>115 and img[q,r]<150):
            img[q,r]=134
        elif(img[q,r]>70 and img[q,r]<95):
            img[q,r]=endcolor
##

##initialization
img[a, b] = 170
img[c, d] = 170
path1.append((a,b))
path2.append((c,d))
print(a,b)
print(c,d)
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
def pathneighbors(x,y,i,path):
    global count2
    
    #print("here")
    neighbors=neighbourInPathPixelsList(x,y)
    #print(neighbors)
    j=0
    for p in path[i::-1]:
        j+=1
        if p in neighbors:
            if(p==(a,b)):
                print("reached start")
                return
            img2[p]=250
            cv2.imshow('Image2', img2.astype(np.uint8))
            cv2.waitKey(5)
            print(p)
            (x,y)=p
            count2+=1
            print("i,j = ", i, j)
            pathneighbors(x,y,i-j,path)

def neighbourInPathPixelsList(x,y):
    neighbors=[]
    for cord1 in range (-4,5,4):
        for cord2 in range (-4,5,4):
            if(img[cord1+x,cord2+y]==170 and (cord1,cord2)!=(0,0)):
                neighbors.append((x+cord1,y+cord2))                 ##will find all the neighbors in the path
    return(neighbors)


##create a main function and initialize a,b as starting point
count2=0
def Main():
    counta=0
    countb=0
    (x1add,y1add)=(a,b)
    (x2add,y2add)=(c,d)
    while (True) :
        x1rand = np.random.randint(0, n)
        y1rand = np.random.randint(0, m)
        x2rand = np.random.randint(0, n)
        y2rand = np.random.randint(0, m)
        print((x1rand,y1rand),(x2rand,y2rand))
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
            if(img[x1add,y1add]!=255 and x1add>0 and y1add>0 and x1add<600 and y1add<600):
                
                path1.append((x1add,y1add))
                        
                displayimage()
                print("here",(y1add,x1add),counta,min,img[x1add,y1add])
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
            if(img[x2add,y2add]!=255 and x2add<600 and y2add<600 and x2add>0 and y2add>0):
                
                path2.append((x2add,y2add))
                        
                displayimage()
                print("here",(y2add,x2add),countb,min,img[x2add,y2add])
                if (x2add,y2add) in path1:     #check condition2
                    (xend,yend)=(x2add,y2add)
                    print("reached")
                    break
                img[x2add,y2add]=170 #170 is just being used as a colour to denote the traversed path
                
                countb+=1
    ##end of traversing

    ##path tracking give i = count as arguement
    
    pathneighbors(xend,yend,counta,path1)
    pathneighbors(xend,yend,countb,path2)
    print("connecting point=",(yend,xend))      ##to spot in inage, given as (y,x)
    print(count2,"total steps")

#end = time.time()
#print(end-begin)

if __name__=="__main__":
    Main()
    cv2.waitKey(0)
    cv2.destroyAllWindows()