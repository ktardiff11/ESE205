import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)


ultra = [0]*MAXSIZE

ax   = [0]*MAXSIZE
ay   = [0]*MAXSIZE
az   = [0]*MAXSIZE

gx   = [0]*MAXSIZE
gy   = [0]*MAXSIZE
gz   = [0]*MAXSIZE

time = [0]*MAXSIZE

i=0
for dat in data:
    values   = dat.split()          
    ultra[i]  = float(values[0])

    ax[i] = float(values[1])
    ay[i] = float(values[2])
    az[i] = float(values[3])

    gx[i] = float(values[4])
    gy[i] = float(values[5])
    gz[i] = float(values[6])

    time[i] = float(values[7])

    i = i + 1

fig, axs = plt.subplots(3)
fig.suptitle('Ultrasonic, Accelerometer, Gyrometer')
axs[0].plot(time, ultra, label="Distance")
axs[0].legend(loc="upper right")
# axs[0].xlabel('time -sec')
# axs[0].ylabel('distance')

axs[1].plot(time, ax, color="orange", label="Ax")
axs[1].plot(time, ay, color="red", label="Ay")
axs[1].plot(time, az, color="blue", label="Az")
axs[1].legend(loc="upper right")
# axs[1].xlabel('time -sec')
# axs[1].ylabel('a vals')


axs[2].plot(time, gx, color="orange", label="Gx")
axs[2].plot(time, gy, color="red", label="Gy")
axs[2].plot(time, gz, color="blue", label="Gz")
axs[2].legend(loc="upper right")
# axs[2].xlabel('time -sec')
# axs[2].ylabel('a vals')


fig.savefig('plotWalk.png')
