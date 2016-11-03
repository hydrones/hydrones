#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reads data from airborne log files
"""

import datetime as dt
import numpy as np

def extractVar(fileName, varName):
    """
        extracts only lines corresponding to varName in fileName
        :return: data dictionnairy
    """
    for ligne in open(nomFic,'r'):
        if (ligne.startswith('FMT') & (variable in ligne)):
            listLigne = ligne.rstrip().replace(' ','').split(',')[5:]
            nbVal = len(listLigne)
            data=dict.fromkeys(listLigne)
            for k in data.keys():
                data[k] = np.array([])
        if ligne.startswith(variable):
            ligneSansVariable = ligne.replace(variable+',','')
            listVal = np.float_(ligneSansVariable.rstrip().split(','))
            for i in range(nbVal):
                data[listLigne[i]] = np.append(data[listLigne[i]], listVal[i])

    return data

def readLogFile(fileName):
    """
        reads from an airborne log file
        :return: dictionnary containing
    """

    # Read Log Airborne
    pos = logExtractVar(nameLogFile, 'POS')
    gps = logExtractVar(nameLogFile, 'GPS')
    ekf1 = logExtractVar(nameLogFile, 'EKF1')

    # Datation des position a l'aide de la date GPS
    dateRef = dt.datetime(1980, 1, 6, 0, 0, 0, 0)
    clockPos = pos['TimeUS']
    clockGPS = gps['TimeUS']
    secGPSfromRef = np.array([gps['GMS'][i]/1e3 + gps['GWk'][i]*7*86400.0 for i in range(len(gps['TimeUS']))])
    secPosfromRef = np.interp(clockPos, clockGPS, secGPSfromRef)
    pos['AbsoluteDate'] = np.array([dateRef + dt.timedelta(seconds=s) for s in secPosfromRef])

    # Interpolation des roll/pitch/yaw angle sur la clockPos:
    clockEKF1 = ekf1['TimeUS']
    roll = ekf1['Roll']
    pitch = ekf1['Pitch']
    yaw = ekf1['Yaw']
    pos['Roll'] = np.interp(clockPos, clockEKF1, roll)
    pos['Pitch'] = np.interp(clockPos, clockEKF1, pitch)
    pos['Yaw'] = np.interp(clockPos, clockEKF1, yaw)

    return pos

def readLogDirectory(directory, pattern='*.log'):
    """
        reads all log files matching pattern in directory
        :return: dictionnary containing the data
    """

    listFile = sorted(glob.glob("%s/%s" %(directory, pattern)))
    data = dict()

    for fileName in listFile:
        currentData = readLogFile(fileName)

        for key in currentData.keys():
            if key in data.keys():
                data[key] = np.append(data[key], currentData[key])
            else
                data[key] = currentData[key]

    return data
