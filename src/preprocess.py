import os
import unidecode

import pandas as pd

DATAPATH = '../data/'

def kwargs_defaults_merge(defaults, kwargs):
    remaining_defaults = { k: v for k, v in defaults.items() if k not in kwargs.keys() }
    return { **remaining_defaults, **kwargs }

def read_to_df(filename, kwargs):
    filepath = os.path.join(DATAPATH, 'raw', filename)
    skiprows = 3 if filename == 'rf_leitos_de_internacao.csv' else 4

    kwargs = kwargs_defaults_merge(defaults={'encoding':'latin-1',
                                             'sep':';',
                                             'skiprows':skiprows},
                                   kwargs=kwargs)
    
    return pd.read_csv(filepath, **kwargs)


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
