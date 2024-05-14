matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False                     # For printing debug statements

time    = [0]*MAXSIZE
dist    = [0]*MAXSIZE
MA_dist = [0]*MAXSIZE

i=0
for dat in data:
    values     = dat.split()          # split on white space
    time[i]    = float(values[0])     # first item in file is time
    dist[i]    = float(values[1])     # second is the value
    MA_dist[i] = float(values[2])     # third is the moving average
    if DEBUG: print (f'{i}\t{time[i]}\t{dist[i]}')
    i = i + 1

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

# Both on one Graph
plt.plot(time, dist, label="dist")
plt.plot(time, MA_dist, label="MovAvg")
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Distance in CM, Moving Average in CM')
plt.savefig('distance.png')
# I wanted to show the labels, but didn't get it, if you figure it out
# let me know ;)

# Two graphs on same page
plt.clf()                           # start new plot
plt.figure()
plt.subplot(211)
plt.grid()                          # show the grid
plt.plot(time, dist)
plt.ylabel('Distance in CM')
plt.subplot(212)
plt.plot(time, MA_dist)
plt.grid()                          # show the grid
plt.ylabel('Moving Average in CM')
plt.xlabel('time - sec')
plt.savefig("Distance_MovingAvg.png")
