import numpy as np

a=[1,2,3,4,5]
c=[[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]

r=16

b=np.cumsum(c)

print(b)

for i, x in enumerate(b):
    if x >= r:
        break
print(i)