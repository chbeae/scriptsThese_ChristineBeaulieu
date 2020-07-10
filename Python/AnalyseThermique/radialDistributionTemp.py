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



"Get the temperature of every annulus"
for radialPosition in range(nbAnnuli):
    lowLimit = radialPosition * annulusWidth
    highLimit = (radialPosition+1) * annulusWidth
    
    boolRadPos = (radialPos > lowLimit) & (radialPos < highLimit)
    nbPartThatAnnulus = sum(boolRadPos)
    tempThatAnnulus = temp[boolRadPos]
    
    rhoThatAnnulus = density[boolRadPos]
    cpThatAnnulus = cpVector[boolRadPos]
    volumeThatAnnulus = volume[boolRadPos]
    

    
    #Average inertia temperature
    rhoCpTiThatAnnulus = rhoThatAnnulus * cpThatAnnulus * tempThatAnnulus
    rhoCpThatAnnulus = rhoThatAnnulus * cpThatAnnulus
    sum_rhoCpTiThatAnnulus = sum(rhoCpTiThatAnnulus)
    sum_rhoCpThatAnnulus = sum(rhoCpThatAnnulus)
    averageInertiaTempThatAnnulus = sum_rhoCpTiThatAnnulus / sum_rhoCpThatAnnulus
    radialTempInertiaTime[radialPosition,index] = averageInertiaTempThatAnnulus
    
    #Number average temperature
    averageTempThatAnnulus = np.mean(tempThatAnnulus)
    radialTempTime[radialPosition,index] = averageTempThatAnnulus
    
    #Average inertia Volume temperature
    rhoCpViTiThatAnnulus = rhoThatAnnulus * cpThatAnnulus * volumeThatAnnulus * tempThatAnnulus
    rhoCpViThatAnnulus = rhoThatAnnulus * cpThatAnnulus * volumeThatAnnulus
    sum_rhoCpViTiThatAnnulus = sum(rhoCpViTiThatAnnulus)
    sum_rhoCpViThatAnnulus = sum(rhoCpViThatAnnulus)
    averageInertiaVolTempThatAnnulus = sum_rhoCpViTiThatAnnulus / sum_rhoCpViThatAnnulus
    radialTempInertiaVolTime[radialPosition,index] = averageInertiaVolTempThatAnnulus    
    



    

        
            
        
    