import json

from datetime import datetime

import numpy as np
import geopandas as gpd
import pandas as pd

from bokeh.io import show, curdoc
from bokeh.models import LogColorMapper, LinearColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, ColorBar

from constants import *
from utils import flatten, load_counties, load_sus_data

# collor mapper
first_option = OPTIONS_NAME['Nº Tomografias Computadorizadas']

# defining control structures
year = Slider(start=YEARS[0], end=YEARS[-1],
              value=YEARS[0], step=1, title="Year")

genre = Select(title="Feature", value='Nº Tomografias Computadorizadas',
               options=list(OPTIONS_NAME.keys()))


br_counties = load_counties()
df = load_sus_data()

dff = df[df.year == '2014']
df_merged = br_counties.merge(dff, on='cod_municipio', how='left').fillna(0)

geodict = df_merged.to_dict('index')

# Defining constant values such as lat, long coordinates
# and counties names
county_xs = [county["lons"] for county in geodict.values()]
county_ys = [county["lats"] for county in geodict.values()]

county_names = [county['nome'] for county in geodict.values()]
county_uf = [county['uf'] for county in geodict.values()]


county_values = [geodict[county_id][first_option]
                 for county_id in geodict]

data = dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    uf=county_uf,
    value=county_values,
)
source = ColumnDataSource(data)

p = figure(
    title="Brazil SUS Information - Period: 2014-2018", 
    tools=TOOLS,
    x_axis_location=None, 
    y_axis_location=None,
    tooltips=TOOLTIPS,
    output_backend="webgl")

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

color_mapper = LinearColorMapper(palette=palette,
                              low=np.min(county_values),
                              high=np.max(county_values))
fill_color = {'field': 'value', 'transform': color_mapper}

patches = p.patches('x', 'y', source=source,
          fill_color=fill_color,
          fill_alpha=0.7, line_color="white", line_width=0.5)

# bar = ColorBar(color_mapper=color_mapper, location=(0,0))
# p.add_layout(bar, "left")

bar_data = df_merged[['nome', first_option]].nlargest(20, columns=[first_option]).values

data_h = dict(
    x=bar_data[:, 1],
    factors=bar_data[:, 0]
)
source_h = ColumnDataSource(data_h)

h = figure(x_range=source_h.data['factors'], plot_height=450,
           toolbar_location=None, tools="pan,reset,hover",
           tooltips=[("Nome", "@factors"), ("Total", "@x{int}")]
          )

h.vbar(x='factors', top='x', source=source_h, width=0.8, alpha=0.5)

h.xgrid.grid_line_color = None
h.xaxis.major_label_orientation = 1.2

def update_df(year):
    dff = df[df.year==str(year)]
    df_merged = br_counties.merge(
        dff, on='cod_municipio', how='left').fillna(0)

    return df_merged


def select_value():
    df_merged = update_df(year.value)
    genre_val = genre.value

    geodict = df_merged.to_dict('index')
    county_values = [geodict[county_id][OPTIONS_NAME[genre_val]]
                     for county_id in geodict]

    source.data['value'] = county_values
    color_mapper = LinearColorMapper(palette=palette,
                                     low=np.min(county_values),
                                     high=np.max(county_values))
    # bar.color_mapper = color_mapper
    patches.glyph.fill_color['transform'] = color_mapper

    p.tools[4].tooltips = [
        ("Name", "@name"),
        ("UF", "@uf"),
        (genre_val, "@value{int}")
    ]

    bar_data = df_merged[['nome', OPTIONS_NAME[genre.value]]].nlargest(20, columns=[OPTIONS_NAME[genre.value]]).values
    
    source_h.data['x'] = bar_data[:, 1]
    source_h.data['factors'] = bar_data[:, 0]
    h.x_range.factors = list(bar_data[:, 0])



controls = [genre, year]
for control in controls:
    control.on_change('value', lambda attr, old, new: select_value())

inputs = column(*controls, width=180, height=500)
inputs.sizing_mode = "fixed"

layout = layout([
    [inputs, p, h],
], sizing_mode='scale_width')

curdoc().add_root(layout)
curdoc().title = "DataSUS - Brazil"
