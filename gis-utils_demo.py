from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gp
import rasterio
import gisutils
import matplotlib.pyplot as plt
import matplotlib as mpl; mpl.use('TkAgg')

# nhdplus_path = Path.home() / 'Documents/NHDPlus/'
#files = [nhdplus_path / 'NHDPlusGL/NHDPlus04/NHDSnapshot/Hydrography/NHDFlowline.shp',
#         nhdplus_path / 'NHDPlusMS/NHDPlus07/NHDSnapshot/Hydrography/NHDFlowline.shp']
files = ['C:/Users/esrag/Documents/GitHub/gis-utils/examples/data/NHDPlus07_flowline.shp']
# make the output folder
Path('output').mkdir(exist_ok=True)


crs = gisutils.get_shapefile_crs(files[0])
crs

df = gisutils.shp2df(files)


df.head()


gisutils.df2shp(df, 'output/combined.shp', crs=4269)


gisutils.df2shp(df.drop('geometry', axis=1), 'output/combined.dbf')


x5070, y5070 = gisutils.project((-91.87370, 34.93738), 4269, 5070)
x5070, y5070


gisutils.project((x5070, y5070), 5070, 4269)



df.geometry.values[0]



x, y = df.geometry.values[0].coords.xy
x, y


x, y = df.geometry.values[0].coords.xy
x3070, y3070 = gisutils.project((x, y), 4269, 3070)
x3070, y3070



geom_3070 = gisutils.project(df.geometry.values[0], 4269, 3070)
geom_4269 = gisutils.project(geom_3070, 3070, 4269)
geom_4269.almost_equals(df.geometry.values[0])



projected = gisutils.project(df.geometry, 4269, 3070)



from rasterio.plot import show
rasterfile = 'C:/Users/esrag/Documents/GitHub/gis-utils/examples/data/top.tif'

with rasterio.open(rasterfile) as src:
    show(src)



gisutils.projection.project_raster(rasterfile, 'output/projected.tif', 4269)

with rasterio.open('output/projected.tif') as src:
    show(src)



gisutils.projection.project_raster(rasterfile, 'output/projected_low_res.tif', 5070,
                                   resolution=1e4
                                   )
with rasterio.open('output/projected_low_res.tif') as src:
    show(src)


proj_str_3070 = (('+proj=tmerc +lat_0=0 +lon_0=-90 +k=0.9996 '
                 '+x_0=520000 +y_0=-4480000 +ellps=GRS80 '
                 '+datum=NAD83  +units=m +no_defs'))


crs_3070 = gisutils.get_authority_crs(proj_str_3070)
crs_3070


crs_3070 == gisutils.get_authority_crs(3070)

wkt_3070 = ('PROJCS["NAD83 / Wisconsin Transverse Mercator",'
            'GEOGCS["GCS_North_American_1983",'
            'DATUM["D_North_American_1983",'
            'SPHEROID["GRS_1980",6378137,298.257222101]],'
            'PRIMEM["Greenwich",0],'
            'UNIT["Degree",0.017453292519943295]],'
            'PROJECTION["Transverse_Mercator"],'
            'PARAMETER["latitude_of_origin",0],'
            'PARAMETER["central_meridian",-90],'
            'PARAMETER["scale_factor",0.9996],'
            'PARAMETER["false_easting",520000],'
            'PARAMETER["false_northing",-4480000],'
            'UNIT["Meter",1]]')


crs_3070 == gisutils.get_authority_crs(wkt_3070)


gisutils.raster.get_raster_crs(rasterfile)



with rasterio.open(rasterfile) as src:
    print(src.meta)



nrow, ncol = 700, 700
x = np.arange(ncol) * 1000 + 177955.0
y = 1604285.0 - (np.arange(nrow) * 1000)[::-1]
X, Y = np.meshgrid(x, y)

sampled = gisutils.get_values_at_points(rasterfile,
                                        x=X.ravel(), y=Y.ravel(),
                                        points_crs=None)
sampled = np.reshape(sampled, (nrow, ncol))


plt.pcolormesh(X, Y, sampled, shading='auto')
plt.gca().set_aspect(1)


from shapely.geometry import Point

stride = 10
geoms = [Point(x, y) for x, y in zip(X[::stride].ravel(), Y[::stride].ravel())]
df = gp.GeoDataFrame({'geometry': geoms,
                      'elevation': sampled[::stride].ravel()},
                      crs=5070)
df.to_file('output/sampled.shp')


gisutils.raster.points_to_raster('output/sampled.shp',
                                 data_col='elevation',
                                 output_resolution=1000,
                                 outfile='surface.tif')

with rasterio.open('surface.tif') as src:
    show(src)


with rasterio.open(rasterfile) as src:
    array = src.read(1)

plt.imshow(array)

xll = src.transform[2]
yll = src.transform[5] + src.height * src.transform[4]
xll, yll


gisutils.raster.write_raster('output/surface2.tif', array, xll=xll, yll=yll,
                             dx=1000, dy=1000, rotation=0, nodata=-9999,
                             crs = 5070)

with rasterio.open('output/surface2.tif') as src:
    show(src)

masked_array = np.ma.masked_array(array, array==-9999)
plt.imshow(masked_array)


gisutils.raster.write_raster('output/surface2.tif', masked_array, xll=xll, yll=yll,
                             dx=1000, dy=1000, rotation=0,
                             crs = 5070)