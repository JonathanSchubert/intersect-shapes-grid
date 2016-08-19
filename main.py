import numpy as np
import pandas as pd
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import shapefile
import time
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import warnings

##################################
# Define dummy grid data over Germany
##################################
lat_start = 5
lat_end = 15.1
lon_start = 47.0
lon_end = 55.1
step = 0.05
testpoint_grid = np.empty((0, 2), int)
for lat in np.arange(lat_start, lat_end, step):
    for lon in np.arange(lon_start, lon_end, step):
        testpoint_grid = np.vstack((testpoint_grid, [lat, lon]))
print('Created dummy grid:\t' + str(len(testpoint_grid)) + ' points')

# Read shapefile of post code areas
file = "shape_data/plz-3stellig/plz-3stellig"
# file = "shape_data/plz-2stellig/plz-2stellig"
# file = "shape_data/plz-gebiete/plz-gebiete"
sf = shapefile.Reader(file + '.shp')
records = sf.records()
shapes = sf.shapes()
print('Imported post codes:\t' + str(len(records)) + ' shapes')

##################################
# use matplotlib for counting grid points within post code area polygon
##################################
print('Start intersecting pc shapes with grid data...')
start_time = time.time()
pc_size = {}
for i in range(0, len(records)):
    path = mplPath.Path(shapes[i].points)
    pc = records[i][0]
    ext = path.get_extents()
    subset_points = testpoint_grid[
        (testpoint_grid[:, 0] >= (ext.extents[0] - 0.01)) &
        (testpoint_grid[:, 0] <= (ext.extents[2] + 0.01)) &
        (testpoint_grid[:, 1] >= (ext.extents[1] - 0.01)) &
        (testpoint_grid[:, 1] <= (ext.extents[3] + 0.01))]
    points_within_pc = path.contains_points(subset_points)
    pc_size[pc] = len(subset_points[points_within_pc])

pc_size_df = pd.DataFrame().from_dict(pc_size, orient='index')
pc_size_df.columns = ['n_gridpoits']
print("\t ...took %s seconds" % round((time.time() - start_time), 2))

##################################
# First plot
##################################
print('Start plotting...')
start_time = time.time()
fig = plt.figure(figsize=(33, 18))
bot, top, left, right = 5.85, 15.05, 47.25, 55.07
ax = fig.add_subplot(121, axisbg='w', frame_on=False)
ax.set_title('Dummy grid and post code shapes', fontsize=24, y=1.03)
m = Basemap(projection='merc', resolution='i',          # res: l, i, h
            llcrnrlat=left, llcrnrlon=bot,
            urcrnrlat=right, urcrnrlon=top)
m.fillcontinents(color='lightgray')

# Read shapefile
m.readshapefile(file, 'units', color='black')

# Add grid points to plot
x, y = m(testpoint_grid[:, 0], testpoint_grid[:, 1])
m.scatter(x, y, color='black', s=3, zorder=4)

##################################
# Second plot
##################################
ax2 = fig.add_subplot(122, axisbg='w', frame_on=False)
ax2.set_title("Number of grid points per post code area", fontsize=24, y=1.03)

# Prepare color mapping
num_colors = 20
cm = plt.get_cmap('gnuplot')
scheme = [cm(i / float(num_colors)) for i in range(num_colors)]
scheme = scheme[::-1]
bins = np.linspace(pc_size_df.min()[0], pc_size_df.max()[0], num_colors)
values = pc_size_df['n_gridpoits']
pc_size_df['bin'] = np.digitize(values, bins) - 1

# Read shapefile and assign colors
m.readshapefile(file, 'units', color='#000000')
for record, shape in zip(m.units_info, m.units):
    postcode = record['plz']
    if postcode not in pc_size_df.index:
        color = '#000000'
    else:
        color = scheme[pc_size_df.ix[postcode]['bin']]

    patches = [Polygon(np.array(shape), True)]
    pc = PatchCollection(patches, zorder=2)
    pc.set_facecolor(color)
    pc.set_edgecolor(color)
    ax2.add_collection(pc)

# Draw color legend
ax_legend = fig.add_axes([0.9, 0.15, 0.015, 0.7], zorder=3)
cmap = mpl.colors.ListedColormap(scheme)
cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=cmap, ticks=bins,
                               boundaries=bins, orientation='vertical')
cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

# Save figure
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.savefig('result.png', bbox_inches='tight')
print("\t... took %s seconds" % round((time.time() - start_time), 2))
