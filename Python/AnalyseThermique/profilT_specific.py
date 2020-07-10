# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:47:27 2018

@author: ChristineB.local

Description:

This script calculates a RADIAL TEMPERATURE at a certain time.

"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

surplus = 1*maxDiameter

"Get the temperature at a specific position"
boolXspeci = (positionxyz[:,0]>= (xPosi-surplus)) & (positionxyz[:,0]<= (xPosi+surplus))
boolYspeci = (positionxyz[:,1]>= (yPosi-surplus)) & (positionxyz[:,1]<= (yPosi+surplus))
boolZspeci = (positionxyz[:,2]>= (zPosi-surplus)) & (positionxyz[:,2]<= (zPosi+surplus))

boolSpeciPlace = boolXspeci & boolYspeci & boolZspeci
nbPartSpeci = sum(boolSpeciPlace)
tempSpeci = temp[boolSpeciPlace]
averageTempSpeci = np.mean(tempSpeci)
tempSpeciVector[index] = averageTempSpeci

"Volume averaged"
volumeZone = volume[boolSpeciPlace]
sumVolumeT = 0
for iT, tempera in enumerate(tempSpeci):
    product = tempera * volumeZone[iT]
    sumVolumeT = sumVolumeT + product
meanTvolume = sumVolumeT/(sum(volumeZone))
#print ("The mean temperature averaged on volume is %.1f K.") %meanTvolume
tempSpeciVolumeVector[index] = meanTvolume      

"Inertia average"
rhoSpeci = density[boolSpeciPlace]
cpSpeci = cpVector[boolSpeciPlace]
rhoCpTiSpeci = rhoSpeci * cpSpeci * tempSpeci
rhoCpSpeci = rhoSpeci * cpSpeci
sum_rhoCpTiSpeci = sum(rhoCpTiSpeci)
sum_rhoCpSpeci = sum(rhoCpSpeci)

averageTempSpeciInertia = sum_rhoCpTiSpeci / sum_rhoCpSpeci
tempSpeciInertiaVector[index] = averageTempSpeciInertia    

        
    