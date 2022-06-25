import cv2
import numpy as np
import math
import time

##Global variables 
path=[]
img = cv2.imread('task3.1.png', 0)
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

##distance between two points
def dist(x1,y1,x2,y2):
    k1 = (x1-x2)*(x1-x2)
    k2 = (y1 - y2) * (y1 - y2)
    u = (k1+k2)     #no need of square root
    u=math.sqrt(u)
    return u

def addcoordinate(xmin,ymin,xrand,yrand):
    if(xrand>xmin):
        xadd=xmin+1
    elif(xrand<xmin):
        xadd=xmin-1
    else:
        xadd=0
    if(yrand>ymin):
        yadd=ymin+1
    elif(yrand<ymin):
        yadd=ymin-1
    else:
        yadd=0
    return(xadd,yadd)

def displayimage():
    cv2.imshow('Image', img.astype(np.uint8))
    cv2.waitKey(5)



#create a main function and initialize i1,j1 as starting point
count=0
(xadd,yadd)=(a,b)
while (True) :
    xrand = np.random.randint(0, n)
    yrand = np.random.randint(0, m)
    print(xrand,yrand)
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
        if(img[xadd,yadd]!=255 and xadd>0 and yadd>0):
            
            path.append((xadd,yadd))
                     #170 is just being used as a colour to denote the traversed path
            displayimage()
            print("here",(yadd,xadd),count,min,img[xadd,yadd])
            if(img[xadd,yadd]==endcolor and xadd>500 and yadd>500):     #check condition
                print("reached")
                break
            img[xadd,yadd]=170 
            
            count+=1









#end = time.time()
#print(end-begin)
cv2.waitKey(0)
cv2.destroyAllWindows()