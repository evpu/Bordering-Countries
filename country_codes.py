# ************************************************************************
# Find country codes from shapefile attributes table and save to csv
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
file = open('country_codes.csv', 'wb')
csv_file = csv.writer(file)
csv_file.writerow(['country_name', 'country_code'])

# Open the shapefile and get field names
source = ogr.Open('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp', update=False)
layer = source.GetLayer()
layer_defn = layer.GetLayerDefn()
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]

# loop over countries
for i in range(layer.GetFeatureCount()):
    country = layer.GetFeature(i)
    country_code = country.GetField("ADM0_A3")
    country_name = country.GetField("ADMIN")
    csv_file.writerow([country_name, country_code])

file.close()
source = None
