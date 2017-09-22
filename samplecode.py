# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:10:39 2017

@author: anoopscoop
"""
#note that trackLength is half of the circle's circumference. It is the max length of the track in one direction.
def StandinVehicleTravelTime(trackLength, stationDensity, cruisingSpeed,dwellTime):

   return ((trackLength+ (1/stationDensity))/(2*cruisingSpeed)) + (trackLength* dwellTime * (.5*stationDensity))
   

print(StandinVehicleTravelTime(1,2,3,4))



    