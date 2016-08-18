#! /usr/bin/env python
# -*- coding: utf-8 -*-
    
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from folium.element import IFrame

import folium
# init d'un trajectoire
from trajectory import Trajectory

t = Trajectory()
t.load_json('/home/pprandi/Documents/hydrones/01_extraction/ceou.geojson')
print(t.source_file)
print(t._dates)
print(t._measurements)
#t.foliumShow('./test.html')

width, height = 500, 250

p = figure(x_axis_type="datetime",
               title="Le Céou",
               width=width, height=height)

p.line(t._dates, t._measurements, line_width=2)
html = file_html(p, CDN, "ceou")
iframe = IFrame(html, width=width+40, height=height+80)

m = folium.Map([43, 10], zoom_start=4, tiles='Stamen Toner')
folium.GeoJson(t.geojson).add_to(m)


popup = folium.Popup(iframe, max_width=2650)
icon = folium.Icon(color='green', icon='stats')
marker = folium.Marker(location=[44.7702502,1.1800149],
                           popup=popup,
                           icon=icon)
marker.add_to(m)
m.save("./test.html")
