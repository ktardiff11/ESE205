import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np
import argparse


gain = str(input('open_loop, kp_equal, kp_half, kp_2x, kp_10x: '))
fname   = f'data_' + gain +'.txt'
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 


MAXSIZE = len(data)
RPS = [0]*MAXSIZE
time = [0]*MAXSIZE

for i in range(0, MAXSIZE):

    values  = data[i].split()          
    time[i] = float(values[0])
    RPS[i]  = float(values[3])


# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

plt.plot(time, RPS, 'r')
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Value')
plt.legend(["RPS"], loc="upper right")



photo = f'plot_' + gain + '.png'
plt.savefig(photo)

