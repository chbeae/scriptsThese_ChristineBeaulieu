# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:47:27 2018

@author: ChristineB.local

Description:

This script calculates the difference between the mean temperature of all
particles of type 1 and all particles of type 2

"""

import numpy as np

temp1 = temp[boolType1]
temp2 = temp[boolType2]
averageTemp1 = np.mean(temp1)
averageTemp2 = np.mean(temp2)

temp1Vector[index] = averageTemp1
temp2Vector[index] = averageTemp2

differenceT1T2 = np.abs(averageTemp1-averageTemp2)
tempDiffVector[index] = differenceT1T2



      
        
    