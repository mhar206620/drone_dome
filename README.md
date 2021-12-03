# drone_dome

This code package generates two hemispherical grid flight paths as kml files that can be uploaded to Google Earth or a drone autopilot software such as UGCS (or any other map rendering software that takes kml). Two files are output: one creates a dome path that spirals in horizontal rings, and the other creates a dome path that rasters in a series of arches. The dome utilizes a "square" aspect ratio between horizontal and vertical passes: the angular separation between all generated points in the dome is the same. Currently, non-square apect ratios are not supported. 

drone_dome generates these dome grids in three stages: first it generates the dome grid in arbitrary xyz-space; second it converts these xyz coordinates to latitude/longitude/altitude coordinates in real space and places the coordinate sets in the correct order to form a physically sensible flight path; finally it writes the ordered coordinate sets to a kml file format and outputs the files. 



### Installation

This repo is located at https://github.com/mhar206620/drone_dome

To install:

All of the dependencies are pip installable with the package install EXCEPT cartopy. Before installing drone_dome, `conda install -c conda-forge cartopy` in the environment where you want to install drone_dome, then follow the steps below to install drone_dome.

1. In the github repo, click the green "code" button and copy the HTTPS link
2. Go to your terminal and navigate to the environment/directory where you would like to install drone_dome
3. In the terminal type `git clone <link you just copied from 1>` and then press enter. This will clone the repo from github and create a local copy of it on your computer, within the current directory. 
4. Next, cd into the new directory. You should see all the files from the github repo now on your computer. Inside this directory in your terminal, type `pip install -e .` to install the package!

### Using drone_dome
There are two options for using drone_dome to generate grids: either in a jupyter notebook or utilizing a gui.

##### Jupyter Notebook
Open the tutorial.ipynb file in your drone_dome directory. This will take you through all the steps required to generate a dome figure, generate latitude/longitude coordinates, and output kml files which can be read into Google Earth, UGCS, or any other program that does map rendering. 

##### Streamlit GUI
In your terminal, cd into your drone_dome directory. Type `streamlit run gui.py` and hit enter. This will open a gui in your browser window where you can input all of the dome parameters and output kml files, as above. Under the hood, this GUI is doing everything you see in the tutorial notebook.

