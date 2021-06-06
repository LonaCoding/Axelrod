import numpy as np

def takeSecond(elem):
    return elem[2]

a=[1,2,3,4]
b=[5,3,4,2]
#x = np.array([3, 5, 7])
x=np.array(a)
#y = np.array([5, 7, 9])
y=np.array(b)
st=np.dstack((x,y))
print(st)
lst=list(st)
print("sort by col 2")
#sor=np.sort(st,axis=1)
sor=lst.sort(key=takeSecond)
print(sor)
#print("tuple")
#t=(a,b)
#print(t)