# dependency imports

import streamlit as st

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import simplekml
import geopy
from geopy.distance import geodesic

# package imports

from drone_dome import PlottingAndSchematics
from drone_dome import MakeDome
from drone_dome import MakeCoords
from drone_dome import MakeKML

#############################################################################################################################

st.title('Drone Dome')

# instantiate the PlottingAndSchematics class for future use
plots = PlottingAndSchematics()

#############################################################################################################################

# initialize the variables with default values
if 'angle_between_points' not in st.session_state:
    st.session_state.angle_between_points = 40
if 'height' not in st.session_state:
    st.session_state.height = 70
if 'radius' not in st.session_state:
    st.session_state.radius = 20
    
# initialize the form    
st.header('Generate Dome')

with st.form('make_dome'):
    # initialize the fields in the form
    abp = float(st.text_input(label='angle between points in degrees', value=40))
    h = float(st.text_input(label='height in meters AGL', value=70))
    r = float(st.text_input(label='radius in meters', value=20))
    
    submitted = st.form_submit_button(label='Generate Dome')
    
    if submitted:
        st.session_state.angle_between_points = abp
        st.session_state.height = h
        st.session_state.radius = r
        
        # passing all the form variables to the class to make the dome
        dome = MakeDome(angle_between_points=st.session_state.angle_between_points, height=st.session_state.height, radius=st.session_state.radius)
        
        x, y, z, theta, phi = dome.dome_points()
        st.session_state.x = x
        st.session_state.y = y
        st.session_state.z = z
        st.session_state.theta = theta
        st.session_state.phi = phi

        # rendering the dome in arbitrary space
        fig_dome, ax_dome = plots.render_dome(x, y, z)

        # creating the streamlit plot
        st.pyplot(fig_dome)

#############################################################################################################################

# initialize the variables with default values
if 'latitude' not in st.session_state:
    st.session_state.latitude = 41.320917
if 'longitude' not in st.session_state:
    st.session_state.longitude = -72.921917

st.header('Generate Coordinates')

with st.form('make_coords'):
    # initialize fields in the form
    lat = float(st.text_input('latitude in decimal degrees', value=41.320917))
    lon = float(st.text_input('longitude in decimal degrees', value=-72.921917))
    
    submitted = st.form_submit_button(label='Generate Coordinates')
    
    if submitted: 
        st.session_state.latitude = lat
        st.session_state.longitude = lon
        
        # passing all the form variables to the class to make the dome
        # do all the calculations to prepare the coordinates
        coords = MakeCoords(st.session_state.x, st.session_state.y, st.session_state.z, st.session_state.theta, st.session_state.phi, latitude=st.session_state.latitude, longitude=st.session_state.longitude)
        
        # generate the latitude/longitude coordinates of the ring passes
        df_ring = coords.make_lat_lon_ring()
        st.session_state.df_ring = df_ring
        
        # generate the latitude/longitude coordinates of the arch passes
        df_arch = coords.make_lat_lon_arch()
        st.session_state.df_arch = df_arch
        
        # plotting the dome grid over a satellite image of the coordinate locations
        fig_sat, ax_sat = plots.sat_plot(df_ring, df_arch, dish_longitude=st.session_state.longitude, dish_latitude=st.session_state.latitude)
        
        # creating the streamlit plot
        st.pyplot(fig_sat)
        
        st.write('NUMBER OF WAYPOINTS = ' + str(len(st.session_state.df_ring)))

#############################################################################################################################

st.header('Generate KML File')

file_form = st.form(key='make_form')

st.session_state.ring_file = file_form.text_input('ring path filename, must have .kml')
st.session_state.arch_file = file_form.text_input('arch path filename, must have .kml')

file_submit_button = file_form.form_submit_button(label='Generate KML Files')

if file_submit_button:

    # instantiate the MakeKML class
    kml = MakeKML()

    # generate separate files for the ring passes and the arch passes
    # this helps keep the number of waypoints in each file low
    # easy to upload second direction while still in the air
    kml.make_kml(st.session_state.df_ring, st.session_state.ring_file)
    kml.make_kml(st.session_state.df_arch, st.session_state.arch_file)
    
    st.write('files generated')