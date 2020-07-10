# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:47:27 2018

@author: ChristineB.local

Description:

This script calculates a RADIAL DISTRIBUTION at a certain time.
The procedure is based on the paper of Pereira, 2017 : Segregation Particles
Shape

This script can be run once the data has been read. You have to enter the right arrays
of positions at the beginning. So this script can be used with Grains3D OR LIGGGHTS

Arrays in this script:

count : nb pf particles of each type in each annulus
      annulus1 annulus2 annulus3...
type1  nbPart   nbPart
type2

distribution : volume of each type and total volume and ratios in each annulus
               annulus1 annulus2 annulus3 ...
type1            vol1
type2            vol2
totalVolume   vol1+vol2
ratio1         vol1/tot
ratio2         vol2/tot
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

 

"Convert the cartesian coordinates in radial coordinate"
r1 = radialPos[boolType1]
r2 = radialPos[boolType2]

"Count how many particles of each type in each annulus"
count = np.zeros((nbType, nbAnnuli), dtype=int)
for radialPosition in range(nbAnnuli):
    lowLimit = radialPosition * annulusWidth
    highLimit = (radialPosition+1) * annulusWidth
    for atom1 in r1: #TYPE 1
        if (atom1 >= lowLimit) & (atom1 < highLimit):
            count[0, radialPosition] = count[0, radialPosition] + 1
    for atom2 in r2: #TYPE 2
        if (atom2 >= lowLimit) & (atom2 < highLimit):
            count[1, radialPosition] = count[1, radialPosition] + 1
print ("")
print ("The counts of particles of each type (lines) in each annulus (column) are:")
print count
            
"Calculate the volumes of each particle in each annulus and the ratio"
distribution = np.zeros(((nbType*2)+1, nbAnnuli), dtype=float)
distribution[0,:] = count[0,:] * volume1 #volume of type1
distribution[1,:] = count[1,:] * volume2 #volume of type 2
distribution[2,:] = distribution[0,:] + distribution[1,:] #total volumes
distribution[3,:] = distribution[0,:]/distribution[2,:] #ratio of type1
distribution[4,:] = distribution[1,:]/distribution[2,:] #ratio of type2
print distribution
distributionType1 = distribution[3,:] 
distributionType2 = distribution[4,:] 

"Plot the radial distribution versus the scaled radius"
"Control of sizes in all the file"
SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig = plt.figure() 
plt.plot(scaledRadius, distributionType1, marker = 'o', color = 'b', label = 'Type 1') 
plt.plot(scaledRadius, distributionType2, marker = 'o', color = 'r', label = 'Type 2')        
plt.xlabel('Scaled Radius ($r/R_{drum}$)')
plt.ylabel('Radial Distribution')
plt.legend(loc = 0, numpoints = 1)
plt.xlim(0,1)
plt.ylim(0,1)


    

        
            
        
    