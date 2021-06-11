#!/usr/bin/env python3

# Author: David Sanchez (DRodrigo96)

# Paso 1. Selenium
#---------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

path = r'C:\Users\RODRIGO\Desktop\MinsaData'
link = 'https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa'
xpath = '//*[@id="data-and-resources"]/div/div/ul/li/div/span/a'

options = webdriver.ChromeOptions()
preferences = {'download.default_directory': path, 'safebrowsing.enabled': 'false'}

options.add_experimental_option ('prefs', preferences)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get(link)
driver.find_element(By.XPATH, xpath).click()

x = int()
while x < 120: 
    time.sleep(30)
    x += 30
    print('Tiempo restante:', 120-x, 'segundos')

driver.close()
print('Descarga completa.')


# Paso 2. Pandas¶
#---------------------------------------------------------------------------------------------
import pandas as pd
import os

path = r'C:\Users\RODRIGO\Desktop\MinsaData'
os.chdir(path)

dataFile = pd.read_csv('positivos_covid.csv', sep=',', encoding='ISO-8859-1')
dataFile.head(3)

dataFile.loc[dataFile['DEPARTAMENTO'] == 'LIMA REGION', 'DEPARTAMENTO'] = 'LIMA'
print('Corregido.')

for x in ['PROVINCIA', 'DISTRITO']:
    condition = dataFile[x] == 'EN INVESTIGACIÓN'
    dataFile = dataFile[~condition]
print('Corregido.')

coor_link = 'https://raw.githubusercontent.com/DRodrigo96/SomeProjects/master/Contagio%20COVID-19/Coordenadas/COORDENADAS%20DISTRITAL.csv'
shapef = pd.read_csv(coor_link, sep=';', encoding='utf-8-sig')
print('Coordenadas cargadas.')


# Paso 3: Fuzzy Wuzzy
#---------------------------------------------------------------------------------------------
dataFile.sort_values(by=['DEPARTAMENTO','PROVINCIA','DISTRITO'], inplace=True)
dataFile['INDEX'] = list(zip(dataFile['DEPARTAMENTO'], dataFile['PROVINCIA'], dataFile['DISTRITO']))

shapef.sort_values(by=['DEPARTAMENTO','PROVINCIA','DISTRITO'], inplace=True)
shapef['INDEX'] = list(zip(shapef['DEPARTAMENTO'], shapef['PROVINCIA'], shapef['DISTRITO']))

dataFile_index = list(dataFile['INDEX'].unique())
shapef_index = list(shapef['INDEX'].unique())

not_in_shp = list()
for x in shapef_index:
    if x not in dataFile_index:
        not_in_shp.append(x)

print('Número de distritos con nombre diferente:', len(not_in_shp) - (len(shapef_index) - len(dataFile_index)))

from fuzzywuzzy import fuzz

x = fuzz.ratio("LIMA PORTILLO MANANTAY", 'LIMA PORTILLO MANANTAI')
if x > 80:
    print("Score: {}. It's a match!".format(x))

for x, y, z in not_in_shp:
    for a, b, c in dataFile_index:
        ratio = fuzz.ratio(str(y + ' ' + z), str(b + ' ' + c))
        if ratio >= 95:
            dataFile.loc[dataFile['PROVINCIA'] == b, 'PROVINCIA'] = y
            dataFile.loc[dataFile['DISTRITO'] == c, 'DISTRITO'] = z
        else:
            pass

dataFile.loc[dataFile['PROVINCIA'] == 'NAZCA', 'PROVINCIA'] = 'NASCA'
dataFile.loc[dataFile['DISTRITO'] == 'HUAY HUAY', 'DISTRITO'] = 'HUAY-HUAY'
dataFile.loc[dataFile['DISTRITO'] == 'SAN FCO DE ASIS DE YARUSYACAN', 'DISTRITO'] = 'SAN FRANCISCO DE ASIS DE YARUSYACAN'
dataFile.loc[dataFile['DISTRITO'] == 'SONDOR', 'DISTRITO'] = 'SONDORILLO'
dataFile.loc[dataFile['DISTRITO'] == 'CORONEL GREGORIO ALBARRACIN L.', 'DISTRITO'] = 'CORONEL GREGORIO ALBARRACIN LANCHIPA'
dataFile.loc[dataFile['DISTRITO'] == 'NAZCA', 'DISTRITO'] = 'NASCA'
dataFile.loc[dataFile['DISTRITO'] == 'ANDRES AVELINO CACERES D.', 'DISTRITO'] = 'ANDRES AVELINO CACERES DORREGARAY'

dataFile['INDEX'] = list(zip(dataFile['DEPARTAMENTO'], dataFile['PROVINCIA'], dataFile['DISTRITO']))

dataFile_index = list(dataFile['INDEX'].unique())
shapef_index = list(shapef['INDEX'].unique())

not_in_shp = list()
for x in shapef_index:
    if x not in dataFile_index:
        not_in_shp.append(x)

print('Número de distritos con nombre diferente:', len(not_in_shp) - (len(shapef_index) - len(dataFile_index)))

# Paso 4: Información Georreferenciada¶
#---------------------------------------------------------------------------------------------
# Collapse información a nivel de distrito
collapseData = dataFile.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']).agg({'FECHA_CORTE': 'count', 'EDAD': 'mean'})
collapseData.reset_index(inplace=True)

# collapseData nuevo index
collapseData['INDEX'] = collapseData[['DEPARTAMENTO','PROVINCIA', 'DISTRITO']].agg(' '.join, axis=1) 
collapseData.set_index('INDEX', inplace=True)
collapseData.drop(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'], axis=1, inplace=True)

# shapef nuevo index
shapef['INDEX'] = shapef[['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']].agg(' '.join, axis=1)
shapef.set_index('INDEX', inplace=True)

# Join de dataframes
dfGeoref = shapef.join(collapseData, how='left')

# Drop distritos sin datos
dfGeoref.dropna(inplace=True)


# Paso 5: Folium: Python, JavaScript, CSS & HTML
#---------------------------------------------------------------------------------------------
import folium
from folium import Map, Marker
from folium import plugins
from folium.plugins import MarkerCluster
from PIL import ImageFont
import json
from jinja2 import Template

latitude = dfGeoref['LATITUD']
longitude = dfGeoref['LONGITUD']
distrito = dfGeoref['DISTRITO']
provincia = dfGeoref['PROVINCIA']
departamento = dfGeoref['DEPARTAMENTO']
numero = dfGeoref['FECHA_CORTE']
edades = dfGeoref['EDAD']

class MarkerWithProps(Marker):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.marker(
            [{{this.location[0]}}, {{this.location[1]}}],
            {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }} 
                {%- endif %}
                }
            )
            .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)
    def __init__(self, location, popup=None, tooltip=None, icon=None,
                 draggable=False, props = None ):
        super(MarkerWithProps, self).__init__(location=location,popup=popup,tooltip=tooltip,icon=icon,draggable=draggable)
        self.props = json.loads(json.dumps(props))    

        
icon_create_function = """
    function(cluster) {

    var c = ' marker-cluster-';

    var markers = cluster.getAllChildMarkers();
    var sum = 0;
    for (var i = 0; i < markers.length; i++) {
        sum += markers[i].options.props.population;
    }
    var sum_total = sum;

    if (sum_total < 1600) {
        c += 'small';
    } else if (sum_total < 6000) {
        c += 'medium';
    } else {
        c += 'large';
    }

    return new L.DivIcon({ html: '<div><span style="font-size: 7pt">' + sum_total + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
    
    }
    """

# Coordenadas de Perú
coor_PE = (-8.043040, -75.534517)

try:
    usedTile = 'https://tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token='+'{token}'.format(token=open("JAWGMAP API KEY.txt", 'r').read())
except:
    usedTile = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'

# Mapa base
maPE = Map(
    coor_PE, 
    zoom_start = 5, 
    tiles=usedTile, 
    attr='''
    <a href="https://www.jawg.io/en/">JawgMaps</a>. 
    Fuente: <a href="https://www.datosabiertos.gob.pe/">datosabiertos.gob.pe</a>.
    Elaboración: <a href="https://www.linkedin.com/in/rodrigosanchezn/">David Sánchez</a>.
    '''
    )

# Marcadores en el mapa
contagio = MarkerCluster(icon_create_function=icon_create_function).add_to(maPE)
font = ImageFont.truetype('times.ttf', 12)

def colorcode(x):
    if x in range(0,1600):
        color = 'blue'
        icon = 'heartbeat'
    elif x in range(1601,6000):
        color = 'orange'
        icon = 'exclamation-circle'
    else:
        color = 'red'
        icon = 'fa-ambulance'
    return (color, icon)

for lat, lon, dep, pro, dis, num, edad in zip(latitude,longitude, departamento, provincia, distrito, numero, edades):
    contagio.add_child(MarkerWithProps(
        location=[lat,lon],
        icon=folium.Icon(color=colorcode(num)[0], icon=colorcode(num)[1], prefix='fa'),
        popup = folium.Popup(
            html='{}, {}, {}<br>Contagiados: {}<br>Edad promedio: {}'.format(dep,pro,dis,int(num),round(edad)),
            max_width=font.getsize(dep+pro+dis+' '*4)[0], min_width=font.getsize(dep+pro+dis+' '*4)[0],
            sticky=True),
        tooltip=folium.Tooltip('{}, {}, {}<br>Contagiados: {}<br>Edad promedio: {}'.format(dep,pro,dis,int(num),round(edad))),
        props = { 'population': num}
    ))

item_txt = """<br> &nbsp; <i class="fa fa-map-marker fa-2x" style="color:{col}"></i> &nbsp; {item}"""
item_clu = """<br> &nbsp; <i class="fa fa-circle-o fa-lg" aria-hidden="true" style="color:{col}"></i> &nbsp; {item}"""
itms_1 = item_txt.format(item="Menos de 1600", col="#82CAFA")
itms_2 = item_txt.format(item="Entre 1600 y 6000", col="orange")
itms_3 = item_txt.format(item="Más de 6000", col="red")
itms_4 = item_clu.format(item="Contagios en el área", col="green")

legend_html = '''
    <div style="
    position: fixed; 
    top: 120px; left: 20px; width: 150px; height: 100px; margin:0 auto;
    border:2px solid grey; z-index:9999; 
    background-color:white;
    opacity: .55;
    font-size:10px;
    font-weight: bold;
    line-height: 12px
    "> 
    &nbsp; 
    {itm_txt_4}
    {itm_txt_1}
    {itm_txt_2}
    {itm_txt_3}
    </div> '''.format(itm_txt_1=itms_1, itm_txt_2=itms_2, itm_txt_3=itms_3, itm_txt_4=itms_4)

title_html = '''
    <div style="
    position: fixed; 
    top: 80px; left: 10px; width: 260px; 
    height: 35px; line-height: 35px; text-align: center;
    border:2px solid grey; z-index:9999; 
    border-radius: 25px;
    background-color:white;
    opacity: .55;
    font-size:12px;
    font-family: fantasy; 
    "> 
    {title}
    </div> '''.format(title="COVID-19 en Perú, contagios por distrito")

maPE.get_root().html.add_child(folium.Element(legend_html))
maPE.get_root().html.add_child(folium.Element(title_html))

maPE.save("COVID19.html")
maPE

import webbrowser
webbrowser.open("COVID19.html",new=2)
