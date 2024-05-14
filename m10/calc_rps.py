import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np


def calculate_rps(mcp_values, totalTime):

    # True - looking for light
    # False - looking for dark
    direction = True
    
    avgMCP = sum(mcp_values)/len(mcp_values)
    transitions = 0
    
    for i in range(0, len(mcp_values)):
        
        if mcp_values[i] > avgMCP and direction:
            transitions += 1
            direction = False


        elif mcp_values[i] < avgMCP and not direction:
            transitions += 1
            direction = True

    
    average_rps = ((transitions/4) / totalTime) 
    return transitions, average_rps

fname   = f'data_9c.txt'
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)


MCP = [0]*MAXSIZE
time = [0]*MAXSIZE

i=0
for dat in data:
    values   = dat.split()          
    
    time[i] = float(values[0])
    MCP[i]  = float(values[3])

    i = i + 1


elasped = time[len(time) - 1]
 
transitions, rps = calculate_rps(MCP, elasped)

# print(f'RPS: {rps}\n')

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

plt.plot(time, MCP, 'r')
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Value')
plt.legend(["ADC - Bits"], loc="upper right")

photo = f"plot_9c.png"
plt.savefig(photo)

