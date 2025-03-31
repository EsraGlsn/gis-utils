from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gp
import rasterio
import gisutils
import matplotlib.pyplot as plt
import matplotlib as mpl; mpl.use('TkAgg')
import matplotlib.font_manager as fm
import flopy
from rasterio.plot import show
from Figures import ReportFigures, basemap


rasterfile = 'F:/USGS/Combined/Elevations/bot_l9.tif'
# with rasterio.open('surface.tif') as src:
#     show(src)

sim = flopy.mf6.MFSimulation.load(sim_ws="C:/Users/esrag/Documents/GitHub/illinoisriverbasin/modflow_regional")

ilrb = sim.get_model('gwf-ilrb')
ilrb.modelgrid.crs = 5070

univers_fonts = [f for f in fm.findSystemFonts(fontpaths=None, fontext='ttf') if 'univers' in f.lower()]


#check for Univers in the system fonts
univers_fonts = [f for f in fm.findSystemFonts(fontpaths=None, fontext='ttf') if 'univers' in f.lower()]


#verify that matplotlib can find them
fm.findfont('Univers 67 Condensed')

plt.rcParams['pdf.fonttype']

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['pdf.fonttype']

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
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.it'] = 'Univers 67 Condensed : italic'
plt.title('Infiltration (meters/day)', fontname= 'Univers 67 Condensed')

# Task #1:
# We are not using flopy in this script.
# Can we overlay this shapefile to the map using the tools in this environment? (or can you add flopy to the environment to use this code)
flopy.plot.plot_shapefile( "F:/USGS/shapefiles/counties_5070.shp",
                           ax= ax, facecolor='none', edgecolor='k', linewidth=2, alpha=1 )

# Task #2:
# change the font on the figures to "Univers Condensed 67" using the functions from "getting Univers working.py"

# 3/11 legends, scale bar, county names with Mike etc

# map parameters
extent = [400000, 1770000, 850000, 2300000] # bounding box in Albers coordinates
projection_shapefile= "F:/USGS/shapefiles/counties_5070.shp"
parallels=[39,40,41,42,43,44] # lat/lon to include in tickmarks
meridians=[-92,-91,-90,-89,-88,-87]
tick_interval= 1

Map = basemap(extent=extent,
              epsg=5070, #projection_shapefile=projection_shapefile,
              parallels=parallels, meridians=meridians,
              subplots=(1,2),
              tick_interval=tick_interval)
# add a scale bar
Map.add_scalebar(loc=(.5, -.1))

# # add some base layers via shapefiles
# counties = Map.add_shapefile(counties_shp, alpha=0.5)
# lm = Map.add_shapefile(lakemichigan, fc='LightSkyBlue')



