# -*- coding: utf-8 -*-
"""
Created on Mon Jul 08 15:24:08 2019

@author: ChristineB.local

Description
This script aims to calculate the error between two sets of data in the
idea of the least square errors

This script needs two sets of data.
!!!!!!!!!!!Using np.load, store your datas in the variables (x1,y1) and (x2,y2)!!!!!!!!!!!

My error is defined as : abs(y2 - y1) / y2
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

"Plot all the curves on the same graph"
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

"Get the experimental data"
donnees = np.loadtxt ('modele.csv', skiprows = 1, unpack = False, delimiter = ';')
x1 = donnees[:,0]
y1 = donnees[:,1]

"Get the model prediction"
modele = np.loadtxt ('exp.csv', skiprows = 1, unpack = False, delimiter = ';')
x2 = modele[:,0]
y2 = modele[:,1]

"Get new global boundaries for the x-vector"
minX = min(min(x1), min(x2))
maxX = min(max(x1), max(x2))
nbPoints = min(len(x1),len(x2))
newX = np.linspace(minX, maxX, nbPoints)

"Create interpolations for the curves"
interY1 = np.interp(newX, x1, y1) #(where we want to interpolate, x, y)
interY2 = np.interp(newX, x2, y2) #(where we want to interpolate, x, y)

"Calculate the absolute error at each point"
error = (abs(interY2 - interY1)) / interY2
maxError = max(error)
averageError = np.mean(error)
print ("The maximum error is %.1f%%.") %(maxError*100)
print ("The average error is %.1f%%.") %(averageError*100)

"Calculate the square of the errors"
squareError = (interY2 - interY1)**2
sumSquareError = sum(squareError)
print ("The sum of the square errors is : %.4f.") %sumSquareError


fig, ax1 = plt.subplots()
ax2 = ax1.twinx() #create a second y-axis with the same x
ax1.plot(x1, y1, marker = 'o', color = 'g', label = 'Exp')
ax1.plot(x2, y2, marker = 'o', color = 'm', label = 'Model')
ax1.plot(newX, interY1, marker = 's', color = 'g', fillstyle = 'none', markersize = 10, linestyle = '', label = 'Inter1')
ax1.plot(newX, interY2, marker = 's', color = 'm', fillstyle = 'none', markersize = 10, linestyle ='', label = 'Inter2')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Temp (C)')
ax2.plot(newX, error, color = 'r')
ax2.set_ylabel('Absolute error (%)', color = 'r')
ax1.legend(loc = 0, numpoints=1)  