from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gp
import rasterio
import gisutils
import matplotlib.pyplot as plt
import matplotlib as mpl; mpl.use('TkAgg')
import flopy
from rasterio.plot import show

rasterfile = 'F:/USGS/Combined/Elevations/bot_l9.tif'
# with rasterio.open('surface.tif') as src:
#     show(src)

sim = flopy.mf6.MFSimulation.load(sim_ws="C:/Users/esrag/Documents/GitHub/illinoisriverbasin/modflow_regional")

ilrb = sim.get_model('gwf-ilrb')
ilrb.modelgrid.crs = 5070



# with rasterio.open(rasterfile) as src:
#     array = src.read(1)
# masked_array = np.ma.masked_array(array, array<=-999)
fig, ax = plt.subplots(figsize=(15,15))
#plt.imshow(masked_array)
#plt.imshow(array)

# plt.imshow(ilrb.rch.recharge.array[0,0,:,:])
ilrb_mf6 = flopy.plot.PlotMapView(model=ilrb, ax=ax, layer=8)

im = ilrb_mf6.plot_array(ilrb.rch.recharge.array[0,0,:,:])
plt.axis('scaled')



# Task #1:
# We are not using flopy in this script.
# Can we overlay this shapefile to the map using the tools in this environment? (or can you add flopy to the environment to use this code)
flopy.plot.plot_shapefile( "F:/USGS/shapefiles/counties_5070.shp",
                           ax= ax, facecolor='none', edgecolor='k', linewidth=2, alpha=1 )

# Task #2:
# change the font on the figures to "Univers Condensed 67" using the functions from "getting Univers working.py"

# 3/11 legends, scale bar,with Mike etc

# 3/17- the goal will be to add model data (I think the best way to do this will be as a raster exported from flopy)

