"""
Copyright (C) 2015 The HDF Group
Copyright (C) 2015 John Evans

This example code illustrates how to access and visualize a GES DISC OCO-2
Swath HDF5 file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python oco2_L2StdND_03945a_150330_B6000_150331024816.h5.py

The HDF file must either be in your current working directory or in a
directory specified by the environment variable HDFEOS_ZOO_DIR.
"""

import os

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


def run():

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    FILE_NAME = 'oco2_L2StdND_03945a_150330_B6000_150331024816.h5'
    if 'HDFEOS_ZOO_DIR' in os.environ.keys():
        FILE_NAME = os.path.join(os.environ['HDFEOS_ZOO_DIR'], FILE_NAME)

    with h5py.File(FILE_NAME, mode='r') as f:

        name = '/RetrievalResults/xco2'
        data = f[name][:]
        units = f[name].attrs['Units'][0]
        longname = f[name].attrs['Description'][0]

        # Get the geolocation data
        latitude = f['/RetrievalGeometry/retrieval_latitude'][:]
        longitude = f['/RetrievalGeometry/retrieval_longitude'][:]

    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 45))
    m.drawmeridians(np.arange(-180, 180, 45),
                    labels=[True, False, False, True])
    m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
              edgecolors=None, linewidth=0)
    cb = m.colorbar(location="bottom", format='%.1e', pad='10%')
    cb.set_label(units)

    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n{1}'.format(basename, longname))
    fig = plt.gcf()
    # plt.show()
    pngfile = "{0}.py.png".format(basename)
    fig.savefig(pngfile)

if __name__ == "__main__":
    run()