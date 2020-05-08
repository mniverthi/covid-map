import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go
import plotly as py

# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
dataset = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', dtype=str)
dataset['text'] = dataset['Country'] +'<br>Cases: '+ dataset['Confirmed'] + '<br>Deaths: '+ dataset['Deaths'] + '<br>Recovered: ' + dataset['Recovered']
dataset.sort_values(by='Date')
dataset['logcases'] = dataset['Confirmed'].astype(float).apply(lambda x : math.log(x, 10))
fig1 = px.choropleth(dataset, 
                        template = 'plotly_dark', 
                        locationmode = "country names", 
                        locations = 'Country', 
                        color = 'Confirmed', 
                        hover_name = 'text', 
                        animation_frame='Date', 
                        scope = 'world', 
                        labels={'Confirmed': 'Number of Cases'}, 
                        color_continuous_scale=px.colors.sequential.Plasma
                    )
fig2 = px.scatter_geo(dataset, 
                        scope='world', 
                        template = 'plotly_dark', 
                        locationmode = "country names", 
                        locations = 'Country', 
                        animation_frame = 'Date', 
                        size = dataset.Deaths.astype(float) * 5, 
                        hover_name='text'
                    )
data = []
layout = dict()
updatemenus = list([dict(buttons=list()), 
                    dict(direction='down',
                         showactive=True)])
total_codes = len(dataset.Country.unique()) * 3
dataset = dataset.sort_values(by=['Country'])
for s, country in enumerate(dataset.Country.unique()):
    dfadj = dataset[dataset['Country'] == country]
    # fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.cases), name='Cases in ' + state, mode='markers'))
    # fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.deaths), name='Deaths in ' + state, mode='markers'))
    data.append(dict(type = 'scatter', 
        x = list(dfadj.Date),
        y = list(dfadj.Confirmed),
        name = 'Cases in ' + country,
        mode = 'markers')
    )
    data.append(dict(type = 'scatter', 
        x = list(dfadj.Date),
        y = list(dfadj.Deaths),
        name = 'Deaths in ' + country,
        mode = 'markers')
    )
    data.append(dict(type = 'scatter', 
        x = list(dfadj.Date),
        y = list(dfadj.Recovered),
        name = 'Recoveries in ' + country,
        mode = 'markers')
    )
    visible_traces = [False] * total_codes
    visible_traces[3 * s] = True
    visible_traces[3 * s + 1] = True
    visible_traces[3 * s + 2] = True
    updatemenus[0]['buttons'].append(dict(args=[{'visible': visible_traces}],
                                          label=country,
                                          method='update'))
layout['updatemenus'] = updatemenus
fig3 = dict(data = data, layout = layout)
fig1.show()
fig2.show()
py.offline.plot(fig3)