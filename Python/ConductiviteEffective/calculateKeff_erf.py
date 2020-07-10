# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:21:02 2020

@author: ChristineB.local

This script aims to calculate keff in transient mode with the erf
function

This script must be ran AFTER evolutionTemperatureHeights
"""

import numpy as np
from scipy import special
import matplotlib.pyplot as plt

T0 = float(raw_input("What is the intial temperature? (in C) : "))
T1 = float(raw_input("What is the top temperature? (in C) : "))
kp = float(raw_input("What is the particle conductivity? (in W/m.K) : "))
Cp = float(raw_input("What is the particle heat capacity? (in J/kg.K) : "))
eps = float(raw_input("What is the porosity? : "))
rhop = float(raw_input("What is the particle density? (in C) : "))
kf = float(raw_input("What is the fluid conductivity? (in W/m.K) : "))

nbThermo = nbThermo

modifiedTimeVector = 2.0*np.sqrt(timeVector)


xVectors = np.zeros((nbPointsStudied,nbThermo))
for thermo in range(nbThermo):
    xVectors[:,thermo] = zVector[thermo]/modifiedTimeVector
    
tempVectors = np.zeros((nbPointsStudied,nbThermo))
for thermo in range(nbThermo):
    temp = 1.0 - ((tableTemperaturesCelsius[thermo,:] - T0) / (T1-T0))
    temp = special.erfinv(temp)
    tempVectors[:,thermo] = temp
    
#Find when it's not "inf"
for indexValue, value in enumerate(reversed(tempVectors[:,nbThermo-1])): #last thermocouple
    if value == float('inf'):
        print indexValue
        print indexValue
        break
indexValue = nbPointsStudied - indexValue
    
#Find the slopes of the n curves
slopes = np.zeros(nbThermo)
intercepts = np.zeros(nbThermo)
for thermo in range(nbThermo):
    coeff = np.polyfit(xVectors[indexValue::,thermo],tempVectors[indexValue::,thermo],1)
    slopes[thermo] = coeff[0]
    intercepts[thermo] = coeff[1]

fig = plt.figure()    
for thermo in range(nbThermo):
    plt.plot(xVectors[indexValue::,thermo],tempVectors[indexValue::,thermo], marker = 'o', label= 'Thermo %d (z=%.3f m)' %((thermo+1),zVector[thermo]))
    plt.plot(xVectors[indexValue::,thermo], slopes[thermo]*xVectors[indexValue::,thermo]+intercepts[thermo])
    pos = 0.3 - (thermo*0.05)
    plt.figtext(0.4, pos, "y=%.1fx+%.3f " %(slopes[thermo], intercepts[thermo]))
plt.legend(loc = 0, numpoints = 1)
plt.xlabel('$\\frac{2}{2rac(t)}$')
plt.ylabel('$erf^{-1}(1-\\theta)$')
plt.subplots_adjust(bottom=0.20)
 

#Calculate keff
meanSlope = np.mean(slopes)

keff = ((1.0/meanSlope)**2) * rhop * Cp * (1-eps)
keffkf = keff/kf
logkpkf = np.log10(kp/kf)

print ("")
print ("log(kp/kf) is %.2f") %logkpkf
print ("keff/kf is : %.2f") %keffkf
    
 

