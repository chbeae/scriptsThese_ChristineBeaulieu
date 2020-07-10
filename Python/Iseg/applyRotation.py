# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:06:22 2017

@author: Christine Beaulieu

Description du code:
Ce code 
-    applique une matrice de rotation d'angle theta à un groupe de
    vecteurs position
-    *** ce code est appelé par le code diffusionCoeff
-   il ne peut pas être roulé seul, car il a besoin de variables dans
    le premier code main
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

"**************************************************************************"
"Apply the rotation Matrix"
"***************************************************************************"
print ""
print "**********************"
print "Rotation of all the position vectors"
theta = - meanDynAngle #deg #34
print theta
thetaRad = math.radians(theta)
rotationM = np.array([[math.cos(thetaRad), 0, math.sin(thetaRad)],\
                      [0, 1, 0],\
                      [-math.sin(thetaRad), 0, math.cos(thetaRad)]])

print ""        
print "The rotation matrix is:" 
print rotationM
positionxyzRot = positionxyz.dot(rotationM)
positionxyz = positionxyzRot
#vitessexyzRot = vitessexyz.dot(rotationM)