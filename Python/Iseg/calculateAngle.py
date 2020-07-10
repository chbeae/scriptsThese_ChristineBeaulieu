# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:02:34 2017

@author: Christine Beaulieu
Description du code:
Ce code 
-    trouve l'angle dynamique d'un rotary drum en roulement à un certain temps
     de simulation
-    *** ce code est appelé par le code diffusionCoeff
-   il ne peut pas être roulé seul, car il a besoin de variables dans
    le premier code main
- l'angle donné est celui formé entre l'horizontale et la pente
************************************************************************
Geometry : Cylindre rotatif (horizontal)
***********************************************************************
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

"Variables for the symmetry"
nbPlanesY = 5
nbPointsX = 8
middle = maxY/2

turn = 1
dynamicAngle = np.array([])
     
for y in np.linspace(0, maxY, nbPlanesY):
    #print ""    
    #print "PLANE %d : y = %.2f m." %(turn, y)
    zFit = np.array([])
    booleanY = (positionxyz[:,1] > (y - maxRadius)) & \
        (positionxyz[:,1] < (y + maxRadius))
    minXPlane = min(positionxyz[:,0][booleanY])
    maxXPlane = max(positionxyz[:,0][booleanY])
    xFit = np.array([])
    for x in np.linspace(minXPlane, maxXPlane, nbPointsX)[1::]: #exclude the first point where particles are lower
        #Select the data that correspond to this filter
        booleanX = (positionxyz[:,0] > (x - maxRadius)) & \
        (positionxyz[:,0] < (x + maxRadius))
        boolean = booleanX & booleanY
        if sum(boolean)!=0:        
            dataSelected = positionxyz[boolean]
            zMax = max(dataSelected[:,2])
            zFit = np.append(zFit, zMax)
            xFit = np.append(xFit,x)
        #print "For x = %.2f m and y = %.2f m, there are %d particles." \
        #%(x,y,sum(boolean))
        #print "The maximum heigth (z) for this zone is %.2f m." \
        #%(zMax)
        
    out = np.polyfit(xFit, zFit, 1)	
    slope = out[0]
    angle = math.atan(slope) #in rad
    angle = math.degrees(angle) #in degrees    
    dynamicAngle = np.append(dynamicAngle, angle)
    
    #print "The dynamic angle of repose for PLANE %d is %.1f degrees." %(turn, angle)
    turn = turn + 1
    
meanDynAngle = np.mean(dynamicAngle)
angleVector = np.append(angleVector, meanDynAngle)

if (index != 0):
    differenceBetweenAngles = np.abs(meanDynAngle - angleVector[index-1])
    angleDifference = np.append(angleDifference, differenceBetweenAngles)
    if (differenceBetweenAngles < 1):
        criterionAngle = criterionAngle + 1
    else:
        criterionAngle = 0 #to have 5 values under 1 in a row

print ""
print "The dynamic angles calculated are", dynamicAngle
print ""
print "The mean dynamic angle is %.1f degrees." %(meanDynAngle)
print ""
 
#"Plot the angle versus the length of the drum"
#colors=['b', 'g', 'r', 'c', 'm', 'k', 'y','b', 'g', 'r', 'c', 'm']
#symbs=['o', 'v', 's', 'p', 'D', '^', '1','o', 'v', 's', 'p', 'D', '^', '1']
#
#fig=plt.figure()
#plt.plot(np.linspace(0, maxY, nbPlanesY), -dynamicAngle, marker = 'o')    
#plt.xlabel('Position in y on the drum (m)')
#plt.ylabel('Dynamic angle (degrees)')
#plt.ylim(0,100) 
 
#"What is the slope of the perpendicular line?"
#slopePerp = -1.0/slope 
#print ""
#print "The direction that is perpendicular to the surface follows the equation of the line : z = %.2fx." %(slopePerp)