"""
Created on Tue May 04 15:14:44 2021

@author: DavidRodrigo
"""


# PASO 2: PANDAS
####################################################################################
####################################################################################


# PACKAGES
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
import os
import glob

os.getcwd()


# DATA CLEANING
# ---------------------------------------------------------------------------
txt_file = open('../input/TERRITORIO.txt', 'r').readlines()
txt_file = [line.rstrip()for line in txt_file]

not_found = open('../input/NOTFOUND.txt', 'r').readlines()
not_found = [line.rstrip() for line in not_found]

found = [x[x.find(';')+1:] for x in txt_file if x[:x.find(';')] not in not_found]

csvfiles = glob.glob('../EXTRACTED/*.csv')
csvfiles.sort(key=os.path.getctime)


# DATAFRAME
# ---------------------------------------------------------------------------
df = pd.DataFrame()

for te, fi in zip(found, csvfiles):
    dataFile = pd.read_csv(fi, sep=',', encoding='ISO-8859-1', skiprows=10, skipfooter=29, header=None, engine='python')
    
    dataFile.columns = ['PARTIDO', 'TOTAL', 'PORCENTAJE_VALIDO']
    dataFile['UBICACION'] = te

    print(f'Appending: {fi}\n')
    df = df.append(dataFile)

df['PORCENTAJE_VALIDO'] = df['PORCENTAJE_VALIDO'] / 100


# --> DATA VALIDATION
# ---------------------------------------------------------------------------
len(df['PARTIDO'].unique())
len(df['UBICACION'].unique())
len(df) == len(df['PARTIDO'].unique()) * len(df['UBICACION'].unique())


# RESHAPE
# ---------------------------------------------------------------------------
df = df.pivot(index='UBICACION', columns='PARTIDO', values=['TOTAL', 'PORCENTAJE_VALIDO']).reset_index()
df.columns = ['{}_{}'.format(i,o) for o,i in df.columns]

df['_UBICACION'] = df['_UBICACION'].str.split('//')

for i, col in enumerate(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']):
    df[col] = df['_UBICACION'].apply(lambda y: pd.Series(y[i]))

df = df.sort_values(by=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])


# MERGE UBIGEO RENIEC
# ---------------------------------------------------------------------------
ubigeo = pd.read_pickle('../input/UBI_RENIEC.pkl')
df = df.merge(ubigeo, how='inner', on=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])


# ORDEN COLUMNAS
# ---------------------------------------------------------------------------
re = len(df.columns)-df.columns.get_loc("DEPARTAMENTO")
df = df[['UBIGEO_RENIEC', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'] + list(df.columns)[1:-re]]


# FINAL DATASET
# ---------------------------------------------------------------------------
df.to_csv(r'..\output\RESULTS.csv', sep=';', index_label='ID_DIS', encoding='ISO-8859-1')


# --> DATA VALIDATION
# ---------------------------------------------------------------------------
# Numero de provincias por departamento

dep = list(df['DEPARTAMENTO'].unique())

for x in dep:
    print(x, len(df[df['DEPARTAMENTO']==x]['PROVINCIA'].unique()))

# Notas:
# Loreto falta 1 provincia
df[df['DEPARTAMENTO']=='Loreto']['PROVINCIA'].unique()