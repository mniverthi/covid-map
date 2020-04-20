from urllib.request import urlopen
import math
import json
import pandas as pd
import plotly
from plotly.graph_objs import *
import chart_studio.plotly as py
import plotly.offline as offile
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("sample_data_states.csv", dtype=str)
# min year in your dataset
# mindate = "2020-03-10"

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

# your color-scale
scl = [[0.0, '#ffffff'],[0.2, '#b4a8ce'],[0.4, '#8573a9'],
       [0.6, '#7159a3'],[0.8, '#5732a1'],[1.0, '#2c0579']] # purples
data_slider = []
for day in df.date.unique():
    dfadj = df[df['date'].astype(str) == day]
    
    for col in dfadj.columns:
        dfadj[col] = dfadj[col].astype(str)
        dfadj['text'] = dfadj['state'] +'Cases: '+ dfadj['cases'] + 'Deaths: '+ dfadj['deaths']
        dfadj['logcases'] = dfadj['cases'].astype(float).apply(lambda x : math.log(x, 10))
        dfadj.statecode = dfadj.state.map(us_state_abbrev)
        if (day < "2020-03-01"):
            print(dfadj)
        data = [ dict(
                    type='choropleth', # type of map-plot
                    colorscale = scl,
                    autocolorscale = False,
                    locations = dfadj.statecode, # the column with the state
                    z = dfadj.logcases.astype(float), # the variable I want to color-code
                    locationmode = 'USA-states',
                    hovertext = dfadj['text'], # hover text
                    marker = dict(     # for the lines separating states
                                line = dict (
                                        color = 'rgb(255,255,255)', 
                                        width = 2) ),               
                    colorbar = dict(
                                title = "Coronavirus Cases")
                    ) 
            ]
    data_slider.append(data)
steps = []
for i in range(len(data_slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)]) # label to be displayed for each step (year)
    step['args'][1][i] = True
    steps.append(step)
sliders = [dict(active=0, pad={"t": 1}, steps=steps)] 
layout = dict(geo=dict(scope='usa',
                projection={'type': 'albers usa'}),
                sliders=sliders)
fig = dict(data=data_slider, layout=layout)

plotly.offline.plot(fig)