import os
import unidecode
import shapefile


import pandas as pd

DATAPATH = '../data/'

def read_to_df(filename):
    filepath = os.path.join(DATAPATH, 'raw', filename)
    skiprows = 3 if filename == 'rf_leitos_de_internacao.csv' else 4
    
    return pd.read_csv(filepath, encoding='latin-1', sep=';', skiprows=skiprows)


def normalize_columns(df):
    df = df.rename(columns=lambda x: unidecode.unidecode(x.lower()))

    return df


def filter_rows(df):
    idx_total = df[df['municipio'] == 'Total'].index[0]
    df = df.iloc[:idx_total, :]

    return df


def melt(df, filename):
    df_melted = (df.melt(id_vars=['municipio'],
                        var_name='data_' + filename[:-4],
                        value_name=filename[:-4])
                   .rename(columns={'municipio': 'municipio_' + filename[:-4]})
                   )

    return df_melted


def combine(files):
    dfs_list = list()
    for file in files:

        df = read_to_df(file)
        df = normalize_columns(df)
        df = filter_rows(df)
        df = melt(df, file)
        dfs_list.append(df)

    return pd.concat(dfs_list, axis=1)
	

def to_date(df, cols_to_transform, period='DAY'):
    if period == 'DAY':
        df[cols_to_transform] = df[cols_to_transform].apply(lambda x: pd.to_datetime(x, format='%Y%m%d', errors='coerce'))
    elif period == 'MONTH':
        df[cols_to_transform] = df[cols_to_transform].apply(lambda x: pd.to_datetime(x, format='%Y%m').dt.to_period('M'))
    return df
