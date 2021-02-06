# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:56:03 2021

@author: Jerry
"""


import sys, pygame
import pandas as pd
import math
from wgs84_to_twd97 import LatLonToTWD97
from math import tan, sin, cos, radians
import matplotlib.pyplot as plt

#Latitude and Longitude of Taiwan County
data = pd.read_csv("data/Latitude and Longitude of Taiwan County.csv")
data.iloc[:,1:3]*100
#data = pd.read_csv("data/TWD97 corrdinate of taiwan county.csv")
data.head()

plt.scatter(data.iloc[:,1]*100,data.iloc[:,2]*100)

round(data.iloc[:,1:3]*pow(10,-4)/2)