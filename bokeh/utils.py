import json

from collections import Iterable

import pandas as pd
import geopandas as gpd
import numpy as np


def load_geojson(path):

    with open(path, "r") as fp:
        geojson = json.load(fp)

    for feature in geojson['features']:
        geo_id = feature['properties']['id']
        feature['id'] = geo_id

    return geojson


def flatten(x):
    if isinstance(x, Iterable) and isinstance(x[0], Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


def load_counties():
    br_counties = gpd.read_file('../data/external/shapefile_municipios/municipios_2010.shp',
                                encoding='latin-1')

    br_counties['cod_municipio'] = br_counties.codigo_ibg.apply(
        lambda x: x[:-1]).astype(int)

    br_counties['lat_lon'] = br_counties.geometry.apply(
        lambda x: np.array(flatten(x.__geo_interface__['coordinates'])))

    br_counties['lats'] = br_counties['lat_lon'].apply(
        lambda x: np.split(x, 2, axis=1)[1])

    br_counties['lons'] = br_counties['lat_lon'].apply(
        lambda x: np.split(x, 2, axis=1)[0])

    br_counties = br_counties.drop(['geometry', 'lat_lon'], axis=1)

    return br_counties

def load_sus_data():
    df = (pd.read_csv('../data/preprocessed/recursos_fis_hum_equi.csv',
                parse_dates=['data'])
            .assign(year=lambda x: x['data'].dt.strftime('%Y'))
            .drop(['municipio', 'data'], axis=1)
            )

    df_grp = (df.groupby(['cod_municipio', 'nom_municipio', 'year'], as_index=False).mean()
                .fillna(0)
                )

    return df_grp
