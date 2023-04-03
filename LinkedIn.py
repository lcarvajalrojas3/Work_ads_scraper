from selenium import webdriver
from selenium.webdriver.common.by import By
import time as timer
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import random
import cv2
import pytesseract
import base64
import numpy as np
import win32gui
import win32con

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-infobars")

exp_opt = ["enable-logging", "enable-automation", "ignore-certificate-errors"]
options.add_experimental_option("excludeSwitches", exp_opt)

def opendriver():
    driver = webdriver.Chrome(options=options)
    return driver

def create_folders(keyword):
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath("__file__"))
    print("path local: ", dir_path)
    folderpath = "LinkedIn"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta LinkedIn creada")
    else: print("Carpeta LinkedIn existente")
    dir_path = folderpath 
    folderpath = keyword.replace(" ", "_") + "_" + str(datetime.now().date())
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    else: print("Subcarpeta Data Existente")
    return folderpath

def login(driver, mail, clave):
    userdiv = driver.find_element(By.XPATH,'//*[@autocomplete="username"]')
    userdiv.click()
    userdiv.clear()
    userdiv.send_keys(mail)

    passdiv = driver.find_element(By.XPATH,'//*[@autocomplete="current-password"]')
    passdiv.click()
    passdiv.clear()
    passdiv.send_keys(clave)

    driver.find_element(By.XPATH,'//*[@type="submit"]').click()
    timer.sleep(1)
    print("Cuenta Logueada\n")
    timer.sleep(2)

def busqueda(driver, keyword):
    searchdiv = driver.find_element(By.XPATH,'//*[@aria-label="Busca por cargo, aptitud o empresa"]')
    searchdiv.click()
    searchdiv.clear()
    searchdiv.send_keys(keyword)
    timer.sleep(1)
    searchdiv.send_keys(Keys.RETURN)

    timer.sleep(1)
    print(f"Búsqueda de {keyword} realizada\n")
    timer.sleep(2)

"""def make_it_work():
    now_time = datetime.datetime.now().time()
    print(now_time)
    # get the time interval for the current iteration
    ventana_apertura = generar_ventana_apertura()
    interval = ventana_apertura[0]
    #interval = 1
    print("tiempo de iteración: ", interval)
    #print(ventanas_apertura[0:5])
    #ventanas_apertura = ventanas_apertura[1:]
    #print(ventanas_apertura[0:5])
    
    start_datetime = datetime.datetime.combine(datetime.date.today(), now_time)
    
    end_datetime = start_datetime + datetime.timedelta(minutes=interval)
    
    start_datetime = start_datetime.time()
    print("momento de inicio: ", start_datetime)
    end_datetime = end_datetime.time()
    print("momento de fin: ", end_datetime)
    while now_time >= start_datetime and now_time <= end_datetime:
        now_time = datetime.datetime.now().time()
        #now_time = datetime.datetime.combine(datetime.date.today(),datetime.datetime.now().time()).time()
        print(now_time)
        timer.sleep(5)"""

def generar_ventana_apertura():
    lower_bound = 5
    upper_bound = 30
    size = 10000
    
    # generate random numbers with a mixture of two normal distributions
    # with different means and variances
    x1 = np.random.normal(loc=12, scale=3, size=int(size*0.65))
    x2 = np.random.normal(loc=22, scale=3, size=int(size*0.15))
    x3 = np.random.normal(loc=28, scale=3, size=int(size*0.1))
    x4 = np.random.normal(loc=28, scale=3, size=int(size*0.1))
    x = np.concatenate((x1, x2, x3))
    np.random.shuffle(x)

    # clip the random numbers to the desired range
    x = np.clip(x, lower_bound, upper_bound)
    
    return x.astype(int).tolist()

##### Función de horario de funcionamiento -> CORE
##### f(x) Öffnungszeiten
##### f(x) operating hours

current_time = datetime.datetime.now().time()
print(current_time)
random_minute = random.randint(30, 59)
start_time = datetime.time(hour=2, minute=random_minute)
end_time = datetime.time(hour=22, minute=random.randint(30, 59))

while True:

    if current_time >= start_time and current_time <= end_time:
        # run your web scraper code here
        print("Scraper is running...")
        #####
        ##### AQUÍ DEBE IR ITERACIÓN DE REALIZACIÓN DE BÚSQUEDA
        INICIO()
    else:
        print("Scraper is currently not running.")

    # wait for 1 minute before checking the time again
    timer.sleep(5)