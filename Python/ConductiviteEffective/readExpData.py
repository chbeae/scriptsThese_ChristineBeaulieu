# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 11:15:58 2020

This script aims to read the experimental data of temperatures to be able
to run the script calculateKeff_erf next.
 This script needs a .csv file with the columns :
 
 Time (s)  Thermo1 (C)  Thermo2 (C)  Thermo3 (C)   Thermo4 (C)

@author: ChristineB.local

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

"Get the experimental data"
donnees = np.loadtxt ("verre10_2essai_20191108_132751_4000s.csv", skiprows = 1, unpack = False, delimiter = ';')

print ("")
print ("There are %d rows in that file.") %len(donnees)
firstTimeStep = 0
nbPointsStudied = int(raw_input("How many points (timesteps) do you want to calculate? "))
indexVector = np.round(np.linspace(firstTimeStep,len(donnees)-1,nbPointsStudied, dtype = 'int'))


timeVector = donnees[:,0][indexVector]
tableTemperaturesCelsius = donnees[:,1::][indexVector]
tableTemperaturesCelsius = np.transpose(tableTemperaturesCelsius)

print ("")            
print ("Info on the thermocouples.")
nbThermo = len(donnees[0]) - 1
print ("There are %d thermocouples.") %nbThermo
zVector = np.array([])
for jjg in range(nbThermo):
    print ("Thermocouple %d") %(jjg+1)
    distanceThermo = float(raw_input("What is the distance of the thermocouple from the top (in m)? "))
    zVector = np.append(zVector, distanceThermo)
    print ("")
    print zVector
    
"Plot the results"
"Control of sizes in all the file"
SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
fig = plt.figure()
ax = plt.subplot(111)
colors=['orange','b', 'g', 'r', 'c', 'm', 'k', 'y','b', 'g', 'r', 'c', 'm']
symbs=['o', 'v', 's', 'p', 'D', '^', '1','o', 'v', 's', 'p', 'D', '^', '1']
for i in range(nbThermo):
    plt.plot(donnees[:,0], donnees[:,i+1], marker='o', color=colors[i], label= 'Thermo %d (z=%.3f m)' %((i+1),zVector[i]))
    #plt.plot(timeVector, tableTemperaturesCelsius[i,:], marker=symbs[i], color='r', linestyle='-') 
plt.legend(loc = 0, numpoints = 1)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))


