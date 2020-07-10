# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:21:55 2018

@author: ChristineB.local

Description:

This code stores the temperature measured by thermocouples at different heights 
in a horizontal drum.
The temperatures are stored in an array named tableTemperatures that must have
been initialized before. This array is constructed as:
              time1  time2  time3  time4 ... nbFiles
     thermo1
     thermo2
     thermo3
     ...
     nbThermocouples
     
You can choose here if you want a temperature averaged on mass, volume or number
     
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

"""
"CUBE around the thermocouple of size = 2*surplus"
surplus = 1*maxRadius # gap around the studied position
xStudied = boxSize/2
yStudied = boxSize/2

"Find the position"
booleanXtemp = (positionxyz[:,0] > (xStudied - surplus)) & \
        (positionxyz[:,0] < (xStudied + surplus))
booleanYtemp = (positionxyz[:,1] > (yStudied - surplus)) & \
        (positionxyz[:,1] < (yStudied + surplus))

for number, zStudied in enumerate(heightsVector):
    booleanZtemp = (positionxyz[:,2] > (zStudied - surplus)) & \
        (positionxyz[:,2] < (zStudied + surplus))
    booleanTotaltemp = booleanXtemp & booleanYtemp & booleanZtemp
    nbPartZone = sum(booleanTotaltemp)
    if nbPartZone != 0:
        print ("There is/are %d particles in that zone.") %nbPartZone
        tempZone = temp[booleanTotaltemp]
        tempLocal = tempZone
        execfile("calculateMeanTemp.py")
        tempDesired = meanTvolume #could change for meanT, meanTvolume OR meanTmass
        tableTemperatures[number,index] = tempDesired
    else:
        print ("There is no particle selected at z=%.4f") %zStudied
        tableTemperatures[number,index] = np.nan

"""       

"*****************************************************************************"        
"All the particles on the same heigth +/- surplus"
"Find the position"

surplus = maxRadius

for number, zStudied in enumerate(heightsVector):
    booleanZtemp = (positionxyz[:,2] > (zStudied - surplus)) & \
        (positionxyz[:,2] < (zStudied + surplus))
    booleanTotaltemp = booleanZtemp
    nbPartZone = sum(booleanTotaltemp)
    if nbPartZone != 0:
        print ("There is/are %d particles in that zone.") %nbPartZone
        tempZone = temp[booleanTotaltemp]
        tempLocal = tempZone
        execfile("calculateMeanTemp.py")
        tempDesired = meanTvolume #could change for meanT, meanTvolume OR meanTmass
        tableTemperatures[number,index] = tempDesired
    else:
        print ("There is no particle selected at z=%.4f") %zStudied
        tableTemperatures[number,index] = np.nan