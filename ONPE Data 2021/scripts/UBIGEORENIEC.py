# -*- coding: utf-8 -*-
"""
Created on Tue May 04 15:14:44 2021

@author: DavidRodrigo
"""


# PASO 1: LINKS UBIGEOS RENIEC
####################################################################################
####################################################################################


# DATA UBIGEOS
# ---------------------------------------------------------------------------
import pandas as pd, os

os.getcwd()

df = pd.read_excel('../input/UBIGEO_RENIEC.xlsx', sheet_name='ubigeo_reniec', dtype={'Ubigeo': str})
df = df[df.columns[:4]]


# UBIGEOS PARA LINKS HTML
# ---------------------------------------------------------------------------
# len('010000') # Departamento
# len('010100') # Provincia
# len('010101') # Distrito
# ---------------------------------------------------------------------------

df['departamento'] = df['Ubigeo'].str.slice(start=0, stop=2) + '0000'
df['provincia'] = df['Ubigeo'].str.slice(start=0, stop=4) + '00'
df['distrito'] = df['Ubigeo']


# TXT CON LINK HTML
# ---------------------------------------------------------------------------
dep = list(df['departamento'])
pro = list(df['provincia'])
dis = list(df['distrito'])
idl = [x for x in range(len(list(df['distrito'])))]

with open('../input/LINKS.txt', 'w') as txt_file:
    for de, pr, di, i in zip(dep, pro, dis, idl):
        txt_file.write('{}-https://www.resultados.eleccionesgenerales2021.pe/EG2021/EleccionesPresidenciales/RePres/P/{}/{}/{}\n'.format(i,de,pr,di))


# TXT CON NOMBRES DEPARTAMENTO, PROVINCIA, DISTRITO
# ---------------------------------------------------------------------------
dep = list(df['Departamento'])
pro = list(df['Provincia'])
dis = list(df['Distrito'])
idl = [x for x in range(len(list(df['distrito'])))]

with open('../input/TERRITORIO.txt', 'w') as txt_file:
    for de, pr, di, i in zip(dep, pro, dis, idl):
        txt_file.write('{};{}//{}//{}\n'.format(i,de,pr,di))


# TXT CON UBIGEOS RENIEC
# ---------------------------------------------------------------------------
df = df.sort_values(by=['Departamento', 'Provincia', 'Distrito'])

df = df[['Ubigeo', 'Departamento', 'Provincia', 'Distrito']]
df.columns = ['UBIGEO_RENIEC', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']

df.to_pickle('../input/UBI_RENIEC.pkl')