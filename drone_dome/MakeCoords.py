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

__all__ = ['MakeCoords']

class MakeCoords():
    
    def __init__(self, x, y, z, theta, phi, latitude, longitude):
        '''
        x: array
            2D meshgrid array containing all the x position data
        y: array
            2D meshgrid array containing all the y position data
        z: array
            2D meshgrid array containing all the z position data
        theta: array
            2D meshgrid array containing spherically parametrized location data
        phi: array
            2D meshgrid array containing spherically parametrized location data
        latitude: float
            the location where we want the dome to be centered IN DECIMAL DEGREES
        longitude: float
            the location where we want the dome to be centered IN DECIMAL DEGREES
            
        THE USER SHOULD ONLY INTERACT WITH THE make_lat_lon METHODS
        '''
        self.latitude = latitude
        self.longitude = longitude
        
        self.ring_coord_list = self.extract_ring_coordinate_sets(x, y, z, theta, phi)
        self.arch_coord_list = self.extract_arch_coordinate_sets(x, y, z, theta, phi)
        
        self.df_ring = self.make_ring_df()
        self.df_ring = self.distance_between_ring_points()
        self.df_arch = self.make_arch_df()
        self.df_arch = self.distance_between_arch_points()
        
################################################################################################################################
# MAKE THE RING PASSES
    
    def xy_at_ring(self, level, x, y, z, theta, phi):
        # extracts the location data from the meshgrid format to give it in ordered coordinate sets for every point at a given z
        ring_coords = [[i, j, k, t, p] for i,j,k,t,p in zip(x[level], y[level], z[level], theta[level], phi[level])]
        return ring_coords
    
    def extract_ring_coordinate_sets(self, x, y, z, theta, phi):
        # creates a list of all the coordinate points in ordered sets
        temp_list = []
        for p in range(len(phi)):
            ring_coords = self.xy_at_ring(p, x, y, z, theta, phi)
            temp_list.append(ring_coords)
        ring_coord_list = np.concatenate(temp_list)
        return ring_coord_list
    
################################################################################################################################
# MAKE THE ARCH PASSES

    def xy_at_arch(self, arch, x, y, z, theta, phi):
        arch_coords = [[i, j, k, t, p] for i,j,k,t,p in zip(x[:,arch], y[:,arch], z[:,arch], theta[:,arch], phi[:,arch])]
        return arch_coords
    
    def extract_arch_coordinate_sets(self, x, y, z, theta, phi):
    # creates a list of all the coordinate points in ordered sets
        temp_list = []
        for t in range(len(theta[0])):
            arch_coords = self.xy_at_arch(t, x, y, z, theta, phi)
            if t %2 == 1:
                temp_list.append(np.flip(arch_coords, axis=0).tolist())
            else:
                temp_list.append(arch_coords)
        arch_coord_list = np.concatenate(temp_list)
        return arch_coord_list
    
################################################################################################################################
# MAKE THE RING DATAFRAME

    def make_ring_df(self):
        # turning the list of coordinate points into a pandas dataframe for ease of use
        df_ring = pd.DataFrame(self.ring_coord_list, columns=['x', 'y', 'z', 'theta', 'phi'])
        return df_ring
    
    def distance_between_ring_points(self):
        
        dist_list = []
        
        for i in range(len(self.df_ring)):
            #dist = np.sqrt((self.df_ring.x[i] - self.df_ring.x[0])**2 + (self.df_ring.y[i] - self.df_ring.y[0])**2)
            dist = np.sqrt((self.df_ring.x[i] - 0)**2 + (self.df_ring.y[i] - 0)**2)
            dist_list.append(dist)
            
        self.df_ring['dist_from_center_km'] = np.array(dist_list)/1000
        
        df_ring = self.df_ring
        return df_ring
    
    def make_lat_lon_ring(self):
        # transform dome coords from arbitrary xyz space into lat lon

        lat_list = []
        lon_list = []

        for i in range(len(self.df_ring)):
            origin = geopy.Point(41.3209269, -72.9219232)
            destination = geodesic(kilometers=self.df_ring.dist_from_center_km[i]).destination(origin, np.degrees(self.df_ring.theta[i]))
            new_lat, new_lon = destination.latitude, destination.longitude
            lat_list.append(new_lat)
            lon_list.append(new_lon)
            
        self.df_ring['latitude'] = lat_list
        self.df_ring['longitude'] = lon_list
        
        df_ring = self.df_ring
        print('NUMBER OF WAYPOINTS = ' + str(len(df_ring)))
        return df_ring
    
################################################################################################################################
# MAKE THE ARCH DATAFRAME

    def make_arch_df(self):
        # turning the list of coordinate points into a pandas dataframe for ease of use
        df_arch = pd.DataFrame(self.arch_coord_list, columns=['x', 'y', 'z', 'theta', 'phi'])
        return df_arch
    
    def distance_between_arch_points(self):
        
        dist_list = []
        
        for i in range(len(self.df_arch)):
            #dist = np.sqrt((self.df_arch.x[i] - self.df_arch.x[0])**2 + (self.df_arch.y[i] - self.df_arch.y[0])**2)
            dist = np.sqrt((self.df_arch.x[i] - 0)**2 + (self.df_arch.y[i] - 0)**2)
            dist_list.append(dist)
            
        self.df_arch['dist_from_center_km'] = np.array(dist_list)/1000
        
        df_arch = self.df_arch
        return df_arch
    
    def make_lat_lon_arch(self):
        # transform dome coords from arbitrary xyz space into lat lon

        lat_list = []
        lon_list = []

        for i in range(len(self.df_arch)):
            origin = geopy.Point(self.latitude, self.longitude)
            destination = geodesic(kilometers=self.df_arch.dist_from_center_km[i]).destination(origin,
                                                                                            np.degrees(self.df_arch.theta[i]))
            new_lat, new_lon = destination.latitude, destination.longitude
            lat_list.append(new_lat)
            lon_list.append(new_lon)
            
        self.df_arch['latitude'] = lat_list
        self.df_arch['longitude'] = lon_list
        
        df_arch = self.df_arch
        print('NUMBER OF WAYPOINTS = ' + str(len(df_arch)))
        return df_arch