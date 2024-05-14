from scipy.fftpack import fft
import matplotlib
matplotlib.use('Agg')       # to avoid warnings if using ssh
import matplotlib.pyplot as plt
import numpy as np
import math
import mod8_func as motor

N = 512                     # number of samples

fname   = f'data_9c_mock.txt'
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = 2**(math.floor(np.log2(len(data))) + 1)

MCP = [0]*MAXSIZE
t = [0]*MAXSIZE
differences = [0]*MAXSIZE
moving = [0]*MAXSIZE

i = 0
for dat in data:
    values   = dat.split()           
    t[i] = float(values[0])
    MCP[i]  = float(values[1])
    if i > 0:
        difference = MCP[i] - MCP[i-1]

        if difference < 90 and difference > -90:
            differences[i] = difference
            moving[i] = motor.movingAvg(differences,i)
    i += 1

T = t[1]
print(t[0])
fixedMCP = differences - np.mean(moving)
print(fixedMCP[1])

fftMCP = fft(differences)

index = np.argmax(2/N*np.abs(fftMCP[0:N//2]))

freq = np.linspace(0, 1/(2*T), N//2)
RPS = freq[index]
print(f'Highest Freq: {RPS}')
plt.plot(freq, 2/N*np.abs(fftMCP[0:N//2]))
plt.grid(True)
plt.ylabel("Amplitude")
plt.xlabel("freq - Hz")
plt.savefig("fft_9c_mock.png")