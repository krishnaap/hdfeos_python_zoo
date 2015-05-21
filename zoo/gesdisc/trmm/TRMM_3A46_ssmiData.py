"""
Copyright (C) 2014 The HDF Group
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a GESDISC TRMM 3A46
 file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python TRMM_3A46_ssmiData.py

The HDF file must either be in your current working directory or in a directory
specified by the environment variable HDFEOS_ZOO_DIR.

The netcdf library must be compiled with HDF4 support in order for this example
code to work.  Please see the README for details.
"""
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

USE_NETCDF4 = False


def run():

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    FILE_NAME = '3A46.080101.2.HDF'
    if 'HDFEOS_ZOO_DIR' in os.environ.keys():
        FILE_NAME = os.path.join(os.environ['HDFEOS_ZOO_DIR'], FILE_NAME)

    DATAFIELD_NAME = 'ssmiData'

    if USE_NETCDF4:

        from netCDF4 import Dataset

        nc = Dataset(FILE_NAME)
        data = nc.variables[DATAFIELD_NAME][0, 0, :, :].astype(np.float64)

    else:

        from pyhdf.SD import SD, SDC

        hdf = SD(FILE_NAME, SDC.READ)
        ds = hdf.select(DATAFIELD_NAME)
        data = ds[0, 0, :, :].astype(np.float64)

    # Consider 0 to be the fill value.
    # Must create a masked array where nan is involved.
    data[data == data[0, 0]] = np.nan
    datam = np.ma.masked_where(np.isnan(data), data)

    # The lat and lon should be calculated manually.
    # More information can be found at:
    # http://disc.sci.gsfc.nasa.gov/precipitation/documentation/TRMM_README/TRMM_3A46_readme.shtml
    latitude = np.arange(89.5, -89.51, -1)
    longitude = np.arange(0.5, 359.51, 1)

    # Draw an equidistant cylindrical projection using the low resolution
    # coastline database.
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=0, urcrnrlon=360)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 120, 30), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(0, 360, 45), labels=[0, 0, 0, 1])
    m.pcolormesh(longitude, latitude, datam, latlon=True)
    cb = m.colorbar()
    cb.set_label('Units: mm/hr')

    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n{1}'.format(basename, DATAFIELD_NAME))

    fig = plt.gcf()
    # plt.show()

    pngfile = "{0}.py.png".format(basename)
    fig.savefig(pngfile)

if __name__ == "__main__":
    run()
