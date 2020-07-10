# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 18:21:12 2018

@author: ChristineB.local

Description du code:
This code calculates the mean temperature of a bulk of particles with 3 means:
    -mean T
    -mean T averaged on particle volume (inspired by Komossa)
    -mean T averaged on particle mass

-    ce code doit être roulé une fois que les particules et leurs infos sont
    chargées
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

"Simple mean"
meanT = np.mean(tempLocal)
#print ("The mean temperature is %.1f K.") %meanT

"Volume averaged"
volume = (4*math.pi*(radius**3))/3. #vector of all particles
volumeZone = volume[booleanTotaltemp]
sumVolumeT = 0
for i, temperature in enumerate(tempLocal):
    product = temperature * volumeZone[i]
    sumVolumeT = sumVolumeT + product
meanTvolume = sumVolumeT/(sum(volumeZone))
#print ("The mean temperature averaged on volume is %.1f K.") %meanTvolume

"Mass averaged"
mass = volume * density # kg. Vector of all particles
massZone = mass[booleanTotaltemp]
sumMassT = 0
for i, temperature in enumerate(tempLocal):
    product = temperature * massZone[i]
    sumMassT = sumMassT + product
meanTmass = sumMassT/(sum(massZone))
#print ("The mean temperature averaged on mass is %.1f K.") %meanTmass

