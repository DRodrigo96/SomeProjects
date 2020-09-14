Aquí hago un pequeño ejercicio demostrativo de evaluación de impacto de un programa social. Tomo el programa social Juntos y busco replicar un experimento aleatorio con la información de una encuesta a nivel de hogares. Toda la información es pública.

Uso Stata para realizar el ejercicio. Las bases de datos se pueden encontrar en http://iinei.inei.gob.pe/microdatos/. Son necesarias las bases:
* enaho01a-2015-300.dta (Código Módulo: 3, base anual 2015)
* enaho01a-2016-300.dta (Código Módulo: 3, base anual 2016)
* enaho01-2016-700.dta (Código Módulo: 37, base anual 2016)
* sumaria-2016.dta (Código Módulo: 34, base anual 2016)
* r_numbers.dta (lista de número aleatorios para replicación, se encuentra en este repositorio en la carpeta "Archivos")

Instrucciones para replicación:  
1) Crear una carpeta que contenga 4 carpetas nombradas de la siguiente manera:  
  "1_Do"  
  "2_BD"  
  "3_Temp"  
  "4_Tablas"  
2) En la carpeta "2_BD" colocar todas las bases de datos necesarias.
3) La carpeta "1_Do" sirve para guardar archivos .do; la carpeta "3_Temp", para almacenar archivos temporales; la "4_Tablas", para guardar tablas.
4) En el archivo "Juntos2016_SanchezN.do" que se encuentra en la carpeta "Archivos", solo cambiar las direcciones "cd" de acuerdo con las respectivas direcciones.
