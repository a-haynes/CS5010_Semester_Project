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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_indicators = df_cfb['Indicator Name'].unique()
available_conferences = df_cfb['Conference'].unique()
available_conferences = np.append(available_conferences,('FBS')) # Adding FBS for no filter
available_years = df_cfb['Year'].unique()

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
        id='crossfilter-year--dropdown',
            options=[{'label': i, 'value': i} for i in available_years],
            value=2020
    )]), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])
        

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--dropdown', 'value'),
     dash.dependencies.Input('conference-filter', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value, conference_value):
    sub_df = df_cfb[df_cfb['Year'] == year_value]
    if conference_value != 'FBS' :
        sub_df = sub_df[sub_df['Conference'] == conference_value]
    try :
        fig = px.scatter(x=sub_df[sub_df['Indicator Name'] == xaxis_column_name]['Value'],
                y=sub_df[sub_df['Indicator Name'] == yaxis_column_name]['Value'],
                hover_name=sub_df[sub_df['Indicator Name'] == yaxis_column_name]['School'],
                opacity=0
                )
    except :
        xaxis_column_name = 'Win'
        yaxis_column_name = 'Win'
        fig = px.scatter(x=sub_df[sub_df['Indicator Name'] == xaxis_column_name]['Value'],
                y=sub_df[sub_df['Indicator Name'] == yaxis_column_name]['Value'],
                hover_name=sub_df[sub_df['Indicator Name'] == yaxis_column_name]['School'],
                opacity=0
                )
    fig.update_traces(customdata=sub_df[sub_df['Indicator Name'] == yaxis_column_name]['School'])
    
    # Defining axis range so we can properly scale images
    xmin = sub_df[sub_df['Indicator Name'] == xaxis_column_name]['Value'].min()
    xmax = sub_df[sub_df['Indicator Name'] == xaxis_column_name]['Value'].max()
    ymin = sub_df[sub_df['Indicator Name'] == yaxis_column_name]['Value'].min()
    ymax = sub_df[sub_df['Indicator Name'] == yaxis_column_name]['Value'].max()
    xlim = [xmin*.95, xmax*1.05]
    ylim = [ymin*.95, ymax*1.05]
    
    # Hiding grids and changing axis titles to selected variables    
    fig.update_xaxes(title=xaxis_column_name, showgrid=False)
    fig.update_yaxes(title=yaxis_column_name, showgrid=False)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',
                      xaxis=dict(range=[xlim[0],xlim[1]]), 
                      yaxis=dict(range=[ylim[0],ylim[1]]))
    # Using team logos as points
    for x_cord, y_cord, path in zip(sub_df[sub_df['Indicator Name'] == xaxis_column_name]['Value'],
                          sub_df[sub_df['Indicator Name'] == yaxis_column_name]['Value'],
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
    sub_df = df_cfb[df_cfb['School'] == school_name]
    sub_df = sub_df[sub_df['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(school_name, xaxis_column_name)
    return create_time_series(sub_df, title, xaxis_column_name)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_y_timeseries(hoverData, yaxis_column_name):
    school_name = hoverData['points'][0]['customdata']
    sub_df = df_cfb[df_cfb['School'] == hoverData['points'][0]['customdata']]
    sub_df = sub_df[sub_df['Indicator Name'] == yaxis_column_name]
    title = '<b>{}</b><br>{}'.format(school_name, yaxis_column_name)
    return create_time_series(sub_df, title, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)