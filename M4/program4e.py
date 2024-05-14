import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)

raw    = [0]*MAXSIZE
movingAverage   = [0]*MAXSIZE
time = [0]*MAXSIZE

i=0
for dat in data:
    values   = dat.split()          # split on white space
    raw[i]  = float(values[0])     # first item in file is time
    movingAverage[i] = float(values[1])       # second is the value
    time[i] = float(values[2])
    i = i + 1

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

plt.plot(time, raw, 'r')
plt.plot(time, movingAverage, 'b')
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Value')
plt.legend(["Raw Data","Moving Average"],loc="upper right")
plt.savefig('plotAccel.png')
