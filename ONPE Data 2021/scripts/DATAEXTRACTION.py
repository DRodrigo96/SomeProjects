# -*- coding: utf-8 -*-
"""
Created on Tue May 04 15:14:44 2021

@author: DavidRodrigo
"""


# PASO 2: SELENIUM

####################################################################################
####################################################################################

# PACKAGES
# ---------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


# CONSTANTES
# ---------------------------------------------------------------------------
txt_file = open('../input/LINKS.txt', 'r').readlines()
txt_file = [line.rstrip().split('-') for line in txt_file]

path = r'C:\Users\RODRIGO\Desktop\ONPEWS\TESTING'
xpath = '//*[@id="pdf"]/div/a[2]'
preferences = {'download.default_directory': path, 'safebrowsing.enabled': 'false'}

options = webdriver.ChromeOptions()
options.add_experimental_option ('prefs', preferences)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

time.sleep(3)

print('\nNAVEGADOR LISTO')


# BOT
# ---------------------------------------------------------------------------
for idl, line in txt_file[1203:]:
    print('HACIENDO: \n{}'.format(line))
    print('HACIENDO: \n{}'.format(line), file=open('../output/logs.txt', 'a'))

    time.sleep(random.uniform(4, 6))

    link = '{}'.format(line)    
    driver.get(link)

    time.sleep(5)

    try:
        driver.find_element(By.XPATH, xpath).click()
    except:
        print('NOT FOUND: {}\n'.format(idl))
        print('NOT FOUND: {}\n'.format(idl), file=open('../output/logs.txt', 'a'))
        print('{}\n'.format(idl), file=open('../input/NOTFOUND.txt', 'a'))
        continue

    x = int()
    thresh = 10
    maxwait = 3

    while x < thresh: 
        time.sleep(maxwait)
        x += 5
        print('Threshold:', thresh-x)    
        print('Threshold:', thresh-x, file=open('../output/logs.txt', 'a'))    
    
    print('DESCARGA COMPLETADA: {}\n'.format(idl))
    print('DESCARGA COMPLETADA: {}\n'.format(idl), file=open('../output/logs.txt', 'a'))


driver.close()

print('\nFIN FIN FIN\n')



