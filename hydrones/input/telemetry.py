#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reads data from binary telemetry files
"""


import datetime as dt
import struct
import numpy as np
import glob

MEAS_KEYS = ['year','month','day','hour','min','sec','usec',
    'gps_lat','gps_lon','gps_nbsat','gps_geoidheight','gps_altitude',
    'leddar_range','leddar_amplitude',
    'baro_pressure','baro_altitude','baro_temperature','baro_sea_level_pressure',
    'imu_yaw_angle','imu_roll_angle','imu_pitch_angle',
    'imu_accel_x','imu_accel_y','imu_accel_z',
    'imu_grav_accel_x','imu_grav_accel_y','imu_grav_accel_z',
    'imu_linear_accel_x','imu_linear_accel_y','imu_linear_accel_z']
CLOCK_KEYS = ['imu','leddar','baro','gps']



def readTmFile(fileName, mode='mode1'):
    """
        reads data from a telemetry file
        returns two dictionnaries, meas, clock
        containing measurement and clock values
    """

    # init of output dictionnaries
    hdMeas = dict()
    hdClock = dict()
    for key in MEAS_KEYS:
        hdMeas[key] = np.array([])
    for key in CLOCK_KEYS:
        hdClock[key] = np.array([])

    # open the file
    tmFile = open(fileName,"rb")

    # read it depending on mode
    if mode=='mode1':

        Structure = "<dH5BI3fIfd4fdfIdfIdfIdfId12fdfIdfIdfIdfId12fd4fdfIdfIdfIdfId12fdfIdfIdfIdfId12fdfIdfI"
        s = struct.Struct(Structure)
        sizeMeas = struct.calcsize(Structure)

        nbMeasure = 0

        try:
            while True:
                measure = tmFile.read(sizeMeas)
                if len(measure) != sizeMeas:
                    break

                # Recuperation des donnees
                readMeasure = s.unpack(measure)

                # GPS
                hdClock['gps'] = np.append(hdClock['gps'], readMeasure[0])
                hdMeas['year'] = np.append(hdMeas['year'], readMeasure[1])
                hdMeas['month'] = np.append(hdMeas['month'], readMeasure[2])
                hdMeas['day'] = np.append(hdMeas['day'], readMeasure[3])
                hdMeas['hour'] = np.append(hdMeas['hour'], readMeasure[4])
                hdMeas['min'] = np.append(hdMeas['min'], readMeasure[5])
                hdMeas['sec'] = np.append(hdMeas['sec'], readMeasure[6])
                hdMeas['usec'] = np.append(hdMeas['usec'], readMeasure[7])
                hdMeas['gps_lat'] = np.append(hdMeas['gps_lat'], readMeasure[8])
                hdMeas['gps_lon'] = np.append(hdMeas['gps_lon'], readMeasure[9])
                hdMeas['gps_geoidheight'] = np.append(hdMeas['gps_geoidheight'], readMeasure[10])
                hdMeas['gps_nbsat'] = np.append(hdMeas['gps_nbsat'], readMeasure[11])
                hdMeas['gps_altitude'] = np.append(hdMeas['gps_altitude'], readMeasure[12])
                # 1 baro
                hdClock['baro'] = np.append(hdClock['baro'], readMeasure[13])
                hdMeas['baro_pressure'] = np.append(hdMeas['baro_pressure'], readMeasure[14])
                hdMeas['baro_sea_level_pressure'] = np.append(hdMeas['baro_sea_level_pressure'], readMeasure[15])
                hdMeas['baro_altitude'] = np.append(hdMeas['baro_altitude'], readMeasure[16])
                hdMeas['baro_temperature'] = np.append(hdMeas['baro_temperature'], readMeasure[17])
                # 4 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[18])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[19])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[20])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[21])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[22])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[23])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[24])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[25])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[26])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[27])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[28])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[29])
                # 1 IMU
                hdClock['imu'] = np.append(hdClock['imu'], readMeasure[30])
                hdMeas['imu_pitch_angle'] = np.append(hdMeas['imu_pitch_angle'], readMeasure[31])
                hdMeas['imu_roll_angle'] = np.append(hdMeas['imu_roll_angle'], readMeasure[32])
                hdMeas['imu_yaw_angle'] = np.append(hdMeas['imu_yaw_angle'], readMeasure[33])
                hdMeas['imu_accel_x'] = np.append(hdMeas['imu_accel_x'], readMeasure[34])
                hdMeas['imu_accel_y'] = np.append(hdMeas['imu_accel_y'], readMeasure[35])
                hdMeas['imu_accel_z'] = np.append(hdMeas['imu_accel_z'], readMeasure[36])
                hdMeas['imu_linear_accel_x'] = np.append(hdMeas['imu_linear_accel_x'], readMeasure[37])
                hdMeas['imu_linear_accel_y'] = np.append(hdMeas['imu_linear_accel_y'], readMeasure[38])
                hdMeas['imu_linear_accel_z'] = np.append(hdMeas['imu_linear_accel_z'], readMeasure[39])
                hdMeas['imu_grav_accel_x'] = np.append(hdMeas['imu_grav_accel_x'], readMeasure[40])
                hdMeas['imu_grav_accel_y'] = np.append(hdMeas['imu_grav_accel_y'], readMeasure[41])
                hdMeas['imu_grav_accel_z'] = np.append(hdMeas['imu_grav_accel_z'], readMeasure[42])
                # 4 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[43])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[44])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[45])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[46])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[47])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[48])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[49])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[50])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[51])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[52])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[53])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[54])
                # 1 IMU
                hdClock['imu'] = np.append(hdClock['imu'], readMeasure[55])
                hdMeas['imu_pitch_angle'] = np.append(hdMeas['imu_pitch_angle'], readMeasure[56])
                hdMeas['imu_roll_angle'] = np.append(hdMeas['imu_roll_angle'], readMeasure[57])
                hdMeas['imu_yaw_angle'] = np.append(hdMeas['imu_yaw_angle'], readMeasure[58])
                hdMeas['imu_accel_x'] = np.append(hdMeas['imu_accel_x'], readMeasure[59])
                hdMeas['imu_accel_y'] = np.append(hdMeas['imu_accel_y'], readMeasure[60])
                hdMeas['imu_accel_z'] = np.append(hdMeas['imu_accel_z'], readMeasure[61])
                hdMeas['imu_linear_accel_x'] = np.append(hdMeas['imu_linear_accel_x'], readMeasure[62])
                hdMeas['imu_linear_accel_y'] = np.append(hdMeas['imu_linear_accel_y'], readMeasure[63])
                hdMeas['imu_linear_accel_z'] = np.append(hdMeas['imu_linear_accel_z'], readMeasure[64])
                hdMeas['imu_grav_accel_x'] = np.append(hdMeas['imu_grav_accel_x'], readMeasure[65])
                hdMeas['imu_grav_accel_y'] = np.append(hdMeas['imu_grav_accel_y'], readMeasure[66])
                hdMeas['imu_grav_accel_z'] = np.append(hdMeas['imu_grav_accel_z'], readMeasure[67])
                # 1 baro
                hdClock['baro'] = np.append(hdClock['baro'], readMeasure[68])
                hdMeas['baro_pressure'] = np.append(hdMeas['baro_pressure'], readMeasure[69])
                hdMeas['baro_sea_level_pressure'] = np.append(hdMeas['baro_sea_level_pressure'], readMeasure[70])
                hdMeas['baro_altitude'] = np.append(hdMeas['baro_altitude'], readMeasure[71])
                hdMeas['baro_temperature'] = np.append(hdMeas['baro_temperature'], readMeasure[72])
                # 4 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[73])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[74])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[75])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[76])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[77])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[78])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[79])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[80])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[81])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[82])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[83])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[84])
                # 1 IMU
                hdClock['imu'] = np.append(hdClock['imu'], readMeasure[85])
                hdMeas['imu_pitch_angle'] = np.append(hdMeas['imu_pitch_angle'], readMeasure[86])
                hdMeas['imu_roll_angle'] = np.append(hdMeas['imu_roll_angle'], readMeasure[87])
                hdMeas['imu_yaw_angle'] = np.append(hdMeas['imu_yaw_angle'], readMeasure[88])
                hdMeas['imu_accel_x'] = np.append(hdMeas['imu_accel_x'], readMeasure[89])
                hdMeas['imu_accel_y'] = np.append(hdMeas['imu_accel_y'], readMeasure[90])
                hdMeas['imu_accel_z'] = np.append(hdMeas['imu_accel_z'], readMeasure[91])
                hdMeas['imu_linear_accel_x'] = np.append(hdMeas['imu_linear_accel_x'], readMeasure[92])
                hdMeas['imu_linear_accel_y'] = np.append(hdMeas['imu_linear_accel_y'], readMeasure[93])
                hdMeas['imu_linear_accel_z'] = np.append(hdMeas['imu_linear_accel_z'], readMeasure[94])
                hdMeas['imu_grav_accel_x'] = np.append(hdMeas['imu_grav_accel_x'], readMeasure[95])
                hdMeas['imu_grav_accel_y'] = np.append(hdMeas['imu_grav_accel_y'], readMeasure[96])
                hdMeas['imu_grav_accel_z'] = np.append(hdMeas['imu_grav_accel_z'], readMeasure[97])
                # 4 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[98])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[99])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[100])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[101])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[102])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[103])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[104])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[105])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[106])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[107])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[108])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[109])
                # 1 IMU
                hdClock['imu'] = np.append(hdClock['imu'], readMeasure[110])
                hdMeas['imu_pitch_angle'] = np.append(hdMeas['imu_pitch_angle'], readMeasure[111])
                hdMeas['imu_roll_angle'] = np.append(hdMeas['imu_roll_angle'], readMeasure[112])
                hdMeas['imu_yaw_angle'] = np.append(hdMeas['imu_yaw_angle'], readMeasure[113])
                hdMeas['imu_accel_x'] = np.append(hdMeas['imu_accel_x'], readMeasure[114])
                hdMeas['imu_accel_y'] = np.append(hdMeas['imu_accel_y'], readMeasure[115])
                hdMeas['imu_accel_z'] = np.append(hdMeas['imu_accel_z'], readMeasure[116])
                hdMeas['imu_linear_accel_x'] = np.append(hdMeas['imu_linear_accel_x'], readMeasure[117])
                hdMeas['imu_linear_accel_y'] = np.append(hdMeas['imu_linear_accel_y'], readMeasure[118])
                hdMeas['imu_linear_accel_z'] = np.append(hdMeas['imu_linear_accel_z'], readMeasure[119])
                hdMeas['imu_grav_accel_x'] = np.append(hdMeas['imu_grav_accel_x'], readMeasure[120])
                hdMeas['imu_grav_accel_y'] = np.append(hdMeas['imu_grav_accel_y'], readMeasure[121])
                hdMeas['imu_grav_accel_z'] = np.append(hdMeas['imu_grav_accel_z'], readMeasure[122])
                # 2 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[123])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[124])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[125])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[126])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[127])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[128])

                nbMeasure += 1

        except IOError:
            print("Erreur de lecture de la mesure")
            pass

    elif mode=='mode2':
        Structure = "<"
        s = struct.Struct(Structure)
        sizeMeas = struct.calcsize(Structure)

        nbMeasure = 0
        try:
            while True:
                measure = tmFile.read(sizeMeas)
                if len(measure) != sizeMeas:
                    break

                # Recuperation des donnees
                readMeasure = s.unpack(measure)

                # GPS
                hdClock['gps'] = np.append(hdClock['gps'], readMeasure[0])
                hdMeas['year'] = np.append(hdMeas['year'], readMeasure[1])
                hdMeas['month'] = np.append(hdMeas['month'], readMeasure[2])
                hdMeas['day'] = np.append(hdMeas['day'], readMeasure[3])
                hdMeas['hour'] = np.append(hdMeas['hour'], readMeasure[4])
                hdMeas['min'] = np.append(hdMeas['min'], readMeasure[5])
                hdMeas['sec'] = np.append(hdMeas['sec'], readMeasure[6])
                hdMeas['usec'] = np.append(hdMeas['usec'], readMeasure[7])
                hdMeas['gps_lat'] = np.append(hdMeas['gps_lat'], readMeasure[8])
                hdMeas['gps_lon'] = np.append(hdMeas['gps_lon'], readMeasure[9])
                hdMeas['gps_geoidheight'] = np.append(hdMeas['gps_geoidheight'], readMeasure[10])
                hdMeas['gps_nbsat'] = np.append(hdMeas['gps_nbsat'], readMeasure[11])
                hdMeas['gps_altitude'] = np.append(hdMeas['gps_altitude'], readMeasure[12])
                # 8 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[12])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[14])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[15])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[16])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[17])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[18])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[19])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[20])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[21])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[22])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[23])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[24])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[25])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[26])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[27])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[28])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[29])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[30])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[31])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[32])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[33])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[34])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[35])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[36])
                # 1 baro
                hdClock['baro'] = np.append(hdClock['baro'], readMeasure[37])
                hdMeas['baro_pressure'] = np.append(hdMeas['baro_pressure'], readMeasure[38])
                hdMeas['baro_sea_level_pressure'] = np.append(hdMeas['baro_sea_level_pressure'], readMeasure[39])
                hdMeas['baro_altitude'] = np.append(hdMeas['baro_altitude'], readMeasure[40])
                hdMeas['baro_temperature'] = np.append(hdMeas['baro_temperature'], readMeasure[41])
                # 8 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[42])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[43])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[44])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[45])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[46])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[47])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[48])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[49])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[50])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[51])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[52])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[53])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[54])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[55])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[56])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[57])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[58])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[59])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[60])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[61])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[62])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[63])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[64])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[65])
                # 1 IMU
                hdClock['imu'] = np.append(hdClock['imu'], readMeasure[66])
                hdMeas['imu_pitch_angle'] = np.append(hdMeas['imu_pitch_angle'], readMeasure[67])
                hdMeas['imu_roll_angle'] = np.append(hdMeas['imu_roll_angle'], readMeasure[68])
                hdMeas['imu_yaw_angle'] = np.append(hdMeas['imu_yaw_angle'], readMeasure[69])
                hdMeas['imu_accel_x'] = np.append(hdMeas['imu_accel_x'], readMeasure[70])
                hdMeas['imu_accel_y'] = np.append(hdMeas['imu_accel_y'], readMeasure[71])
                hdMeas['imu_accel_z'] = np.append(hdMeas['imu_accel_z'], readMeasure[72])
                hdMeas['imu_linear_accel_x'] = np.append(hdMeas['imu_linear_accel_x'], readMeasure[73])
                hdMeas['imu_linear_accel_y'] = np.append(hdMeas['imu_linear_accel_y'], readMeasure[74])
                hdMeas['imu_linear_accel_z'] = np.append(hdMeas['imu_linear_accel_z'], readMeasure[75])
                hdMeas['imu_grav_accel_x'] = np.append(hdMeas['imu_grav_accel_x'], readMeasure[76])
                hdMeas['imu_grav_accel_y'] = np.append(hdMeas['imu_grav_accel_y'], readMeasure[77])
                hdMeas['imu_grav_accel_z'] = np.append(hdMeas['imu_grav_accel_z'], readMeasure[78])
                # 8 leddar measurements
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[79])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[80])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[81])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[82])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[83])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[84])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[85])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[86])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[87])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[88])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[89])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[90])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[91])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[92])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[93])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[94])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[95])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[96])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[97])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[98])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[99])
                hdClock['leddar'] = np.append(hdClock['leddar'], readMeasure[100])
                hdMeas['leddar_range'] = np.append(hdMeas['leddar_range'], readMeasure[101])
                hdMeas['leddar_amplitude'] = np.append(hdMeas['leddar_amplitude'], readMeasure[102])

                nbMeasure += 1

        except IOError:
            print("Erreur de lecture de la mesure")
            pass

    else:
        raise Exception("mode %s is unknown")

    return (hdMeas, hdClock)


def readTmDirectory(directory, pattern='*', mode='mode1'):
    """
        reads all telemetry files mathcing pattern in directory
    """

    # init of output dictionnaries
    meas = dict()
    clock = dict()
    for key in MEAS_KEYS:
        meas[key] = np.array([])
    for key in CLOCK_KEYS:
        clock[key] = np.array([])

    # list of files to read
    listFile = sorted(glob.glob("%s/%s" %(directory, pattern)))

    # loop through all files
    for fileName in listFile:
        currentMeas, currentClock = readTmFile(fileName, mode=mode)

        # append to the dictionnaries
        for key in MEAS_KEYS:
            meas[key] = np.append(meas[key], currentMeas[key])
        for key in CLOCK_KEYS:
            clock[key] = np.append(clock[key], currentClock[key])

    return (meas, clock)
