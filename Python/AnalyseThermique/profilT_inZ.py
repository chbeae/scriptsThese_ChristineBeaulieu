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

"Get the temperature of part versus depth at X=0"
booleanX0 = (positionxyz[:,0]>= -surplus) & (positionxyz[:,0]<= surplus)

for zIndex in range(nbPaquets):
    lowLimitZ = -drumRadius + (zIndex*paquetWidth)
    highLimitZ = -drumRadius + ((zIndex+1)*paquetWidth)
    
    zMiddleVector[zIndex] = lowLimitZ + (paquetWidth/2)
    boolZPos = (positionxyz[:,2]>=lowLimitZ) & (positionxyz[:,2] <= highLimitZ)
    boolTotZ = booleanX0 & boolZPos
    nbPartThatPaquet = sum(boolTotZ)
    if nbPartThatPaquet != 0 :
        tempPaquet = temp[boolTotZ]
        averageTempThatPaquet = np.mean(tempPaquet)
        zTempTime[zIndex,index] = averageTempThatPaquet
        
        #Average inertia Volume temperature
        rhoPaquet = density[boolTotZ]
        cpPaquet= cpVector[boolTotZ]
        volumePaquet = volume[boolTotZ]
        rhoCpViTiPaquet = rhoPaquet * cpPaquet * volumePaquet * tempPaquet
        rhoCpViPaquet = rhoPaquet * cpPaquet * volumePaquet 
        sum_rhoCpViTiPaquet = sum(rhoCpViTiPaquet)
        sum_rhoCpViPaquet = sum(rhoCpViPaquet)
        averageInertiaVolTempPaquet = sum_rhoCpViTiPaquet/ sum_rhoCpViPaquet
        zTempInertiaVolTime[zIndex,index] = averageInertiaVolTempPaquet 
    
    



    

        
            
        
    