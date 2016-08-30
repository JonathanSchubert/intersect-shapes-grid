# intersect-shapes-grid

### Description
Demo code for:
- intersecting shapes/polygons with gridded data
- visualizing the results

in Python (without PostGIS or other GIS software).

For intersecting the spatial data only matplotlib standard functionality was used. Shapely lib was also tested, but turned out to be slower.
In our case intersecting just means counting the number of grid points within a polygon, all other and more complex aggregation would be easily implemented.

In this example only a dummy grid data and 3-digit post code shapes were used.
Post code shapes with full resolution are also included in the repository.
Instead of the used regular dummy grid data each other geo referenced point data can easily be implemented.

### Result
![Alt text](result.png?raw=true "Result")

### Source shape data
www.suche-postleitzahl.org/downloads

Raw data: © OpenStreetMap contributors
