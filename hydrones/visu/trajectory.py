#!/usr/bin/env python
#

'''
several tools to work along drone trajectories
'''
import numpy as np
import pandas as pd
import datetime

class Trajectory():
    '''
    class to hold trajectories data and manipulate them
    '''

    def __init__(self):
        '''
        constructor
        '''
        return None

    def load_json(self, file):
        '''
        load a Trajectory from a GeoJSON file
        '''

        # load the geojson file
        import geojson
        self.source_file=file
        io = open(self.source_file, 'r')
        self.geojson = geojson.load(io)
        io.close()

        # extract coordinates

        # for the sake of example, generate fake data
        self._generateDummyData(size=1000)






        return 0

    def _generateDummyData(self, size=10000, start=datetime.datetime(2016, 7, 22), freq=1.):

        # generate an array of dates at given frequency
        delta_t=pd.tseries.offsets.DateOffset(seconds=1./freq)
        self._dates = pd.date_range(start, periods=size, freq=delta_t)

        # generate a data array
        self._measurements=np.arange(size)*(-0.0003)+np.random.randn(size)





    def travel(self, distancce=10, interp='linear'):
        '''
        return the next position along the trajectory
        '''
        self.current_position = 0
        return 0

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
