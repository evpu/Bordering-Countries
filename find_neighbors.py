# ************************************************************************
# Find neighboring countries and save to csv
# Python 2.7
# Map shapefile: http://www.naturalearthdata.com/downloads/110m-cultural-vectors
# https://github.com/evpu
# ************************************************************************

from osgeo import ogr
from shapely import wkt
import csv
import os

print(os.getcwd())
os.chdir('.')  # set working directory

# Create csv file where to save output
file = open('neighbors.csv', 'wb')
csv_file = csv.writer(file)
csv_file.writerow(['country_name', 'country_code', 'neighbor_name', 'neighbor_code'])


# Open the shapefile and get field names
source = ogr.Open('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp', update=False)
layer = source.GetLayer()
layer_defn = layer.GetLayerDefn()
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]

# Number of countries
count = layer.GetFeatureCount()

# Get country outlines
outline = {}
for i in range(count):
    country = layer.GetFeature(i)
    outline[i] = wkt.loads(country.GetGeometryRef().ExportToWkt())

# loop over countries
for i in range(count):
    country = layer.GetFeature(i)
    country_code = country.GetField("ADM0_A3")
    country_name = country.GetField("ADMIN")

    # loop over countries again to get neighbors
    for j in range(count):
        neighbor = layer.GetFeature(j)
        neighbor_code = neighbor.GetField("ADM0_A3")
        neighbor_name = neighbor.GetField("ADMIN")
        if outline[i].intersects(outline[j]) & (i != j):
            print '%s - %s' % (country_name, neighbor_name)
            csv_file.writerow([country_name, country_code, neighbor_name, neighbor_code])

file.close()
source = None
