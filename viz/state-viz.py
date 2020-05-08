import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go
import plotly as py
dataset = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', dtype=str)
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

dataset['text'] = dataset['state'] +'<br>Cases: '+ dataset['cases'] + '<br>Deaths: '+ dataset['deaths']
dataset['logcases'] = dataset['cases'].astype(float).apply(lambda x : math.log10(x))
dataset['statecode'] = dataset['state'].map(us_state_abbrev)
dataset.sort_values(by='date')
fig1 = px.choropleth(dataset, template = 'plotly_dark', 
                        locationmode = "USA-states", 
                        locations = 'statecode', 
                        color = 'logcases', 
                        hover_name = 'text', 
                        animation_frame='date', 
                        scope = 'usa', 
                        labels={'cases': 'Number of Cases'}, 
                        color_continuous_scale=px.colors.sequential.Plasma
                    )
fig2 = px.scatter_geo(dataset, 
                        scope='usa', 
                        template = 'plotly_dark', 
                        locationmode = "USA-states", 
                        locations = 'statecode', 
                        animation_frame = 'date', 
                        size = dataset.deaths.astype(float) * 5, 
                        hover_name='text'
                    )
data = []
layout = dict()
updatemenus = list([dict(buttons=list()), 
                    dict(direction='down',
                         showactive=True)])
total_codes = len(dataset.state.unique()) * 2
dataset = dataset.sort_values(by=['state'])
for s, state in enumerate(dataset.state.unique()):
    dfadj = dataset[dataset['state'] == state]
    # fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.cases), name='Cases in ' + state, mode='markers'))
    # fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.deaths), name='Deaths in ' + state, mode='markers'))
    data.append(dict(type = 'scatter', 
        x = list(dfadj.date),
        y = list(dfadj.cases),
        name = 'Cases in ' + state,
        mode = 'markers')
    )
    data.append(dict(type = 'scatter', 
        x = list(dfadj.date),
        y = list(dfadj.deaths),
        name = 'Deaths in ' + state,
        mode = 'markers')
    )
    visible_traces = [False] * total_codes
    visible_traces[2 * s] = True
    visible_traces[2 * s + 1] = True
    updatemenus[0]['buttons'].append(dict(args=[{'visible': visible_traces}],
                                          label=state,
                                          method='update'))
layout['updatemenus'] = updatemenus

fig3 = dict(data = data, layout = layout)
fig1.show()
fig2.show()
py.offline.plot(fig3)
