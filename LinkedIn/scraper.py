from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep

class Scraper:
    def scrap(self, driver, keyword):
        sleep(1)
        self.Title = driver.find_element(By.XPATH,'//*[contains(@class,"job-title")]').text
        print(self.Title)
        self.Link = driver.find_element(By.XPATH,'//*[contains(@class,"job-title")]/a').get_attribute("href")
        print(self.Link)

        ## PRIMARY DESCRIPTION
        # Aquí podría ser mejor traer el texto completo y solamente dividir.
        primary_description = driver.find_element(By.XPATH,'//*[contains(@class,"primary-description-without-tagline")]').text.split(" · ")
        print("primary_description: ",primary_description)
        # Ejemplo: WSP Chile y Argentina · Las Condes, Región Metropolitana de Santiago, Chile · Publicado de nuevo hace 1 semana · Más de 100 solicitudes
        self.Company = primary_description[0]
        #print(self.Company)
        self.Location = primary_description[1]
        #print(self.Location)
        self.Time_on = primary_description[2]
        #print(self.time_on)
        self.Applies = primary_description[3]
        #print(self.applies)

        ## job-insight-...-secondary
        job_insight_secondary = driver.find_elements(By.XPATH, "//*[contains(@class, 'job-insight') and contains(@class, '-secondary')]/../span")
        print("job_insight_secondary: "," ".join([element.text for element in job_insight_secondary]))
        self.Modality = job_insight_secondary[0].text
        #print("Modality: ", self.Modality)
        self.Working_day = job_insight_secondary[1].text
        #print("Working_day: ", self.Working_day)
        try:
            self.Experience = job_insight_secondary[2].text
        except:
            self.Experience = None
        #print("Experience: ", self.Experience)

        # Company top card job insight
        try:
            job_insight_company = driver.find_element(By.XPATH, '//li-icon[contains(@type,"company")]/../../../..').text.split(" · ")
            print("job_insight_company: ",job_insight_company)
            try: self.Company_size = job_insight_company[0]
            except: self.Company_size = None
            #print("Company_size: ", self.Company_size)
            try: self.Company_area = job_insight_company[1]
            except: self.Company_area = None
            #print("Company_area: ", self.Company_area)
        except:
            self.Company_size = None
            #print("Company_size: ", self.Company_size)
            self.Company_area = None
            #print("Company_area: ", self.Company_area)

        # def aptitudes(driver):
        #     button = driver.find_element(By.XPATH,'//button[contains(@id, "ember") and contains(@class, "mv5 t-16")]')
        #     print("botón encontrado")
        #     driver.execute_script("arguments[0].click();", button)
        #     #button.click()
        #     print("botón clickeado")
        #     sleep(5)
        #     aptsdiv = driver.find_elements(By.XPATH,'//*[@class="display-flex align-items-center"]')
        #     print("objetos encontrados")
        #     Apts = []
        #     for aptdiv in aptsdiv[:-1]:
        #         Apts.append(aptdiv.text)
        #     closebutton = driver.find_element(By.XPATH, '//*[@aria-label= "Descartar"]')
        #     print("botón encontrado")
        #     closebutton.click()
        #     sleep(1)
        #     return Apts
        
        try: 
            #self.Apts = aptitudes(driver)
            button = driver.find_element(By.XPATH,'//button[contains(@id, "ember") and contains(@class, "mv5 t-16")]')
            #print("botón encontrado")
            driver.execute_script("arguments[0].click();", button)
            #print("botón clickeado")
            sleep(5)
            aptsdiv = driver.find_elements(By.XPATH,'//*[@class="display-flex align-items-center"]')
            self.Apts = []
            for aptdiv in aptsdiv[:-1]:
                self.Apts.append(aptdiv.text)
            print("Aptitudes obtenidas: ", self.Apts)
            # closebutton = driver.find_element(By.XPATH, '//*[@aria-label= "Descartar"]')
            # #print("botón encontrado")
            # closebutton.click()
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
            sleep(1)
        except: 
            print("falla en recolección de aptitudes")
            self.Apts = None
        
        self.Description = driver.find_element(By.XPATH,'//*[contains(@class,"jobs-description-content")]').text.replace("Acerca del empleo\n","")
        print("Descripción encontrada")#self.Description)


        return {"Title": self.Title, "Link": self.Link, "Company":self.Company, "Location":self.Location, "Time_on": self.Time_on, "Applies": self.Applies, 
                "Working_day":self.Working_day, "Experience": self.Experience, 
                "Company_size":self.Company_size, "Apts": [self.Apts], "Description":self.Description, "Keyword": keyword}

scraper = Scraper()