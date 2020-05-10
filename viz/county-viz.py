from urllib.request import urlopen
import pandas as pd
import json
import math
import plotly as py
import plotly.express as px
import plotly.graph_objects as go 
import geopy
from geopy.geocoders import Nominatim
import plotly.figure_factory as ff

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
dataset = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv', dtype=str)
dataset.sort_values(by='date')
# geocoder = Nominatim(user_agent='covid-map')
dataset['location'] = dataset['county'] + ", " + dataset['state']
# dataset.lat = dataset['location'].progress_apply(geocoder.geocode).apply(lambda x : x.latitude if x != None else None)
# dataset.long = dataset['location'].progress_apply(geocoder.geocode).apply(lambda x : x.longitude if x != None else None)
# print(dataset)
dataset['text'] = dataset['county'] +  ', ' + dataset['state'] +'<br>Cases: '+ dataset['cases'] + '<br>Deaths: '+ dataset['deaths']
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
dataset['statecode'] = dataset['state'].map(us_state_abbrev)
fig1 = px.choropleth(dataset, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale="Magma",
                           range_color=(0, 12),
                           scope="usa",
                           animation_frame='date')
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.show()
fig2 = px.choropleth(dataset, geojson=counties, locations='fips', color='deaths',
                           color_continuous_scale="Magma",
                           range_color=(0, 12),
                           scope="usa",
                           animation_frame='date')        
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()
# fig3 = px.scatter_geo(dataset, 
#                         locationmode = 'USA-states', 
#                         scope='usa', 
#                         lat=dataset.lat,
#                         lon=dataset.long,
#                         template = 'plotly_dark', 
#                         animation_frame = 'date', 
#                         size = dataset.deaths.astype(float) * 5, 
#                         hover_name='text'
#                     )