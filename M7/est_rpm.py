from scipy.fftpack import fft
import matplotlib
matplotlib.use('Agg')       # to avoid warnings if using ssh
import matplotlib.pyplot as plt
import numpy as np

N = 512                     # number of samples

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)

MCP = [0]*MAXSIZE
t = [0]*MAXSIZE

i=0
for dat in data:
    values   = dat.split()          
    
    MCP[i]  = float(values[1])
    t[i] = float(values[0])

    i = i + 1

T = t[1]

fixedMCP = MCP - np.mean(MCP)

fftMCP = fft(fixedMCP)

index = np.argmax(2/N*np.abs(fftMCP[0:N//2]))

freq = np.linspace(0, 1/(2*T), N//2)
RPM = freq[index]
print(f'Highest Freq: {RPM}')
plt.plot(freq, 2/N*np.abs(fftMCP[0:N//2]))
plt.grid(True)
plt.ylabel("Amplitude")
plt.xlabel("freq - Hz")
plt.savefig("fft.png")