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

st.header('Generate Dome')

dome_form = st.form(key='make_dome')

st.session_state.angle_between_points = float(dome_form.text_input(label='angle between points in degrees'))
st.session_state.height = float(dome_form.text_input(label='height in meters AGL'))
st.session_state.radius = float(dome_form.text_input(label='radius in meters'))

dome_submit_button = dome_form.form_submit_button(label='Generate Dome')

if dome_submit_button:
    
    # do all the calculations to prepare the dome
    dome = MakeDome(angle_between_points=st.session_state.angle_between_points, height=st.session_state.height, radius=st.session_state.radius)
    
    # generate the dome
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

st.header('Generate Coordinates')

coords_form = st.form(key='make_coords')

st.session_state.latitude = float(coords_form.text_input('latitude in decimal degrees'))
st.session_state.longitude = float(coords_form.text_input('longitude in decimal degrees'))

coords_submit_button = coords_form.form_submit_button(label='Generate Coordinates')

if coords_submit_button:
    
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