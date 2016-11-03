#! /usr/bin/env python
#

from bokeh.plotting import figure, curdoc
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.client import push_session

from folium.element import IFrame
import time
import folium
# init d'un trajectoire
from trajectory import Trajectory

t = Trajectory()
t.load_json('/home/pprandi/Documents/hydrones/01_extraction/ceou.geojson')

# creation de la carte
m = folium.Map([43, 10], zoom_start=4, tiles='Stamen Toner')
folium.GeoJson(t.geojson).add_to(m)
session = push_session(curdoc())


def update():
    t._oneStepTravel()
    marker = t.createFoliumMarker(m)
    marker.add_to(m)
    m.save('./FlyingOcerVeou.html')

curdoc().add_periodic_callback(update, 1000)

#session.show(m) # open the document in a browser

session.loop_until_closed() # run fodaline_width

'''
p = figure(x_axis_type="datetime",
               title="Le Céou",
               width=width, height=height)
p.line(t._dates, t._measurements, line_width=2)
html = file_html(p, CDN, "ceou")
iframe = IFrame(html, width=width+40, height=height+80)



popup = folium.Popup(iframe, max_width=2650)
icon = folium.Icon(color='green', icon='stats')
marker = folium.Marker(location=[44.7702502,1.1800149],
                           popup=popup,
                           icon=icon)
marker.add_to(m)
'''
