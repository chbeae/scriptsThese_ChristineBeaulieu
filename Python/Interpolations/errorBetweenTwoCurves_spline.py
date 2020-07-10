# -*- coding: utf-8 -*-
"""
Created on Mon Jul 08 15:24:08 2019

@author: ChristineB.local

Description
This script aims to calculate the error between two sets of data in the
idea of the least square errors

x : values in log [log(kp/kf)]
xx : values wihout log [kp/kf]

This script needs two sets of data.
!!!!!!!!!!!Using np.load, store your datas in the variables (x1,y1) and (x2,y2)!!!!!!!!!!!

My error is defined as : abs(y2 - y1) / y1
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math
import scipy.cluster
import scipy.interpolate 
from scipy import interpolate
from scipy.interpolate import spline
from scipy.signal import savgol_filter


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
donnees = np.loadtxt ('exp.csv', skiprows = 1, unpack = False, delimiter = ';')
x1 = donnees[:,0]
y1 = donnees[:,1]
xx1 = 10 ** x1

"Get the model prediction"
modele = np.loadtxt ('modele.csv', skiprows = 1, unpack = False, delimiter = ';')
x2 = modele[:,0]
y2 = modele[:,1]
xx2 = 10 ** x2
yy2 = y2

"Create a spline interpolations for the model curve"
newX = np.linspace(min(x1), max(x1), 40)
newX = np.array([35,1556,4630,8185])
splineModel = scipy.interpolate.spline(x2, y2, newX, order=3, kind='smoothest') #(x, y, where we want to interpolate)
splineExp = scipy.interpolate.spline(x1, y1, newX, order=3)
tck = interpolate.splrep(x1, y1)
splineExp = scipy.interpolate.splev(newX, tck)

"Calculate the square of the errors"
#squareError = (splineModel - y1)**2
#sumSquareError = sum(squareError)
#print ("The sum of the square errors is : %.4f.") %sumSquareError


fig = plt.figure()
plt.plot(x1, y1, marker = 'o', linestyle='', label = 'Data')  
plt.plot(newX, splineExp, marker = '', linestyle='-', color='r', label = 'Spline')  
#plt.plot(x1, smoothY, marker = 'o', label = 'Filter')
#plt.plot(np.log10(newX), splineModel, marker = 'o', color = 'r', label = 'Spline')  
#plt.plot(x2, y2, marker = 's', linestyle = '', label = 'Model')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc = 0, numpoints=1)
"""
#fig, ax1 = plt.subplots()
#ax2 = ax1.twinx() #create a second y-axis with the same x
#ax1.plot(x1, y1, marker = 'o', color = 'g', label = 'Spheres')
#ax1.plot(x2, y2, marker = 'o', color = 'm', label = 'Cubes')
#ax1.plot(newX, interY1, marker = 's', color = 'g', fillstyle = 'none', markersize = 10, linestyle = '', label = 'Inter1')
#ax1.plot(newX, interY2, marker = 's', color = 'm', fillstyle = 'none', markersize = 10, linestyle ='', label = 'Inter2')
#ax1.set_xlabel('Number of rotations')
#ax1.set_ylabel('RSD (-)')
#ax2.plot(newX, error, color = 'r')
#ax2.set_ylabel('Absolute error (%)', color = 'r')
#ax1.legend(loc = 0, numpoints=1)  
#
#
#
#
#x = np.arange(10)
#y = np.sin(x)
##cs = CubicSpline(x, y)
#xs = np.arange(-0.5, 9.6, 0.1)
#ys = spline(x,y, xs)
#fig = plt.figure()
#plt.plot(x, y, marker = 'o', linestyle='', label = 'Data')  
#plt.plot(xs, ys, marker = '', label = 'Spline')  
#plt.xlabel('Log (kp/kf)')
#plt.ylabel('ke/kf')
#plt.legend(loc = 0, numpoints=1)
"""