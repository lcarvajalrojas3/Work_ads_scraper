import time
from LinkedIn.site_mechanics import Site
from LinkedIn.scraper import scraper
from LinkedIn.data_handle import data
import datetime
import pandas as pd
import os
import random

# Define the start and end times for web scraping
start_time = datetime.time(hour=6)
end_time = datetime.time(hour=23, minute=59)
current_time = datetime.datetime.now().time()

clave = "polghtherce1"
mail = "laserena.arbolada@gmail.com"
keywords = ["Data Scientist", "Data Analyst", "Ingeniero Comercial", "Administración de Empresas"]
keyword = "Data Scientist"

folderpath = data.create_folders(keyword)

### Permanent Process
while True:

    ### HOURS SCHEDULE
    if start_time <= datetime.datetime.now().time() <= end_time:

        print("Starting process")

        ## Initianing site_mechanics, opening driver, logging in account, bar_searching
        site = Site()
        driver = site.run()
        site.login(driver, mail, clave)
        site.busqueda(driver, keyword)
        

        finish = 0
        pag = 1


        ### INICIANDO ITERACIÓN
        while finish == 0 and (start_time <= datetime.datetime.now().time() <= end_time):

            print("INITIATING WORK WINDOW")

            ## Seteo de tiempo de ventana de trabajo
            current_time = datetime.datetime.now().time()
            minutes_window = datetime.timedelta(minutes=random.randint(15,30))
            window_start_time = current_time
            window_stop_time = (
                datetime.datetime.combine(datetime.date.today(), current_time)
                + minutes_window).time()
            

            print("START TIME:", current_time)
            print("STOP TIME", window_stop_time)


            # Inicio de ventana de trabajo
            while finish == 0 and (
                # Se plantea 
                window_start_time <= datetime.datetime.now().time() <= window_stop_time
                ):


                # f(x) : Obtiene lista para request
                jobs = site.list_of_links(driver)


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
                        dftemp = pd.DataFrame(dicc)
                        dftemp.to_csv(os.path.join(folderpath, f"{keyword}_{pag}_{i}_{datetime.datetime.today().strftime('%d-%m-%Y')}.csv"))
                        
                        print(f"Scrap exitoso en pag {pag} - i {i} - n {i/2+1}")
                        time.sleep(random.randint(1,5))

                    except: print(f"Error en pag {pag} i {i} ... continuing")


                # Preparación variables siguiente de página
                keyword_x = keyword.replace(" ", "%20")
                pagestart = (pag)*25
                next_page = (f"https://www.linkedin.com/jobs/search/?keywords={keyword_x}&start={pagestart}")
                

                # f(x) click en botón de siguiente página
                pag, finish = site.nextpage(pag, driver)

                    # try: finish 0 pag =+1 : botón  encontrado y clickeado
                    # except: finish 1 pag = pag : botón no encontrado
            
            ### Caso A: No hay botón de término por término de páginas
            ### o por ERROR dentro de secuencia de scrapeo de página/paso a sgt página.
            if finish == 1:
                print("Pages finished")

            ### Caso B: Se terminó la ventana de trabajo
            ### y no las páginas del keyword:
            if datetime.datetime.now().time() >= window_stop_time and finish == 0:
                
                print("WINDOW TIME RUNOUT")
                driver.close()

                print("Next page url:", next_page)
                print("Initiating sleep time")
                time.sleep(random.randint(30*60,80*60))

                print("RESTARTING PROCESS")
                site = Site()
                driver = site.run()
                site.login(driver, mail, clave)
                driver.get(next_page)
                time.sleep(5)

            ### Caso C: Se terminó el horario de trabajo.    
            if datetime.datetime.now().time() >= end_time:
                print("Scheduled time ended")
                driver.close()
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
    else:
        print("MASTER SLEEP TIME SCHEDULE")
        # Generar F(x) que compile dfs de carpeta Data, y guarde en df central
        time.sleep(300)