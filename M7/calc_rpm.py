import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np


def calculate_rpm(mcp_values, totalTime):

    # True - looking for light
    # False - looking for dark
    direction = True
    
    avgMCP = sum(mcp_values)/len(mcp_values)
    transitions = 0
    print(avgMCP)
    for i in range(0, len(mcp_values)):
        
        if mcp_values[i] > avgMCP and direction:
            transitions += 1
            direction = False


        elif mcp_values[i] < avgMCP and not direction:
            transitions += 1
            direction = True

    
    average_rpm = ((transitions/4) / totalTime) * 60
    return transitions, average_rpm

duty = input('Duty used: ')
fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)

MCP = [0]*MAXSIZE
time = [0]*MAXSIZE

i=0
for dat in data:
    values   = dat.split()          
    
    MCP[i]  = float(values[1])
    time[i] = float(values[0])

    i = i + 1


elasped = time[len(time) - 1]

transitions, rpm = calculate_rpm(MCP, elasped)

print(f'Transitions: {transitions}\t RPM: {rpm}\n')

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

plt.plot(time, MCP, 'r')
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Value')
plt.legend(["ADC - Bits"], loc="upper right")

photo = f"photo_DC_{duty}.png"
plt.savefig(photo)

