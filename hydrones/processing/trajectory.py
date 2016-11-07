#!/usr/bin/env python
#

'''
    class to manipulate data along a drone trajectory
'''

from __future__ import print_function
import numpy as np
import pandas as pd
import datetime as dt
from input.telemetry import readTmDirectory
from input.dronelogs import readLogDirectory

class Trajectory:
    '''
    class to hold trajectories data and manipulate them
    '''

    def __init__(self, tmDir=None, tmPattern='HD*', tmMode='mode1',
                    logDir=None, logPattern='*.csv',
                    df=None):
        '''
            constructor

            :param tmDir: directory to read tm files from
            :param tmPattern: pattern to select tm files
            :param logDir: directory to read log files from
            :param logPattern: pattern to select log files
        '''

        # fill object from a dataframe
        if df is not None:
            self.data = df
            self.timeIndex = np.array([pd.Timestamp(i).to_datetime() for i in self.data.index.values])
            self.origDate = self.timeIndex[0]

        else:
            # read telemetry files
            if tmDir is not None:
                (meas, clock) = readTmDirectory(tmDir, pattern=tmPattern, mode=tmMode)
                self._tmMeasure = meas
                self._tmClock = clock

            # read drones log files
            if logDir is not None:
                log = readLogDirectory(logDir, pattern=logPattern)
                self._logMeasure = log

            # get the origin of dates
            self.origDate = dt.datetime(int(self._tmMeasure['year'][0]),
            int(self._tmMeasure['month'][0]),
            int(self._tmMeasure['day'][0]),
            int(self._tmMeasure['hour'][0]),
            int(self._tmMeasure['min'][0]),
            int(self._tmMeasure['sec'][0]),
            int(self._tmMeasure['usec'][0]))

            # create the main time index from leddar clock values
            self.timeIndex = self.secondsToDatetime(self._tmClock['leddar'], self.origDate)

            # interpolate everything to leddar dates
            self.data = self.everythingToDataframe(index=self.timeIndex)

#===============================================================================
# dates interpolation
    def interpDateToDate(self, xOrig, yOrig, xOut):
        """
            interpolate values from one datetime array to another

            :param xOrig: datetime array of input data
            :param yOrig: array of input values
            :param xOut: datetime array of output data

            :return: array of values interpolated of xOut values
        """
        xOrigSeconds = self.datetimeToSeconds(xOrig, xOrig[0])
        xOutSeconds = self.datetimeToSeconds(xOut, xOrig[0])
        yOut = np.interp(xOutSeconds, xOrigSeconds, yOrig)
        return yOut

    def secondsToDatetime(self, seconds, origDate):
        """
            convert seconds from origDate to datetime array

            :param seconds: array of seconds
            :param origDate: date of origin

            :return: array of datetimes
        """
        datetimes = []
        for i in seconds:
            if i < 0:
                datetimes.append(origDate - dt.timedelta(seconds=i))
            else:
                datetimes.append(origDate + dt.timedelta(seconds=i))
        return np.array(datetimes)

    def datetimeToSeconds(self, datetimes, origDate):
        """
            convert datetime array to seconds from origDate

            :param datetimes: array of datetimes objects
            :param origDate: origin of dates for conversion

            :return: array of seconds from origDate
        """
        orientation=[]
        for date in datetimes:
            if date < origDate:
                orientation.append(-1.)
            else:
                orientation.append(1.)
        seconds = [(i - origDate).total_seconds() for i in datetimes]
        return np.multiply(seconds, np.array(orientation))
#===============================================================================

#===============================================================================
# dataframe manipulation
    def everythingToDataframe(self, index=None):
        """
            blends all tm and log data to a single dataframe

            :return: pandas dataframe containing everything
        """
        if index is None:
            raise Exception("an index must be given")

        d = dict()

        # hydrones tm fields
        for key in self._tmMeasure.keys():
            if 'leddar' in key:
                d[key] = self._tmMeasure[key]

            if 'imu' in key:
                origVal = self._tmMeasure[key]
                origDate = self.secondsToDatetime(self._tmClock['imu'], self.origDate)
                interpVal = self.interpDateToDate(origDate, origVal, index)
                d[key] = interpVal

            if 'baro' in key:
                origVal = self._tmMeasure[key]
                origDate = self.secondsToDatetime(self._tmClock['baro'], self.origDate)
                interpVal = self.interpDateToDate(origDate, origVal, index)
                d[key] = interpVal

            if 'gps' in key:
                origVal = self._tmMeasure[key]
                origDate = self.secondsToDatetime(self._tmClock['gps'], self.origDate)
                interpVal = self.interpDateToDate(origDate, origVal, index)
                d[key] = interpVal

        # drone log fields
        for key in self._logMeasure.keys():
            if key == 'TimeUS' or key =='AbsoluteDate':
                continue
            origVal = self._logMeasure[key]
            origSeconds = self.datetimeToSeconds(self._logMeasure['AbsoluteDate'], self.origDate)
            origDate = self.secondsToDatetime(origSeconds, self.origDate)
            interpVal = self.interpDateToDate(origDate, origVal, index)
            d[key] = interpVal

        return(pd.DataFrame(d, index=self.timeIndex))

#===============================================================================
# data selection routines
    def timeSelection(self, beginDate, endDate):
        """
            performs a data selection based on times

            :param beginDate: first date of the selection
            :param endDate: last date of the selection

            :return: trajectory object containing the selection
        """
        index = np.where((self.timeIndex >= beginDate) & (self.timeIndex) < endDate)
        df = self.data.iloc[index, :]
        return trajectory(df=df)
#===============================================================================



#===============================================================================
# different loaders to accomodate various cases
    def load_json(self, fileName):
        '''
        load a Trajectory from a GeoJSON file
        '''

        # save the file it was loaded from
        self._geojsonSource = fileName

        # load the geojson file
        import geojson
        io = open(self._geojsonSource, 'r')
        self.geojson = geojson.load(io)
        io.close()

        # extract coordinates
        latitudes = []
        longitudes = []
        if self.geojson.type=='FeatureCollection':
            for feature in self.geojson.features:
                coordinates = feature.geometry.coordinates
                for c in coordinates:
                    latitudes.append(c[1])
                    longitudes.append(c[0])

        # for the sake of example, generate fake data
        # fake date range
        hdMeas = dict()
        dates = pd.date_range(start='1/1/2016', periods=len(latitudes), freq='s')
        # fake data except for lat & lon
        for key in self._keys:
            if key == 'gps_lon':
                hdMeas[key] = longitudes
            elif key =='gps_lat':
                hdMeas[key] = latitudes
            else:
                hdMeas[key] = self._generateDummyData(len(latitudes))

        self._measurements = pd.DataFrame(hdMeas, index=dates)
        return 0

    def readBinaryFile(self, filename):
        '''
        load from a binary file generated by HMK1
        '''

        # expected structure of the file
        Structure = "<HBBBBBIfffIffIfffffffff"
        s = struct.Struct(Structure)
        sizeMeas = struct.calcsize(Structure)

        # init the output dictionnary
        hdMeas = dict()

        for key in self._keys:
            hdMeas[key] = []

        # open the file
        try:
            hdFile = open(filename,"rb")
        except IOError:
            raise

        # loop through the file
        nbMeasures = 0
        try:
            while True:
                measure = hdFile.read(sizeMeas)
                if len(measure) != sizeMeas:
                    break

                # Recuperation des donnees
                readMeasure = s.unpack(measure)
                hdMeas['year'].append(readMeasure[0])
                hdMeas['month'].append(readMeasure[1])
                hdMeas['day'].append(readMeasure[2])
                hdMeas['hour'].append(readMeasure[3])
                hdMeas['min'].append(readMeasure[4])
                hdMeas['sec'].append(readMeasure[5])
                hdMeas['usec'].append(readMeasure[6])
                hdMeas['gps_lat'].append(readMeasure[7])
                hdMeas['gps_lon'].append(readMeasure[8])
                hdMeas['gps_geoidheight'].append(readMeasure[9])
                hdMeas['gps_nbsat'].append(readMeasure[10])
                hdMeas['gps_altitude'].append(readMeasure[11])
                hdMeas['leddar_range'].append(readMeasure[12])
                hdMeas['leddar_ampl'].append(readMeasure[13])
                hdMeas['baro_pressure'].append(readMeasure[14])
                hdMeas['baro_sea_level_pressure'].append(readMeasure[15])
                hdMeas['baro_altitude'].append(readMeasure[16])
                hdMeas['baro_temperature'].append(readMeasure[17])
                hdMeas['imu_pitch_angle'].append(readMeasure[18])
                hdMeas['imu_roll_angle'].append(readMeasure[19])
                hdMeas['imu_linear_accel_x'].append(readMeasure[20])
                hdMeas['imu_linear_accel_y'].append(readMeasure[21])
                hdMeas['imu_linear_accel_z'].append(readMeasure[22])

                nbMeasures += 1

        except IOError:
            print("Erreur de lecture de la mesure")
            pass

        # convert the dates to datetime object
        dates = [dt.datetime(hdMeas['year'][i],
                                hdMeas['month'][i],
                                hdMeas['day'][i],
                                hdMeas['hour'][i],
                                hdMeas['min'][i],
                                hdMeas['sec'][i],
                                hdMeas['usec'][i]) for i in np.arange(nbMeasures)]

        # store the values in the Object
        df = pd.DataFrame(hdMeas, index=dates)
        self._measurements =  pd.concat([self._measurements, df])

        return 0

    def loadBinaryFiles(self, directory, motif):
        '''
        reads from binary measurement files in a directory
        '''
        filesToRead = sorted(glob.glob("%s/%s" %(directory, motif)))
        print(filesToRead)

        for f in filesToRead:
            print("reading from file %s" %f)
            self.readBinaryFile(f)
        return 0

    def _generateDummyData(self, length):
        '''
        generate dummy data
        '''
        return np.arange(length)*(-0.0003)+np.random.randn(length)
        return 0

#==============================================================================
# functions to travel along a trajectory
    def travel(self, delay=0.1):
        '''
        travels along the trajectory
        '''
        while self._oneStepTravel()==0:
            return self._current_position
            time.sleep(delay)
        return 0

    def _oneStepTravel(self, loop=True):
        '''
        moves from the current index to the next one
        '''

        if self._currentIndex < len(self._measurements.index)-1:
            self._currentIndex += 1
        else:
            if loop:
                self._currentIndex = 0
            else:
                print("end of trajectory reached")
                return 1
        return 0

#===============================================================================
# some access to values (other than pandas methods)
    def pastTimes(self):
        """
        returns all past times as a flattened array
        """
        return np.array(self._measurements.index.values[0:self._currentIndex])

    def pastValues(self, key):
        """
        returns all past values of a key as a flattened array
        """
        if key not in self._keys:
            print("There is no such key: " %key)
            raise Exception()
        else:
            return(self._measurements[key].values[0:self._currentIndex])

    def currentValue(self, key):
        '''
        returns the value associated to a key at the current position
        '''
        if key not in self._keys:
            print("There is no such key: " %key)
            raise Exception()
        else:
            return(self._measurements[key].values[self._currentIndex])

    def pastPositions(self):
        """
        returns all past positions as a flattened array
        """
        return np.array(self._pastPositions)

#===============================================================================
# operations on variables
    def integrate(key_in, key_out, inplace=False):
        '''
        integrates values over time
        '''
        if key_in not in self._keys():
            print("There is no such key: %s" %key_in)
            raise Exception()

        values = self._measurements[key].values
        times = self._measurements.index.values
        integration = np.zeros(len(values))

        for i in np.arange(1,len(values)-1,1):
            deltaT = (times[i] - times[i-1]).item().total_seconds()
            integration[i] = integration[i-1] + values[i] * deltaT

        df = pd.DataFrame({key_out:integration}, index=self._measurements.index)

        if inplace:
            self._measurements = pd.concat([self._measurements, df])
            return 0
        else:
            return df

    def foliumShow(self, out):
        '''
        plot the trajectory using folium
        '''
        import folium
        m = folium.Map([43, 10], zoom_start=4, tiles='Stamen Toner')
        folium.GeoJson(self.geojson).add_to(m)
        m.save(out)

    def bokehSeries(self):
        return 0

    def createFoliumMarker(self,
            color='green',
            icon='stats',
            max_width=2650,
            location='current',
            width=500,
            height=250):
        '''
        return a folium marker with the measurements of the trajectory
        '''
        from bokeh.plotting import figure
        from bokeh.resources import CDN
        from bokeh.embed import file_html
        import folium
        from folium.element import IFrame

        # get the marker location
        if location=='current':
            location=self._current_position

        elif location=='center':
            location=self.center_position

        # create the figure of past data
        p = figure(x_axis_type="datetime",
                       width=width, height=height)
        p.line(self.pastTimes(), self.pastValues(), line_width=2)

        html = file_html(p, CDN, "marker")
        iframe = IFrame(html, width=width+40, height=height+80)
        popup = folium.Popup(iframe, max_width=max_width)
        icon = folium.Icon(color=color, icon=icon)

        marker = folium.Marker(location=[location[1],location[0]],
                                   popup=popup,
                                   icon=icon)
        return marker
