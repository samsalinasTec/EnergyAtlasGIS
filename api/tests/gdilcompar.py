from osgeo import gdal
import pyproj
import geopandas as gpd
import rasterio
import shapely

print("GDAL:", gdal.VersionInfo())
print("PyProj:", pyproj.__version__)
print("GeoPandas:", gpd.__version__)
print("Rasterio:", rasterio.__version__)
print("Shapely:", shapely.__version__)
