# intersect-shapes-grid

### Description
Demo code for:
- intersecting shapes/polygons with grid data
- visualizing the results
in Python (without PostGIS or other GIS software).

For intersecting only matplotlib standard functionality was used. Shapely lib was also tested, but turned out to be slower.
Intersecting here just means counting the number of grid points within a polygon.

In this example only dummy grid data and 3-digit post code shapes were used.
Post code shapes with full resolution are also included in the repo.
Instead of the used regular dummy grid data each other geo referenced point data can easily be implemented.

### Result
![Alt text](result.png?raw=true "Result")

### Source shape data
http://www.suche-postleitzahl.org/downloads
