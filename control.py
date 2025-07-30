import time
from LinkedIn.site_mechanics import Site    
from LinkedIn.scraper import scraper
from LinkedIn.data_handle import data
import datetime
import pandas as pd
import os
import sys
import random

### Español:

# Web Scraping Automatizado para Análisis de Empleos
# Monitoreo Automatizado de Ofertas de Trabajo para Análisis
# Crawler de Empleos para Análisis de Mercado Laboral

## English:

# Automated Web Scraping for Job Analysis
# Continuous Job Offer Monitoring for Analysis
# Job Market Analysis Crawler

# Deutsch:

# Automatisierte Web Scraping für Job-Analyse
# Kontinuierliche Überwachung von Job-Angeboten für Analyse
# Job-Markt-Analyse Crawler

# Conceptos Técnicos:

# Web Scraping
# Automatización de Procesos
# Análisis de Datos

# Technical Concepts:

# Web Scraping
# Process Automation
# Data Analysis

# Technische Konzepte:

# Web Scraping
# Prozessautomatisierung
# Datenanalyse


"""          WORKFLOW

>>>> WHILE >>>> INIT HOURS MAIN-SCHEDULE
    >> IF >> WORK
        >> WHILE >> Init Keyword-Iteration (finish = 0, pag = 1)
            >> IF >> Init Time Window 
                >> while(finish == 0) >> Init Scrap-Iteration 
                    >>>> SCRAP (Subprocess)
                    >   Site_Mechanics
                    >   Scraper *Pipeline
                    >   /Data
            >> ELSE >> SLEEP

    >> ELIF >> DATA SAVE
        > Concat
        > Format
        > Delete

    >> ELSE >> SLEEP

                                            
"""
### THIS SCRIPTS NEEDS AN LINKEDIN ACCOUNT TO LOG IN AND WORK. << MUST COMPLETE >>

clave = "eureka12345"
mail = "delirantedesvario@gmail.com"

### List of posible searches. << MUST COMPLETE >>

# keywords = [
#             "Data Scientist", "Data Analyst", "Ingeniero Comercial", "Administración de Empresas", "C#", "DevOps",
#             "Trabajo Social", "Actuación", "Psicología", "Química", "IaC", "Administración de contratos", "Business Partner",
#             "Antropología", "Ingeniero Civil Industrial", "Física", "C++", "Construcción", "Ejecutivo Comercial"
#             "Ciencias Sociales", "Finanzas", "Arquitectura", "Diseño", "Diseño de interiores", "Python",
#             "Cientista Social", "Forestal", "Java", "Azure", "Cloud", "Banca", "Ejecutivo Banca", "Ejecutivo de Ventas"
#             ]

keywords = [
            "Data Scientist", "Data Analyst", "Ingeniero Comercial", "Administración de Empresas", "C#", "DevOps",
            "Química", "IaC", "Software",
            "Ingeniero Civil Industrial", "Física", "C++", "Construcción",
            "Python", "Data Scientist",
            "Forestal", "Java", "Azure", "Cloud"
            ]

keyword = random.choice(keywords)

### Define the start and end times for web scraping. 

start_time = datetime.time(hour=0)
end_time = datetime.time(hour=23, minute=59)

# Create Data directorys con biblioteca data_handle
data_folderpath = data.check_data_folder(keyword)
log_folderpath = data.check_log_folder(keyword)

log_file = os.path.join(log_folderpath, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# Setting iteration tokens
pag = 1
finish = 0
driver_open = 0

# Trayendo herramientas y scraper en sí.
# Abriendo instancia
site = Site()

### Init Permanent Process
try:
    while True:

        ### WORK WINDOWs
        while (start_time <= datetime.datetime.now().time() <= end_time):
                
            if finish == 0:
                print("INITIATING WORK WINDOW")

                ## Seteo de tiempo de ventana de trabajo
                minutes_window = datetime.timedelta(minutes=random.randint(120,200))
                window_start_time = datetime.datetime.now()
                window_stop_time = window_start_time + minutes_window
                
                print("START TIME:", window_start_time)
                print("STOP TIME", window_stop_time)

                # > Driver Cerrado
                if driver_open == 0:
                    driver = site.run()
                    driver_open = 1

                    # Inicio de sesión
                    site.login(driver, mail, clave)
                    time.sleep(5)

            # pag se modifica según finish = 1, sino, se mantiene.    
            elif finish == 1 and (window_start_time <= datetime.datetime.now() <= window_stop_time): 
                print("CONTINUING WORK WINDOW WITH NEW KEYBOARD")
                finish = 0
                pag = 1
                keyword = random.choice(keywords)



            ### Cargado de pag de avisos
            if pag == 1:
                ## Initianing site_mechanics, opening driver, logging in account, bar_searching
                site.busqueda(driver, keyword)
            if pag > 1:
                driver.get(next_page)

            # Ejecución de Site y Scraper
            while finish == 0 and (
                window_start_time <= datetime.datetime.now() <= window_stop_time
                ):

                ### GENERO CICLO    
                # f(x) : Obtención de lista para request
                
                jobs = site.list_of_links(driver) ### Está seteado para botar los últimos 2 link, que dan bug

                print(f"\nIniciando scrap [{keyword}] en página {pag}")
                print("Avisos en página: ", len(jobs), "\n")

                ### SCRAPEO DE LIST_OF_LINKS
                for i in range(0, len(jobs), 1):
                    try:

                        # Carga de datos de aviso
                        jobs[i].click()
                        print("click realizado en i ", i)
                        time.sleep(2)
                        
                        # Extracción de datos
                        dicc = scraper.scrap(driver, keyword) ### F(x) Extrae info del item, y la devuelve en un dicc
                        #print(dicc)
                        time.sleep(random.randint(1,3))

                        #Encapsulado y guardado de datos
                        date_temp = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
                        dftemp = pd.DataFrame(dicc)
                        dftemp.to_csv(os.path.join(
                            data_folderpath, f"{keyword}_{date_temp}.csv"), sep="|", index=False)
                        
                        print(f"Scrap exitoso en pag {pag} - i {i} - n {i+1}\n")
                        time.sleep(random.randint(1,2))

                    except: 
                        print(f"Error en pag {pag} i {i}  n {i+1} ... continuando")
                        time.sleep(3)

                # Preparación variables siguiente de página
                keyword_x = keyword.replace(" ", "%20")
                pagestart = (pag)*25
                next_page = (f"https://www.linkedin.com/jobs/search/?keywords={keyword_x}&start={pagestart}")

                # f(x) click en botón de siguiente página
                pag, finish = site.nextpage(pag, driver)
                    # try: Botón encontrado y clickeado >>> finish=0, pag =+1 : 
                    # except: Botón no encontrado >>> finish=1, pag=pag : 
            



            ### TERMINO DE 
            ### Caso A: No hay botón de término por término de páginas
            ### o por ERROR dentro de secuencia de scrapeo de página/paso a sgt página.
            if finish == 1:
                print("Pages finished")

            ### Caso B: Se terminó la ventana de trabajo
            ### y no las páginas del keyword:
            if end_time >= datetime.datetime.now().time() and datetime.datetime.now() >= window_stop_time and finish == 0:
                
                print("WINDOW TIME RUNOUT")
                driver.close()
                driver_open = 0

                ## Si cae aquí puede generar error
                print("SAVED Next page url:", next_page)
                intrand = random.randint(20*60,60*60)
                print(f"Initiating sleep time for {intrand/60} minutes at {datetime.datetime.now()}")
                time.sleep(intrand)

            ### Caso C: Se terminó el horario de trabajo.    
            if datetime.datetime.now().time() >= end_time and finish == 1:
                print("Scheduled time ended")
                
                # if driver_open == 1:
                #     driver.close()
                #     driver_open = 0

                ### Lógica de consolidación de datos.

                ### Guardado de datos
                # if os.path.exists(os.path.join(os.path.dirname(data_folderpath), "data.csv")):
                #     print("DDTT existente")
                #     df = pd.read_csv(os.path.join(os.path.dirname(data_folderpath), "data.csv"))
                #     df = data.save_data(data_folderpath, df)
                #     df.to_csv(os.path.join(os.path.dirname(data_folderpath), "data.csv"))
                # else:
                #     print("DDTT no existente")
                #     df = pd.DataFrame()
                #     df = data.save_data(data_folderpath, df)
                #     df.to_csv(os.path.join(os.path.dirname(data_folderpath), "data.csv"))
                
                ### Falta eliminado de datos antiguos.

        print("MASTER SLEEP TIME SCHEDULE")
        # Generar F(x) que compile dfs de carpeta Data, y guarde en df central
        
        time.sleep(900)


except Exception as e:
    print("Ocurrió un error durante la ejecución del script:", e)
finally:
    # Cierra el archivo al finalizar el script
    print("Goodbye cruel world")