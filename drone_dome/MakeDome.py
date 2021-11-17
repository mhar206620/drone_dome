import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import simplekml
import geopy
from geopy.distance import geodesic

######################################################################################################################################

__all__ = ['MakeDome']

class MakeDome():
    
    def __init__(self, angle_between_points, height, radius):
        '''
        angle_between_points: float
            the angular separation between all points in the grid
        height: float
            this is the height of the TOP of the dome (maximum altitude the flight will reach)
        radius: float
            the radius of the dome
            
        THE USER ONLY NEEDS TO RUN THE dome_points METHOD
        '''
        self.angle_between_points = angle_between_points
        self.height = height
        self.radius = radius
        
        self.theta_steps, self.phi_steps = self.grid_density()
        self.dome_bottom = self.height_offset()
    
    def grid_density(self):
        theta_steps = int(360 / self.angle_between_points + 1)
        phi_steps = int(theta_steps / 2)
        return theta_steps, phi_steps
        
    def height_offset(self):
        dome_bottom = self.height - self.radius # because dome height offset is computed from center of sphere, not top
        return dome_bottom
        
    def dome_points(self):
        # using linspace instead of arange because i want to include the endpoint
        theta_range = np.linspace(0, 2*np.pi, self.theta_steps) 
        phi_range = np.linspace(0, np.pi/2, self.phi_steps)
    
        theta, phi = np.meshgrid(theta_range, phi_range)
    
        x = self.radius * np.cos(theta) * np.sin(phi)
        y = self.radius * np.sin(theta) * np.sin(phi)
        z = self.radius * np.cos(phi) + self.dome_bottom
        
        return x, y, z, theta, phi