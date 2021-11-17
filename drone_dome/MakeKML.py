import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import simplekml
import geopy
from geopy.distance import geodesic

#######################################################################################################################################

__all__ = ['MakeKML']

class MakeKML():
    
    def __init__(self):
        '''
        df: pandas dataframe
            output from make_lat_lon method of MakeCoords
        filename: string
            name of the flight path route, MUST HAVE .kml in filename
        '''
    
    def make_kml(self, df, filename):
        
        coord_list = []
        for i in range(len(df)):
            coord_list.append((df.longitude[i], df.latitude[i], df.z[i]))
        
        kml = simplekml.Kml()
        linestring = kml.newlinestring(name='route')
        linestring.coords = coord_list
        linestring.altitudemode = simplekml.AltitudeMode.relativetoground
        
        kml.save(filename)