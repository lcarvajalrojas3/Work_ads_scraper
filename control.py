import time
from LinkedIn.site_mechanics import Site
from LinkedIn.scraper import scraper
from LinkedIn.data_handle import data
import datetime
import pandas as pd
import os
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

clave = "polghtherce1"
mail = "laserena.arbolada@gmail.com"

### List of posible searches. << MUST COMPLETE >>

keywords = ["Data Scientist", "Data Analyst", "Ingeniero Comercial", "Administración de Empresas",
            "Trabajo Social", "Actuación", "Psicología", "Enfermería", "Prevención de riesgos",
            "Recursos Humanos", "Antropología", "Prevencionista", "Ingeniero Civil Industrial",
            "Ciencias Sociales", "Finanzas", "Arquitectura", "Diseño", "Diseño de interiores",
            "Cientista Social", "Profesional de las ciencias sociales", "Forestal"]
keyword = random.choice(keywords)

### Define the start and end times for web scraping. <<MUST COMPLETE>>

start_time = datetime.time(hour=2)
end_time = datetime.time(hour=23, minute=5)

# Create Data directorys.
folderpath = data.create_folders(keyword)

# Setting iteration tokens
pag = 1
finish = 0
driver_open = 0

site = Site()
### Init Permanent Process
while True:

    ### WORK WINDOWs
    while (start_time <= datetime.datetime.now().time() <= end_time):
               
        if finish == 0:
            print("INITIATING WORK WINDOW")

            ## Seteo de tiempo de ventana de trabajo
            minutes_window = datetime.timedelta(minutes=random.randint(15,35))
            window_start_time = datetime.datetime.now().time()
            window_stop_time = (
                datetime.datetime.combine(datetime.date.today(), window_start_time)
                + minutes_window).time()
            
            print("START TIME:", window_start_time)
            print("STOP TIME", window_stop_time)

            # > Driver Cerrado
            if driver_open == 0:
 
                driver = site.run()
                driver_open = 1
                site.login(driver, mail, clave)

        # pag se modifica según finish = 1, sino, se mantiene.    
        elif finish == 1 and (window_start_time <= datetime.datetime.now().time() <= window_stop_time): 
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
            window_start_time <= datetime.datetime.now().time() <= window_stop_time
            ):

            ### GENERO CICLO    
            # f(x) : Obtención de lista para request
            jobs = site.list_of_links(driver) ### Está seteado para botar los últimos 2 link, que dan bug

            print(f"\nIniciando scrap de página {pag}")
            print("Avisos en página: ", len(jobs)/2, "\n")

            ### SCRAPEO DE LIST_OF_LINKS
            for i in range(0, len(jobs), 2):
                try:

                    # Carga de datos de aviso
                    jobs[i].click()
                    time.sleep(5)

                    # Extracción de datos
                    dicc = scraper.scrap(driver, keyword) ### F(x) Extrae info del item, y la devuelve en un dicc
                    
                    #Encapsulado y guardado de datos
                    date_temp = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
                    dftemp = pd.DataFrame(dicc)
                    dftemp.to_csv(os.path.join(
                        folderpath, f"{keyword}_{date_temp}.csv"))
                    
                    print(f"Scrap exitoso en pag {pag} - i {i} - n {i/2+1}")
                    time.sleep(random.randint(1,5))

                except: print(f"Error en pag {pag} i {i}  n {i/2+1} ... continuing")

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
        if end_time >= datetime.datetime.now().time() >= window_stop_time and finish == 0:
            
            print("WINDOW TIME RUNOUT")
            driver.close()
            driver_open = 0

            print("SAVED Next page url:", next_page)
            intrand = random.randint(30*60,80*60)
            print(f"Initiating sleep time for {intrand} minutes at {datetime.datetime.now()}")
            time.sleep(intrand)

        ### Caso C: Se terminó el horario de trabajo.    
        if datetime.datetime.now().time() >= end_time:
            print("Scheduled time ended")
            driver.close()
            driver_open = 0

            ### Guardado de datos
            if os.path.exists(os.path.join(os.path.dirname(folderpath), "data.csv")):
                print("DDTT existente")
                df = pd.read_csv(os.path.join(os.path.dirname(folderpath), "data.csv"))
                df = data.save_data(folderpath, df)
                df.to_csv(os.path.join(os.path.dirname(folderpath), "data.csv"))
            else:
                print("DDTT no existente")
                df = pd.DataFrame()
                df = data.save_data(folderpath, df)
                df.to_csv(os.path.join(os.path.dirname(folderpath), "data.csv"))
            
            ### Falta eliminado de datos antiguos.

    print("MASTER SLEEP TIME SCHEDULE")
    # Generar F(x) que compile dfs de carpeta Data, y guarde en df central
    time.sleep(900)