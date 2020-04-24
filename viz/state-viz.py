import plotly.graph_objects as go
from urllib.request import urlopen
import pandas as pd
import json
import math
import plotly
import plotly.express as px
from plotly.subplots import make_subplots

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
dataset = pd.read_csv("./sources/datasets/sample_data_states.csv", dtype=str)
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
dataset['logcases'] = dataset['cases'].astype(float).apply(lambda x : math.log(x, 10))
dataset['statecode'] = dataset['state'].map(us_state_abbrev)

fig1 = px.choropleth(dataset, template = 'plotly_dark', locationmode = "USA-states", locations = 'statecode', color = 'logcases', 
    hover_name = 'text', animation_frame='date', scope = 'usa', labels={'logcases': 'Number of Cases'}, color_continuous_scale=px.colors.sequential.Plasma)
fig2 = px.scatter_geo(dataset, scope='usa', template = 'plotly_dark', 
    locationmode = "USA-states", locations = 'statecode', animation_frame = 'date', size = dataset.deaths.astype(float)*5, hover_name='text')
fig3 = go.Figure()


for state in dataset.state.unique():
    dfadj = dataset[dataset['state'] == state]
    fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.cases), name='Cases in ' + state, mode='markers'))
    fig3.add_trace(go.Scatter(x=list(dfadj.date), y=list(dfadj.deaths), name='Deaths in ' + state, mode='markers'))
fig1.show()
fig2.show()
# Add dropdown
# fig3.update_layout(
#     updatemenus=[
#         dict(
#             buttons=list([
#                 dict(
#                     args=["type", "cases"],
#                     label="Cases",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=["type", "deaths"],
#                     label="Deaths",
#                     method="restyle"
#                 )
#             ]),
#             direction="down",
#             pad={"r": 10, "t": 10},
#             showactive=True,
#             x=0.1,
#             xanchor="left",
#             y=1.1,
#             yanchor="top"
#         ),
#     ]
# )

# # Add annotation
# fig3.update_layout(
#     annotations=[
#         dict(text="Trace type:", showarrow=False,
#         x=0, y=1.085, yref="paper", align="left")
#     ]
# )
# data = [dict(type='choropleth',
#              locations = dataset['statecode'].astype(str),
#              z=dataset['total exports'].astype(float),
#              locationmode='USA-states', 
#              visible=True)]
fig3.show()
# # create the empty dropdown menu
# updatemenus = list([dict(buttons=list()), 
#                     dict(direction='down',
#                          showactive=True)])

# total_codes = len(dataset.code.unique()) + 1

# for s, state in enumerate(dataset.code.unique()):
#     # add a trace for each state
#     data.append(dict(type='scatter',
#                      x=[i for i in range(1980, 2016)],
#                      y=[i + random.random() * 100 for i in range(1980, 2016)],
#                      visible=False))
#     # add each state to the dropdown    
#     visible_traces = [False] * total_codes
#     visible_traces[s + 1] = True
#     updatemenus[0]['buttons'].append(dict(args=[{'visible': visible_traces}],
#                                           label=state,
#                                           method='update'))

# # add a dropdown entry to reset the map    
# updatemenus[0]['buttons'].append(dict(args=[{'visible': [True] + [False] *  (total_codes - 1)}],
#                                       label='Map',
#                                       method='update'))

# days = list((set(dataset['date'])))
# list.sort(days)
# print(days)
'''
# make figure
fig_dict = {
    "layout": {},
    "frames": []
}

# fill in most of layout
# fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
# fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
# fig_dict["layout"]["hovermode"] = "closest"
# fig_dict["layout"]["sliders"] = {
#     "args": [
#         "transition", {
#             "duration": 400,
#             "easing": "cubic-in-out"
#         }
#     ],
#     "initialValue": "2020-01-21",
#     "plotlycommand": "animate",
#     "values": days,
#     "visible": True
# }

fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons"
    }
]

sliders_dict = {
    "active": 0,
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Day:",
        "visible": True,
#        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
#    "len": 0.9,
#    "x": 0.1,
#    "y": 0,
    "steps": []
}

# make data
# make frames
for year in days:
    frame = {"data": [], "name": str(year)}
    for continent in continents:
        dataset_by_year = dataset[dataset["year"] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["lifeExp"]),
            "y": list(dataset_by_year_and_cont["gdpPercap"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["country"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["pop"])
            },
            "name": continent
        }
        
    --------------------------------------------------------------
'''
# for day in dataset.date.unique():
#     frame = {"name": str(day)}
#     dataset = dataset[dataset['date'].astype(str) == day]
#     for col in dataset.columns:
#         dataset[col] = dataset[col].astype(str)
# print(dataset)
#         fig = px.choropleth(dataset, locations='state', color='logcases',
#                            color_continuous_scale="balance",
#                            range_color=(0, 12),
#                            scope="usa",
#                            labels={'unemp':'unemployment rate'}
#                           )
#     fig_dict["frames"].append(frame)
#     slider_step = {"args": [
#         [day],
#         {"frame": {"duration": 300, "redraw": False},
#          "mode": "immediate",
#          "transition": {"duration": 300}}
#     ],
#         "label": day,
#         "method": "animate"}
#     sliders_dict["steps"].append(slider_step)

# fig_dict["layout"]["sliders"] = [sliders_dict]
# fig = go.Figure(fig_dict)