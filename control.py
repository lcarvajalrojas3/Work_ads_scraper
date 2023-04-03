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
end_time = datetime.time(hour=22)#, minute=50)
current_time = datetime.datetime.now().time()

clave = "polghtherce1"
mail = "laserena.arbolada@gmail.com"
keywords = ["Data Scientist", "Data Analyst", "Ingeniero Comercial", "Adminstración de Empresas"]
keyword = "Data Scientist"

while True:
    if start_time <= current_time <= end_time:
        print("Starting process")
        site = Site()
        driver = site.run()
        site.login(driver, mail, clave)
        folderpath = data.create_folders(keyword)
        site.busqueda(driver, keyword)
        finish = 0
        pag = 1

        while finish == 0 and (start_time <= current_time <= end_time):
            print("INITIATING WORK WINDOW")
            current_time = datetime.datetime.now().time()
            window_start_time = current_time
            print("START TIME:", current_time)
            minutes_window = datetime.timedelta(minutes=random.randint(15,30))
            window_stop_time = (datetime.datetime.combine(datetime.date.today(), current_time)
                                    + minutes_window).time()
            print("STOP TIME", window_stop_time)

            while finish == 0 and (window_start_time <= current_time <= window_stop_time):
                jobs = site.listof_jobs(driver)
                print(f"\nIniciando scrap de página {pag}")
                print("Avisos en página: ", len(jobs)/2, "\n")

                for i in range(0, len(jobs), 2):
                    current_time = datetime.datetime.now().time()
                    print(current_time)
                    jobs[i].click()
                    time.sleep(2)

                    dicc = scraper.scrap(driver, keyword) ### F(x) Extrae info del item, y la devuelve en un dicc
                    dftemp = pd.DataFrame(dicc)
                    dftemp.to_csv(os.path.join(folderpath, f"{keyword}_{pag}_{i}_{datetime.datetime.today().strftime('%d-%m-%Y')}.csv"))

                    time.sleep(7)

                current_page = f'https://www.linkedin.com/jobs/search/?keywords={keyword.replace(" ", "%20")}&start={(pag)*25}'
                pag, finish = site.nextpage(pag, driver)
            
            if finish == 1:
                print("Pages finished")
            elif current_time >= window_stop_time and finish == 0 and current_time <= end_time:
                print("WINDOW TIME RUNOUT")
                driver.close()
                print(current_page)
                print("Initiating sleep time")
                time.sleep(random.randint(30,60))
                print("RESTARTING PROCESS")
                current_time = datetime.datetime.now().time()
                site = Site()
                driver = site.run()
                site.login(driver, mail, clave)
                driver.get(current_page)
                time.sleep(5)
            elif current_time >= end_time:
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