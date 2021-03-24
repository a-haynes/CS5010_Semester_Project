# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:52:14 2021

@author: rbc6wr
"""

# Import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

dataset_url = 'https://raw.githubusercontent.com/a-haynes/CS5010_Semester_Project/main/datasets/cfb'

#Reading in the datasets
df_2013 = pd.read_csv(dataset_url + '13.csv')
df_2013.insert(1,'Year',2013)
df_2014 = pd.read_csv(dataset_url + '14.csv')
df_2014['Year'] = 2014
df_2015 = pd.read_csv(dataset_url + '15.csv')
df_2015['Year'] = 2015
df_2016 = pd.read_csv(dataset_url + '16.csv')
df_2016['Year'] = 2016
df_2017 = pd.read_csv(dataset_url + '17.csv')
df_2017['Year'] = 2017
df_2018 = pd.read_csv(dataset_url + '18.csv')
df_2018['Year'] = 2018
df_2019 = pd.read_csv(dataset_url + '19.csv')
df_2019['Year'] = 2019
df_2020 = pd.read_csv(dataset_url + '20.csv')
df_2020['Year'] = 2020

#Merging datasets into one dataframe
frames = [df_2013, df_2014, df_2015, df_2016, df_2017, df_2017, df_2018, df_2019,
          df_2020]
df_stats = pd.concat(frames)
df_stats = df_stats.dropna(axis=1)

df_stats['WinPct']=df_stats.Win / df_stats.Games

df_stats.Team = df_stats.Team.apply(lambda x: x.replace('St.', 'State'))
df_stats.Team=df_stats.Team.replace({"App State (Sun Belt)":"Appalachian State (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Fla. Atlantic (C-USA)":"Florida Atlantic (C-USA)"})
df_stats.Team=df_stats.Team.replace({"Ga. Southern (Sun Belt)":"Georgia Southern (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Massachusettes (FBS Independent)":"UMass (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"Western Ky. (C-USA)":"Western Kentucky (C-USA)"})
df_stats.Team=df_stats.Team.replace({"Western Mich. (MAC)":"Western Michigan (MAC)"})
df_stats.Team=df_stats.Team.replace({"Southern California (Pac-12)":"USC (Pac-12)"})
df_stats.Team=df_stats.Team.replace({"Connecticut (FBS Independent)":"UConn (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"ULM (Sun Belt)":"Louisiana–Monroe (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Army West Point (FBS Independent)":"Army (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"Northern Ill. (MAC)":"Norther Illinois (MAC)"})
df_stats.Team=df_stats.Team.replace({"Southern Miss. (C-USA)":"Southern Miss (C-USA)"})

#Pulling Team Info from Wikipedia
page = requests.get('https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs')
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the table div
table = soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')

# Finding the nth occurance of a substring in a string
def find_nth(string, substring, n):
    start = string.find(substring)
    while start >= 0 and n > 1:
        start = string.find(substring, start+len(substring))
        n -= 1
    return start

schools = {}
nicknames = {}
conferences = {}
team_names = {}

for team in rows[1:]:
    school = team.get_text()[find_nth(team.get_text(),'\n', 1)+1:
                                find_nth(team.get_text(),'\n', 2)]
    nickname = team.get_text()[find_nth(team.get_text(),'\n', 3)+1:
                                find_nth(team.get_text(),'\n', 4)]
    conference = team.get_text()[find_nth(team.get_text(),'\n', 11)+1:
                                find_nth(team.get_text(),'\n', 12)]
    if conference == 'Independent' :
        conference = 'FBS Independent'
    key = school + ' (' + conference + ')'
    schools[key] = school
    nicknames[key] = nickname
    conferences[key] = conference
    team_names[schools[key] + ' ' + nicknames[key]] = key
    

# Collect ESPN's FPI Page (Page containing links to all FBS teams)
page = requests.get('https://www.espn.com/college-football/fpi/_/season/2020')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the Table__TBODY div
team_table = soup.find(class_='Table__TBODY')

# Pull text from all instances of data-clubhouse-uid attribute
# within Table__TBODY div
all_team_items = team_table.find_all(attrs={"data-clubhouse-uid": True}) 

logos = {}

# Loop through the all_team_items element and get the logo links
for team in all_team_items:
        team_id = team['data-clubhouse-uid'].partition('t:')[2]
        team_logo = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
            + team_id + ".png&h=50&w=50"
        if (team.get_text() == 'Miami Hurricanes') :
            logos['Miami (FL) Hurricanes'] = team_logo
        elif (team.get_text() == 'Southern Mississippi Golden Eagles'):
            logos['Southern Miss Golden Eagles'] = team_logo
        elif (team.get_text() == 'UT San Antonio Roadrunners'):
            logos['UTSA Roadrunners'] = team_logo
        elif (team.get_text() == 'UL Monroe Warhawks'):
            logos['Louisiana–Monroe Warhawks'] = team_logo
        elif (team.get_text() == 'Florida International Panthers'):
            logos['FIU Golden Panthers'] = team_logo
        elif (team.get_text() == 'San José State Spartans'):
            logos['San Jose State Spartans'] = team_logo
        elif (team.get_text() == 'Hawai\'i Rainbow Warriors'):
            logos['Hawaii Rainbow Warriors'] = team_logo
        else:
            logos[team_names[team.get_text()]] = team_logo


indicators = []
for col in df_stats.columns:
    if col not in ['Year', 'Team'] :
        indicators.append(col)
identifiers = ['Year', 'Team', 'School', 'Nickname', 'Conference', 'Logo']       

df_stats.insert(1,'School',df_stats['Team'].map(schools))
df_stats.insert(1,'Nickname',df_stats['Team'].map(nicknames))
df_stats.insert(1,'Conference',df_stats['Team'].map(conferences))
df_stats['Logo'] = df_stats['Team'].map(logos)
df_stats = df_stats.dropna()

df_stats = df_stats.melt(id_vars=identifiers, value_vars=indicators)

df_stats = df_stats.rename(columns={"variable": "Indicator Name","value": "Value"})

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = df_stats['Indicator Name'].unique()

available_conferences = df_stats['Conference'].unique()

available_conferences = np.append(available_conferences,('FBS'))

available_years = df_stats['Year'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.Label(['X-variable Selection',dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Def.Rank'
            )]),
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.Label(['Y-variable Selection',dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='WinPct'
            )]),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
        
    html.Div([
        html.Label(['Conference Filter',dcc.Dropdown(
            id='conference-filter',
            options=[{'label': i, 'value': i} for i in available_conferences],
            value='FBS'
        )]),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}), 

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Virginia'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(
        html.Label(['Select Year',dcc.Dropdown(
        id='crossfilter-year--slider',
            options=[{'label': i, 'value': i} for i in available_years],
            value=2020
    )]), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])
        

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('conference-filter', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value, conference_value):
    dff = df_stats[df_stats['Year'] == year_value]
    
    if conference_value != 'FBS' :
        dff = dff[dff['Conference'] == conference_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['School'],
            opacity=0
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['School'])

    xmin = dff[dff['Indicator Name'] == xaxis_column_name]['Value'].min()
    
    xmax = dff[dff['Indicator Name'] == xaxis_column_name]['Value'].max()
    
    ymin = dff[dff['Indicator Name'] == yaxis_column_name]['Value'].min()
    
    ymax = dff[dff['Indicator Name'] == yaxis_column_name]['Value'].max()
    
    xlim = [xmin*.95, xmax*1.05]
    
    ylim = [ymin*.95, ymax*1.05]    

    fig.update_xaxes(title=xaxis_column_name, type='linear', showgrid=False)

    fig.update_yaxes(title=yaxis_column_name, type='linear',showgrid=False)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',
                      xaxis=dict(range=[xlim[0],xlim[1]]), 
                      yaxis=dict(range=[ylim[0],ylim[1]]))
    
    for x_cord, y_cord, path in zip(dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                          dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                          dff['Logo']):
        fig.add_layout_image(
        dict(
            source=path,
            xref="x",
            yref="y",
            x=x_cord,
            y=y_cord,
            sizex=(xmax-xmin)*0.1,
            sizey=(ymax-ymin)*0.1,
            opacity=1,
            xanchor="center", yanchor="middle",
            layer="below")
        ) 
       

    return fig


def create_time_series(dff, title, axis_name):

    fig = px.scatter(dff, x='Year', y='Value', labels={
                     "Value": axis_name})

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(showgrid=False)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_x_timeseries(hoverData, xaxis_column_name):
    school_name = hoverData['points'][0]['customdata']
    dff = df_stats[df_stats['School'] == school_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(school_name, xaxis_column_name)
    return create_time_series(dff, title, xaxis_column_name)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_y_timeseries(hoverData, yaxis_column_name):
    school_name = hoverData['points'][0]['customdata']
    dff = df_stats[df_stats['School'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    title = '<b>{}</b><br>{}'.format(school_name, yaxis_column_name)
    return create_time_series(dff, title, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)