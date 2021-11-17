import setuptools

setuptools.setup(
    name='drone_dome',
    version='0.1',
    author='Maile Harris',
    author_email='maile.harris@yale.edu',
    description='generate a hemispherical gridded flight path for a drone, for import into UGCS autopilot software',
    packages=setuptools.find_packages(include=['drone_dome','drone_dome.*']),
    python_requires='>=3',
    install_requires=['numpy', 'matplotlib', 'pandas', 'cartopy', 'simplekml', 'geopy']
)

# pip installing cartopy is hard because it has a lot of dependencies
# better to conda install it: conda install -c conda-forge cartopy
# everything else is easy and pip installable