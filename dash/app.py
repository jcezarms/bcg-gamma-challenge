# -*- coding: utf-8 -*-
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import geopandas as gpd

import utils


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

'''
~~~~~~~~~~~~~~~~
~~ LOADING DATA ~~
~~~~~~~~~~~~~~~~
'''

df_full = pd.read_csv('../data/preprocessed/recursos_fis_hum_equi.csv')
df_jan_2014 = df_full[df_full.data=='2014-01-01'].copy()

geojson = utils.load_geojson('data/brazil_counties.json')


gdf = gpd.read_file('../data/external/shapefile_municipios/municipios_2010.shp',
                    encoding='latin-1')
gdf['cod_municipio'] = gdf.codigo_ibg.apply(lambda x: x[:-1]).astype(int)

df_jan_2014 = df_jan_2014.merge(gdf, on='cod_municipio')
df_jan_2014['id'] = df_jan_2014['id'].astype(int)

token = "pk.eyJ1IjoidmljdG9ydnRyZCIsImEiOiJjazFwNHpja2cwdGI2M2RzN3EybWl3Z2QzIn0.gDjxI5E8q_26lG7NtRRB2w"


'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
           style=dict(
                 height='700px'
                ),
			id = 'choroplethmapbox',
			figure = dict(
				    data=[dict(
                        geojson=geojson,
                        locations=df_jan_2014['id'], 
                        z=df_jan_2014['rf_raios_x'],
                        colorscale="Viridis", 
                        zmin=0, 
                        zmax=100,
                        marker_opacity=0.5, 
                        marker_line_width=0,
                        type = 'choroplethmapbox'
				)],
				layout = dict(
                        mapbox = dict(
						accesstoken = token,
						style = 'light',
						center=dict(
							lat=-25.66,
							lon=-50.7129,
						),
						pitch=0,
						zoom=2.5
					)
                )
			)
		)
])

if __name__ == '__main__':
    app.run_server(debug=True)