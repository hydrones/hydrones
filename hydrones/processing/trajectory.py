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
# fonctions d'editing
    def zeroesToNan(self, inputKey, outputKey=None, dropna=False, inplace=False):
        """
            replaces null values with NaNs

            :param inputKey: field to scan for null values
            :param outputKey: field to write (if None, will modify the column)
            :param dropna: will remove all NaN (default is False)
            :param inplace: changes the object itself (default False)

            :return: trajectory object is inplace is True, O if not
        """

        dfInput = copy(self.data)
        inputValues = copy(dfInput[inputKey].values)
        inputValues[np.where(inputValues != inputValues)] = np.nan

        # apply the changes to self.data
        if outputKey is None:
            # do the modifications on the column itself
            dfInput[inputKey].values = inputValues
        else:
            # add a new column to the dataframe
            df = pd.DataFrame({outputKey: inputValues}, index=dfInput.index)
            dfInput = pd.concat([dfInput, df], axis=1)

        # drop NaNs if needed
        if dropna:
            dfInput.dropna(axis=0, inplace=True)

        # returns
        if inplace:
            self.data = dfInput
            return 0
        else:
            return Trajectory(df=dfInput)
#===============================================================================


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
