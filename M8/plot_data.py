import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--plot', type=float, default=5)
args = parser.parse_args()

duty = input('Duty used: ')
fname   = f'data_PWM_' + duty +'.0.txt'
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 


length = 0

for i in range(0,len(data)):
    vals = data[i].split()
    if float(vals[0]) >= args.plot:
        length = i
        break

MAXSIZE = length
RPS = [0]*MAXSIZE
time = [0]*MAXSIZE
print(MAXSIZE)

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

photo = f"velocityplot.png"
plt.savefig(photo)

