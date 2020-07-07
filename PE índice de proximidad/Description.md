Me baso en el trabajo «Characteristics of Workers in Low Work-From-Home and High Personal-Proximity Occupations» (Mongey & Weinberg, 2020) para elaborar un indicador de proximidad física por cada sector de la economía peruana. Discuto un poco la coyuntura nacional y la informalidad. Toda la información es pública.

Uso Stata para realizar el ejercicio. Las bases de datos se pueden encontrar en http://iinei.inei.gob.pe/microdatos/. Son necesarias las bases:
* enaho01a-2018-500.dta (Código Módulo: 5, base anual 2018)
* sumaria-2018.dta (Código Módulo: 34, base anual 2018)
* Correspondencia INEI_ISCO_SOC.dta (códigos de correspondencia entre clasificaciones internacionales de ocupaciones, la base se encuentra en este repositorio en la carpeta "Archivos")

Instrucciones para replicación:  
1) Crear una carpeta que contenga 4 carpetas nombradas de la siguiente manera:  
  "1_Do"  
  "2_BD"  
  "3_Temp"  
  "4_Tablas"  
2) En la carpeta "2_BD" colocar todas las bases de datos necesarias.
3) La carpeta "1_Do" sirve para guardar archivos .do; la carpeta "3_Temp", para almacenar archivos temporales; la "4_Tablas", para guardar tablas.
4) En el archivo "ProximityIndex_Sánchez Navarro.do" que se encuentra en la carpeta "Archivos", solo cambiar las direcciones "cd" de acuerdo con las respectivas direcciones.
