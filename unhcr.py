# ************************************************************************
# Plot fractions of refugees to neighboring and to non-neighboring countries
# Data source: United Nations High Commissioner for Refugees (UNHCR) Population Statistics Reference Database
# http://popstats.unhcr.org/en/overview
# https://github.com/evpu
# ************************************************************************

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

print(os.getcwd())
os.chdir('.')  # set working directory

# ************************************************************************
# Load data
# ************************************************************************

data = pd.read_csv('unhcr_popstats_export_time_series_all_data.csv', skiprows=[0, 1, 2], dtype=str)

# For population type select only refugees
data = data.loc[data['Population type'] == 'Refugees (incl. refugee-like situations)', :]

# Keep only data in 2016
data = data.loc[data['Year'] == '2016', :]

# Drop rows with 0 and * (Redacted value, can be between 1 and 4)
data = data.loc[data['Value'] != '*', :]
data = data.loc[data['Value'] != '0', :]

data['Value'] = pd.to_numeric(data['Value'])
data['Year'] = pd.to_numeric(data['Year'])

# ************************************************************************
# Clean up: change country names so that they match 'neighbors.csv'
# ************************************************************************

# Clean up destination and origin countries
for X in ['Country / territory of asylum/residence', 'Origin']:
    data.loc[data[X] == 'Bahamas', X] = 'The Bahamas'
    data.loc[data[X] == 'Bolivia (Plurinational State of)', X] = 'Bolivia'
    data.loc[data[X] == 'Central African Rep.', X] = 'Central African Republic'
    data.loc[data[X] == "Côte d'Ivoire", X] = 'Ivory Coast'
    data.loc[data[X] == 'Dem. Rep. of the Congo', X] = 'Democratic Republic of the Congo'
    data.loc[data[X] == 'Congo', X] = 'Republic of Congo'
    data.loc[data[X] == 'Czech Rep.', X] = 'Czech Republic'
    data.loc[data[X] == 'Dominican Rep.', X] = 'Dominican Republic'
    data.loc[data[X] == 'Guinea-Bissau', X] = 'Guinea Bissau'
    data.loc[data[X] == 'Viet Nam', X] = 'Vietnam'
    data.loc[data[X] == 'Iran (Islamic Rep. of)', X] = 'Iran'
    data.loc[data[X] == 'Rep. of Korea', X] = 'South Korea'
    data.loc[data[X] == 'Timor-Leste', X] = 'East Timor'
    data.loc[data[X] == 'Palestinian', X] = 'Palestine'
    data.loc[data[X] == 'Rep. of Moldova', X] = 'Moldova'
    data.loc[data[X] == 'The former Yugoslav Republic of Macedonia', X] = 'Macedonia'
    data.loc[data[X] == "Lao People's Dem. Rep.", X] = 'Laos'
    data.loc[data[X] == "Dem. People's Rep. of Korea", X] = 'North Korea'
    data.loc[data[X] == 'Russian Federation', X] = 'Russia'
    data.loc[data[X] == 'Serbia and Kosovo (S/RES/1244 (1999))', X] = 'Republic of Serbia'
    data.loc[data[X] == 'Syrian Arab Rep.', X] = 'Syria'
    data.loc[data[X] == 'United Rep. of Tanzania', X] = 'United Republic of Tanzania'
    data.loc[data[X] == 'Venezuela (Bolivarian Republic of)', X] = 'Venezuela'

# ************************************************************************
# Merge in data on whether countries are neighboring or not and prepare for plotting
# ************************************************************************

neighbors = pd.read_csv('neighbors.csv')

# Sum up number of refugees to neighboring countries
to_neighbors = data.merge(neighbors, left_on=['Origin', 'Country / territory of asylum/residence'], right_on=['country_name', 'neighbor_name'], how='inner')
to_neighbors = to_neighbors.groupby(['Origin'])[['Value']].sum()
to_neighbors = to_neighbors.rename(columns={'Value': 'to_neighbors'})

# Sum up total number of refugees
total = data.groupby(['Origin'])[['Value']].sum()
total = total.rename(columns={'Value': 'total'})

# For plotting take top 15 counties by total number of refugees
to_plot = pd.concat([to_neighbors, total], axis=1)
to_plot = to_plot.sort_values(by=['total'], ascending=False).head(15)

# rewrite as percent
to_plot['to_neighbors'] = to_plot['to_neighbors'] / to_plot['total'] * 100
to_plot['total'] = 100
to_plot['country'] = to_plot.index

# ************************************************************************
# Plot
# ************************************************************************

# plot style settings
sns.set(style='white')
sns.set_color_codes('pastel')
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15

sns.barplot(x='total', y='country', data=to_plot, label='To non-neighboring countries', color='b')
sns.barplot(x='to_neighbors', y='country', data=to_plot, label='To neighboring countries', color='r')
plt.xlabel('')
plt.ylabel('')
plt.box(on=None)
plt.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.35, -0.05), fontsize=18)

plt.savefig('unhcr.png', dpi=400, bbox_inches='tight')
