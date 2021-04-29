# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 03:14:27 2021

@author: rbc6wr
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px

from cfb_dataframe import df_cfb

external_stylesheets = ['https://codepen.io/shshaw/pen/vJNMQY.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Creating options for variable, conference filter, and year dropdown menus
available_indicators = df_cfb['Indicator Name'].unique()
available_conferences = df_cfb['Conference'].unique()
available_conferences = np.append(available_conferences,('FBS')) # Adding FBS for no filter
available_years = df_cfb['Year'].unique()


# Much of the app generation and update code is modified from the documentation
# and examples found on dash.plotly.com
app.layout = html.Div([
    html.Div([
        # Creating y-variable dropdown item
        html.Div([
            html.Label(['X-variable Selection',dcc.Dropdown(
                id='x-variable',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Def.Rank',
            )]),
        ],
        style={'width': '49%', 'display': 'inline-block', 'color':'#232D4B',
               'backgroundColor': '#E57200'}),
        # Creating y-variable dropdown item
        html.Div([
            html.Label(['Y-variable Selection',dcc.Dropdown(
                id='y-variable',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='WinPct'
            )]),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block',
                  'color':'#232D4B','backgroundColor': '#E57200'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }),
    # Creating conference filter dropdown item
    html.Div([
        html.Label(['Conference Filter',dcc.Dropdown(
            id='conference-filter',
            options=[{'label': i, 'value': i} for i in available_conferences],
            value='FBS'
        )]),
    ], style={'width': '98%', 'display': 'inline-block', 'backgroundColor': '#E57200',
              'color': '#232D4B','padding': '0 20'}), 
    # Creating x vs. y scatterplot
    html.Div([
        dcc.Graph(
            id='scatterplot',
            hoverData={'points': [{'customdata': 'Virginia'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 
              'padding': '0 20'}),
    # Creating x and y time series charts for selected team
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    # Creating year selection dropdown item
    html.Div(
        html.Label(['Select Year',dcc.Dropdown(
        id='year-filter',
            options=[{'label': i, 'value': i} for i in available_years],
            value=2020
    )]), style={'width': '49%', 'padding': '0px 20px 20px 20px', 'background':'#E57200',
              'color': '#232D4B'})
])
        
# Scatter-plot update 
@app.callback(
    dash.dependencies.Output('scatterplot', 'figure'),
    [dash.dependencies.Input('x-variable', 'value'),
     dash.dependencies.Input('y-variable', 'value'),
     dash.dependencies.Input('year-filter', 'value'),
     dash.dependencies.Input('conference-filter', 'value')])
def update_graph(x_variable, y_variable,
                 year_value, conference_value):
    sub_df = df_cfb[df_cfb['Year'] == year_value]
    if conference_value != 'FBS' :
        sub_df = sub_df[sub_df['Conference'] == conference_value]
    try :
        fig = px.scatter(x=sub_df[sub_df['Indicator Name'] == x_variable]['Value'],
                y=sub_df[sub_df['Indicator Name'] == y_variable]['Value'],
                hover_name=sub_df[sub_df['Indicator Name'] == y_variable]['School'],
                opacity=0
                )
    # In case a selected variable wasn't included in selected year
    # Default to Win vs. Win scatterplot
    except :
        x_variable = 'Win'
        y_variable = 'Win'
        fig = px.scatter(x=sub_df[sub_df['Indicator Name'] == x_variable]['Value'],
                y=sub_df[sub_df['Indicator Name'] == y_variable]['Value'],
                hover_name=sub_df[sub_df['Indicator Name'] == y_variable]['School'],
                opacity=0
                )
    fig.update_traces(customdata=sub_df[sub_df['Indicator Name'] == y_variable]['School'])
    
    # Defining axis range so we can properly scale images
    xmin = sub_df[sub_df['Indicator Name'] == x_variable]['Value'].min()
    xmax = sub_df[sub_df['Indicator Name'] == x_variable]['Value'].max()
    ymin = sub_df[sub_df['Indicator Name'] == y_variable]['Value'].min()
    ymax = sub_df[sub_df['Indicator Name'] == y_variable]['Value'].max()
    xlim = [xmin*.95, xmax*1.05]
    ylim = [ymin*.95, ymax*1.05]
    
    # Hiding grids and changing axis titles to selected variables    
    fig.update_xaxes(title=x_variable, showgrid=False)
    fig.update_yaxes(title=y_variable, showgrid=False)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',
                      xaxis=dict(range=[xlim[0],xlim[1]]), 
                      yaxis=dict(range=[ylim[0],ylim[1]]))
    # Using team logos as points
    for x_cord, y_cord, path in zip(sub_df[sub_df['Indicator Name'] == x_variable]['Value'],
                          sub_df[sub_df['Indicator Name'] == y_variable]['Value'],
                          sub_df['Logo']):
        fig.add_layout_image(
        dict(
            source=path,
            xref="x",
            yref="y",
            x=x_cord,
            y=y_cord,
            sizex=(xmax-xmin)*0.1, # Scaling image based on axis range
            sizey=(ymax-ymin)*0.1, # Scaling image based on axis range
            opacity=1,
            xanchor="center", yanchor="middle",
            layer="below")
        ) 
    return fig

# Create time series plot
def create_time_series(sub_df, title, axis_name):
    fig = px.scatter(sub_df, x='Year', y='Value', labels={
                     "Value": axis_name})
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

# y-variable Time series update
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('scatterplot', 'hoverData'),
     dash.dependencies.Input('x-variable', 'value')])
def update_x_timeseries(hoverData, x_variable):
    school_name = hoverData['points'][0]['customdata']
    sub_df = df_cfb[df_cfb['School'] == school_name]
    sub_df = sub_df[sub_df['Indicator Name'] == x_variable]
    title = '<b>{}</b><br>{}'.format(school_name, x_variable)
    return create_time_series(sub_df, title, x_variable)

# y-variable Time series update
@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('scatterplot', 'hoverData'),
     dash.dependencies.Input('y-variable', 'value')])
def update_y_timeseries(hoverData, y_variable):
    school_name = hoverData['points'][0]['customdata']
    sub_df = df_cfb[df_cfb['School'] == hoverData['points'][0]['customdata']]
    sub_df = sub_df[sub_df['Indicator Name'] == y_variable]
    title = '<b>{}</b><br>{}'.format(school_name, y_variable)
    return create_time_series(sub_df, title, y_variable)


if __name__ == '__main__':
    app.run_server(debug=False)