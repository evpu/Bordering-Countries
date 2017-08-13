# Finding neighboring countries
Using a map shapefile one can quickly find countries that are bordering each other.

The code in "find_neighbors.py" uses world shapefile from Natural Earth and outputs a csv with a list of countries and their neighbors.

For example, Afghanistan borders 6 other countries:

| country_name | country_code | neighbor_name | neighbor_code |
|:-------------|:-------------|:--------------|:--------------|
| Afghanistan  | AFG          | China         | CHN           |
| Afghanistan  | AFG          | Iran          | IRN           |
| Afghanistan  | AFG          | Pakistan      | PAK           |
| Afghanistan  | AFG          | Tajikistan    | TJK           |
| Afghanistan  | AFG          | Turkmenistan  | TKM           |
| Afghanistan  | AFG          | Uzbekistan    | UZB           |

And here are Zambia's neighbors highlighted on a map:

<img src="https://raw.githubusercontent.com/evpu/Bordering-Countries/master/zambia.png" alt="Zambia" width="600">

This allows to quickly count how many neighbors each country has:

    import pandas as pd
    neighbors = pd.read_csv('neighbors.csv')
    neighbors['country_name'].value_counts()

Result:

    Russia                              14
    China                               14
    Brazil                              10
    Democratic Republic of the Congo     9
    Germany                              9
    Republic of Serbia                   8
    United Republic of Tanzania          8
    France                               8
    Turkey                               8
    Zambia                               8
    Niger                                8
    Cameroon                             7
    Mali                                 7
    Iran                                 7
    Ukraine                              7
    ...

## Refugee flows to neighboring countries

To illustrate the use of information on neighboring / non-neighboring countries further, let's find out what share of people who applied for refugee status in 2016 did so in neighboring / non-neighboring countries relative to their country of origin, using data from the United Nations High Commissioner for Refugees (UNHCR).

In 2016, the majority of refugees applied for refugee status in their neighboring countries. For countries in fragile situations that are ongoing for a long time, the share of refugees who apply in non-neighboring countries tends to increase.

<img src="https://raw.githubusercontent.com/evpu/Bordering-Countries/master/unhcr.png" alt="Refugees in 2016: to neighboring / non-neighboring countries" width="600">

Source: the United Nations High Commissioner for Refugees (UNHCR) Population Statistics Reference Database
