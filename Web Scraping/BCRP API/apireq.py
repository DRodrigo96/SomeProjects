#!/usr/bin/env python3

# Author: David Sánchez


# PACKAGES
from pathlib import Path
import requests, json
import pandas as pd
import sys

# PRELIMINARES
Path("output").mkdir(parents=True, exist_ok=True)

txt = sys.argv[1]

# API SERIES
with open(txt) as f:
    file = [line.strip() for line in f]

for serie in file:
    try:
        # Request
        url = f'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{serie}/json/1940/2018/'

        req = requests.get(url)
        req.encoding = 'utf-8'

        # Dataframe
        df = (
            pd
            .json_normalize(req.json(), record_path='periods')
            .rename(columns={'name': 'DATE', 'values': serie})
        )

        # Values
        df[serie] = df[serie].str[0].astype('float')

        # Export CSV
        df.to_csv(f'output/{serie}.csv', sep=';', encoding='iso-8859-1', index=False)
    
    except:
        print(f'Problema con serie {serie}.')
        continue

print('\nFIN DE LA DESCARGA!\n')
