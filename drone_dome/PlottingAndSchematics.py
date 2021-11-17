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

__all__ = ['PlottingAndSchematics']

class PlottingAndSchematics():
    
    def __init__(self):
        pass
    
    def render_dome(self, x_grid, y_grid, z_grid):
        '''
        x_grid, y_grid, z_grid: array
            the meshgrid output of the dome_points method of MakeDome
        '''
        
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(projection='3d')
        
        ax.plot_wireframe(x_grid, y_grid, z_grid) # just for rendering what flight grid should look like
        
        ax.set_aspect('auto')
        
        ax.set_title('Hemispherical Dome Grid', fontsize=25)
        ax.set_xlabel('x [m]', fontsize=20)
        ax.set_ylabel('y [m]', fontsize=20)
        ax.set_zlabel('z [m]', fontsize=20)
        
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='z', labelsize=12)
        
        plt.show()
        
        return fig, ax
    
    def diagnostics(self, ring_dataframe, arch_dataframe):
        '''
        ring_dataframe: pandas dataframe
            the output of the make_lat_lon_ring method of MakeCoords
            contains the points in the proper order to make the ring passes
        arch_dataframe: pandas dataframe
            the output of the make_lat_lon_arch method of MakeCoords
            contains the points in the proper order to make the arch passes
        
        expect the left hand column to look exactly like the right hand column, but rotated 90 degrees
            this is a sanity check to make sure the coordinate transform worked
        '''
        fig, ax = plt.subplots(2, 2, figsize=(10,10))

        ax[0,0].plot(ring_dataframe.x, ring_dataframe.y)
        ax[0,0].scatter(ring_dataframe.x, ring_dataframe.y, color='orange')
        ax[0,0].set_title('xy ring')
        
        ax[0,1].plot(ring_dataframe.longitude, ring_dataframe.latitude)
        ax[0,1].scatter(ring_dataframe.longitude, ring_dataframe.latitude, color='orange')
        ax[0,1].set_title('lat lon ring')
        
        ax[1,0].plot(arch_dataframe.x, arch_dataframe.y)
        ax[1,0].scatter(arch_dataframe.x, arch_dataframe.y, color='orange')
        ax[1,0].set_title('xy arch')
        
        ax[1,1].plot(arch_dataframe.longitude, arch_dataframe.latitude)
        ax[1,1].scatter(arch_dataframe.longitude, arch_dataframe.latitude, color='orange')
        ax[1,1].set_title('lat lon arch')
        
        return fig, ax
    
    def sat_plot(self, ring_dataframe, arch_dataframe, dish_longitude, dish_latitude):
        '''
        ring_dataframe: pandas dataframe
            the output of the make_lat_lon_ring method of MakeCoords
            contains the points in the proper order to make the ring passes
        arch_dataframe: pandas dataframe
            the output of the make_lat_lon_arch method of MakeCoords
            contains the points in the proper order to make the arch passes
        dish_longitude: float
            location of dish, or wherever the grid is centered, in DECIMAL DEGREES
        dish_latitude: float
            location of dish, or wherever the grid is centered, in DECIMAL DEGREES
        '''
        
        MAPBOX_KEY = "pk.eyJ1IjoiYW5uaWVwb2xpc2giLCJhIjoiY2p5b3BwdXl3MTdhdzNjdDRjbGw5MWJ6ciJ9.01NjskBuc2SQcm5QjbyLwA"
        MAPBOX_STYLE = "cjypy1k7x0ru71cjva7cs5iwz"
        MAPBOX_USERNAME = "anniepolish"
        PLOT_BG = cimgt.MapboxStyleTiles(MAPBOX_KEY, MAPBOX_USERNAME, MAPBOX_STYLE)
        BORDER = 0.00009 # if this cell takes forever to run, make border smaller
        
        # Create a Stamen terrain background instance.
        stamen_terrain = cimgt.Stamen('terrain-background')
        
        fig = plt.figure(figsize=(10,10))
        
        # Create a GeoAxes in the tile's projection.
        ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
        
        # Limit the extent of the map to a small longitude/latitude range.
        ax.set_extent([ring_dataframe.longitude.min()-BORDER, 
                       ring_dataframe.longitude.max()+BORDER, 
                       ring_dataframe.latitude.min()-BORDER, 
                       ring_dataframe.latitude.max()+BORDER], crs=ccrs.Geodetic())
        
        ax.add_image(PLOT_BG, 20)
        ax.set_aspect('equal')
        
        # Add a marker for the dish
        ax.plot(dish_longitude, dish_latitude, marker='o', color='red', markersize=15, alpha=0.7, transform=ccrs.Geodetic())
        
        # and plot the grid
        ax.plot(ring_dataframe.longitude, ring_dataframe.latitude, transform=ccrs.Geodetic(), color='magenta')
        ax.plot(arch_dataframe.longitude, arch_dataframe.latitude, transform=ccrs.Geodetic(), color='orange')
        
        plt.show()
        
        return fig, ax