from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class Site:
    def __init__(self):
        self.url = 'https://www.linkedin.com/'
        #print(self.url)
        self.is_running = False

    def run(self):
        self.is_running = True
        self.driver = self.open_webdriver()
        self.driver.get(self.url)
        return self.driver

    def stop(self):
        # Stop the web scraping process
        self.is_running = False
        self.driver.quit()

    def open_webdriver(self):
        # Open the web driver
        self.options = Options()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--no-default-browser-check")
        self.options.add_argument("--disable-infobars")

        self.exp_opt = ["enable-logging", "enable-automation", "ignore-certificate-errors"]
        self.options.add_experimental_option("excludeSwitches", self.exp_opt)

        self.driver = webdriver.Chrome(options=self.options) # Replace with appropriate web driver
        return self.driver
    
    def login(self, driver, mail, clave):
        self.userdiv = driver.find_element(By.XPATH,'//*[@autocomplete="username"]')
        self.userdiv.click()
        self.userdiv.clear()
        self.userdiv.send_keys(mail)

        self.passdiv = driver.find_element(By.XPATH,'//*[@autocomplete="current-password"]')
        self.passdiv.click()
        self.passdiv.clear()
        self.passdiv.send_keys(clave)

        self.driver.find_element(By.XPATH,'//*[@type="submit"]').click()
        sleep(1)
        print("Cuenta Logueada\n")
        sleep(2)

    def busqueda(self, driver, keyword):
        sleep(2)
        driver.get("https://www.linkedin.com/jobs/")
        sleep(3)
        self.searchdiv = self.driver.find_element(By.XPATH,'//*[@aria-label="Busca por cargo, aptitud o empresa"]')
        self.searchdiv.click()
        self.searchdiv.clear()
        self.searchdiv.send_keys(keyword)
        sleep(1)
        self.searchdiv.send_keys(Keys.RETURN)

        sleep(1)
        print(f"Búsqueda de {keyword} realizada\n")
        sleep(2)

    def listof_jobs(self, driver):#, df, folderpath, pag):
        ### A usarse en Escenario: Página-listado de trabajos < - Resultado búsqueda()
        ### Debiese scrolear hacia abajo div de listado, hasta cargar todos los link
        ### y luego abrir uno a uno y aplicar la función scrap_item()

        self.df_page = pd.DataFrame()
            ## Identificación de container

        self.container = driver.find_element(By.XPATH, '//*[contains(@class, "scaffold-layout__list-container")]/..')
            # Medido de tamaño de scroll
        self.prev_height = driver.execute_script("return arguments[0].scrollHeight;", self.container)
            # Scroll down the container until the height no longer changes
        while True:
                # Scroll down the container by a certain amount
            driver.execute_script("arguments[0].scrollTop += 1000;", self.container)
            sleep(1)  
            # Get the new height of the container
            self.new_height = driver.execute_script("return arguments[0].scrollHeight;", self.container)

            if self.new_height == self.prev_height:
                # If the height no longer changes, it means there are no more options to load
                break
            self.prev_height = self.new_height  # Update the previous height
        
        ### Trabaja sobre cada "link" de trabajo dentro de la lista de búsqueda
        self.jobs = driver.find_elements(
            By.XPATH,'//*[@class="scaffold-layout__list-container"]/li/div/div/div/div[2]/div/a'
            )
        return self.jobs

    def nextpage(self, pag, driver):
      try:   
         pag +=1
         self.temp_button = driver.find_element(By.XPATH, f'//*[contains(@aria-label,"Página {pag}")]')
         self.temp_button.click()
         sleep(3)
         finish = 0
         return pag, finish
      except:
         finish = 1
         pag = pag
         print("SCRAPING DE BÚSQUEDA FINALIZADO")
         return pag, finish

#url = 'https://www.linkedin.com/'
#site = Site()
