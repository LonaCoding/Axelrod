import matplotlib.pyplot as plt
import numpy as np
import shutil

# First create some toy data:
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

a=3
b=3

subplotFileName="plotTest7.png"
targetOutFolder = "testPlotsGen"


# Create four polar axes and access them through the returned array
#fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
fig, axs = plt.subplots(a, b)
print(axs[1][1])

#     0   :   1
#-----------------
#0 | 0,0  :  0,1
#1 | 1,0  :  1,1

for ax in range(a):
    for by in range(b):
        y=y+1 #proof iteration works
        axs[ax][by].plot(x, y)

#axs[0][0].plot(x, y)
#axs[1][0].plot(x, y)
#axs[1][1].scatter(x, y)
plt.suptitle("a test plot\nNumber 7")
plt.savefig(subplotFileName,format='PNG', dpi=100) #saves the plot as image
outputNewPath = shutil.move(subplotFileName, targetOutFolder) #move the saved image plot to output fold
