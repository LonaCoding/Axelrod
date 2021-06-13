import numpy as np
import math

def largestFactor(inputValue):
    n=1
    factors=[]
    a=1
    b=1
    while n <=math.sqrt(inputValue): #only look for factors up to square root
        if inputValue%n==0: #if factor found    
            a=n #put factor in list
        n=n+1
            
    #find middle vector
    #print(factors)
    #halfLen=math.floor(len(factors)/2) #should be ceil, but because using arrazy index that starts at 0
    #print(halfLen)
    #a=int(factors[halfLen])
    b=int(inputValue/a)

    return a, b

a=[1,2,3,4,5]
c=[[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]

r=16

#b=np.cumsum(c)

#print(b)

#for i, x in enumerate(b):
#    if x >= r:
#        break
#print(i)


a,b=largestFactor(3) #1,2,3,5,6,10,15,30
#print(a)
#print(b)

q,r =divmod(2,5)
#print(q)
#print(r)

a=0/10
print(a)