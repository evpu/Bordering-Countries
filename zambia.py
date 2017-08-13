import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import os

print(os.getcwd())
os.chdir('.')  # set working directory

# ************************************************************************
# Get data about Zambia's neighbors
# ************************************************************************
neighbors = pd.read_csv('neighbors.csv')
neighbors = neighbors.loc[neighbors['country_name'] == 'Zambia', ['neighbor_name']]
neighbors = neighbors['neighbor_name'].tolist()


# ************************************************************************
# Plot
# ************************************************************************
plt.figure()

# load shapefile
sf = Basemap()
sf.readshapefile("ne_110m_admin_0_countries/ne_110m_admin_0_countries", "world")

# Fill oceans and lakes blue and land gold
sf.drawmapboundary(fill_color='#b2e2e2')
sf.fillcontinents(color='#fed98e', lake_color='#b2e2e2')

# get information about country names
country_names = []
for i in sf.world_info:
    country_names.append(i['admin'])

ax = plt.gca()

# Fill Zambia in purple
ax.add_patch(Polygon(sf.world[country_names.index('Zambia')], facecolor='#8856a7'))

# Fill its neighbors in pink
for i in neighbors:
    ax.add_patch(Polygon(sf.world[country_names.index(i)], facecolor='#f768a1'))

plt.savefig('zambia.png', dpi=200, bbox_inches='tight')
plt.show()
