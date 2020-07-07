


clear all
cd "C:\CHANGE THIS\2_BD\\"

unicode analyze "enaho01a-2018-500.dta"
unicode encoding set "ISO-8859-1"
unicode translate "enaho01a-2018-500.dta" 


cd "C:\CHANGE THIS\\"

global a "1_Do"
global b "2_BD"
global c "3_Temp"
global d "4_Tablas"


	use "$b\\enaho01a-2018-500.dta", clear
	merge m:1 nconglome conglome vivienda hogar ubigeo dominio estrato using "$b\sumaria-2018.dta", keepusing(mieperho factor07)
	drop _merge

	merge m:1 p505r4 using "$b\\Correspondencia INEI_ISCO_SOC.dta"
	fre p505r4 if _merge == 1
	drop if _merge == 2
	drop _merge
	
	gen year = 2018

	gen  	Sector4 = 1  if p506r4 >= 111 & p506r4 <= 322 
	replace Sector4 = 2  if p506r4 >= 510 & p506r4 <= 990 
	replace Sector4 = 3  if p506r4 >= 1010 & p506r4 <= 3320 
	replace Sector4 = 4  if p506r4 >= 3510 & p506r4 <= 3530 
	replace Sector4 = 5  if p506r4 >= 3600 & p506r4 <= 3900 
	replace Sector4 = 6  if p506r4 >= 4100 & p506r4 <= 4390 
	replace Sector4 = 7  if p506r4 >= 4510 & p506r4 <= 4799 
	replace Sector4 = 8  if p506r4 >= 4911 & p506r4 <= 5320 
	replace Sector4 = 9  if p506r4 >= 5510 & p506r4 <= 5630 
	replace Sector4 = 10 if p506r4 >= 5811 & p506r4 <= 6399
	replace Sector4 = 11 if p506r4 >= 6411 & p506r4 <= 6630
	replace Sector4 = 12 if p506r4 >= 6810 & p506r4 <= 6820
	replace Sector4 = 13 if p506r4 >= 6910 & p506r4 <= 7500
	replace Sector4 = 14 if p506r4 >= 7710 & p506r4 <= 8299
	replace Sector4 = 15 if p506r4 >= 8411 & p506r4 <= 8430
	replace Sector4 = 16 if p506r4 >= 8510 & p506r4 <= 8550
	replace Sector4 = 17 if p506r4 >= 8610 & p506r4 <= 8890
	replace Sector4 = 18 if p506r4 >= 9000 & p506r4 <= 9329
	replace Sector4 = 19 if p506r4 >= 9411 & p506r4 <= 9609
	replace Sector4 = 20 if p506r4 >= 9700 & p506r4 <= 9820
	replace Sector4 = 21 if p506r4 >= 9900 & p506r4 <= 9999
	
	#delimit;
	label define Sector4_eti
	1  "Agricultura, ganadería, silvicultura y pesca" 
	2  "Explotacion de minas y canteras" 
	3  "Industrias manufactureras" 
	4  "Suministro de electricidad, gas, vapor y aire acondicionado"
	5  "Suministro de agua, evacuación aguas residuales, gestión desechos y descontaminación" 
	6  "Construcción" 
	7  "Comercio" 
	8  "Transporte y almacenamiento" 
	9  "Actividades de alojamiento y servicio de comidas" 
	10 "Información y comunicaciones" 
	11 "Actividades financieras y de seguros" 
	12 "Actividades inmobiliarias" 
	13 "Actividades profesionales, científicas y ténicas" 
	14 "Actividades de servicios administrativos y de apoyo" 
	15 "Administracion publica y defensa, planes de seguridad social de afiliación obligatoria" 
	16 "Enseñanza (privada)" 
	17 "Actividades de atención, salud humana y de asistencia social" 
	18 "Actividades artísticas, de entretenimiento y recreativas" 
	19 "Otras actividades de servicios" 
	20 "Actividades de los hogares como empleadores" 
	21 "Actividades de organizaciones y órganos extraterritoriales";
	#delimit cr
	label values Sector4 Sector4_eti

	replace Sector4 = 4 if Sector4 == 5
	replace Sector4 = 18 if Sector4 == 19 | Sector4 == 20
	
	gen area=(estrato>=1 & estrato<=5)==1
	recode area (0=2) 
	label define area_eti 1 "Urbano" 2 "Rural"
	label values area area_eti
		
	foreach x in i524a1 d529t i530a d536 i538a1 d540t i541a d543 d544t{
	replace `x'=. if `x'>=999999
	}
	egen r6op    = rowtotal(i524a1 d529t i530a d536), m
	egen r6os    = rowtotal(i538a1 d540t i541a d543), m
	gen  r6ex    = d544t
	egen ing     = rowtotal(r6op r6os r6ex) if ocu500 == 1,m
	gen  ingreso = ing/12
	
	
	tab year [iw = fac500a] if ocu500 == 1
	tab ocu500 [iw = fac500a]
	tab Sector4 [iw = fac500a] if ocu500 == 1

	
	* Peru
	table Sector4 [iw = fac500a] if ocu500 == 1, c(mean ONET mean ingreso count year)
	mean ONET ingreso [iw = fac500a] if ocu500 == 1
	tab year [iw = fac500a] if ocu500 == 1
	
	preserve 
	gen contador = 1
	keep if ocu500 == 1
	collapse (mean) ONET APPENDIX ingreso (count) contador [iw = fac500a], by(Sector4)
	export excel using "$d\\180420_proximity.xls", sheet("stata1") sheetreplace firstrow(var) 
	restore 
	
	* Urbano
	table Sector4 [iw = fac500a] if (ocu500 == 1 & area == 1), c(mean ONET mean ingreso count year)
	mean ONET ingreso [iw = fac500a] if (ocu500 == 1 & area == 1)
	tab year [iw = fac500a] if (ocu500 == 1 & area == 1)
	
	preserve 
	keep if area == 1 
	gen contador = 1
	keep if ocu500 == 1
	collapse (mean) ONET APPENDIX ingreso (count) contador [iw = fac500a], by(Sector4)
	export excel using "$d\\180420_proximity.xls", sheet("stata2") sheetreplace firstrow(var) 
	restore 
	
	
*█	Quintiles de ingreso monetario

	preserve
	use "$b\sumaria-2018.dta", clear
	gen year = 2018
	keep year nconglome conglome vivienda hogar ubigeo dominio estrato gashog1d
	xtile quintile = gashog1d, n(5)
	save "$c\suma_2018.dta", replace
	restore
	
*█	Continuacion
	
	#delimit;
	merge m:1 year nconglome conglome vivienda hogar ubigeo dominio estrato 
	using "$c\suma_2018.dta", keepusing(quintile);
	#delimit cr


	* Primer y segundo quintil (urbano)
	table Sector4 [iw = fac500a] if (ocu500 == 1 & quintile <= 2 & area == 1), c(mean ONET mean ingreso mean mieperho count year)
	mean ONET ingreso [iw = fac500a] if (ocu500 == 1 & quintile <= 2 & area == 1)
	tab year [iw = fac500a] if (ocu500 == 1 & quintile <= 2 & area == 1)

	gen xxx = (Sector4 == 3 | Sector4 == 6 | Sector4 == 7 | Sector4 == 8 | Sector4 == 9 | Sector4 == 16 | Sector4 == 18) if (ocu500 == 1 & quintile <= 2 & area == 1)
	tab ocupinf [iw = fac500a] if xxx == 1
	
	tab Sector4 if (ocu500 == 1 & quintile <= 2 & area == 1), m
	
	preserve
	keep if xxx == 1
	collapse (count) xxx, by(year nconglome conglome vivienda hogar ubigeo dominio estrato)
	merge 1:1 nconglome conglome vivienda hogar ubigeo dominio estrato using "$b\sumaria-2018.dta", keepusing(mieperho factor07)
	keep if _merge == 3
	mean mieperho [iw = factor07]
	restore
	
	preserve 
	gen contador = 1
	keep if ocu500 == 1 & quintile <= 2 & area == 1 
	collapse (mean) ONET APPENDIX ingreso (count) contador [iw = fac500a], by(Sector4)
	export excel using "$d\\180420_proximity.xls", sheet("stata3") sheetreplace firstrow(var) 
	restore 

	* Tercer quintil
	table Sector4 [iw = fac500a] if (ocu500 == 1 & quintile == 3), c(mean ONET mean ingreso count year)
	mean ONET ingreso [iw = fac500a] if (ocu500 == 1 & quintile == 3)
	tab year [iw = fac500a] if (ocu500 == 1 & quintile == 3)
	
	preserve 
	gen contador = 1
	keep if ocu500 == 1 & quintile == 3
	collapse (mean) ONET APPENDIX ingreso (count) contador [iw = fac500a], by(Sector4)
	export excel using "$d\\180420_proximity.xls", sheet("stata4") sheetreplace firstrow(var) 
	restore 
	
	* Cuarto y quinto quintil
	table Sector4 [iw = fac500a] if (ocu500 == 1 & quintile >= 4), c(mean ONET mean ingreso count year)
	mean ONET ingreso [iw = fac500a] if (ocu500 == 1 & quintile >= 4)
	tab year [iw = fac500a] if (ocu500 == 1 & quintile >= 4)
	
	preserve 
	gen contador = 1
	keep if ocu500 == 1 & quintile >= 4
	collapse (mean) ONET APPENDIX ingreso (count) contador [iw = fac500a], by(Sector4)
	export excel using "$d\\180420_proximity.xls", sheet("stata5") sheetreplace firstrow(var) 
	restore 
	
	
	
