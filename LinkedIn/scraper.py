from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

class Scraper:
    def scrap(self, driver, keyword):
        sleep(1)
        self.Title = driver.find_element(By.XPATH,'//*[contains(@class,"job-title")]').text
        #print(self.Title)
        self.Link = driver.find_element(By.XPATH,'//*[contains(@class,"job-title")]/..').get_attribute("href")
        #print(self.Link)
        self.Company = driver.find_element(By.XPATH,'//*[contains(@class,"company-name")]').text
        #print(self.Company)
        self.Location = driver.find_element(By.XPATH,'//*[@class="jobs-unified-top-card__bullet"]').text
        #print(self.Location)
        self.Working_day = driver.find_elements(By.XPATH,'//*[@class="jobs-unified-top-card__job-insight"]')[0].text.split(" · ")[0]
        #print(self.Working_day)
        try:
            self.Experience = driver.find_elements(By.XPATH,'//*[@class="jobs-unified-top-card__job-insight"]')[0].text.split(" · ")[1]
        except:
            self.Experience = None
        #print(self.Experience)
        try: self.Company_size = driver.find_elements(By.XPATH,'//*[@class="jobs-unified-top-card__job-insight"]')[1].text
        except: self.Company_size = None
        #print(self.Company_size)
        def aptitudes(driver):
            button = driver.find_element(By.XPATH,'//*[contains(@aria-label, "módulo para coincidencias")]')
            button.click()
            sleep(1)
            aptsdiv = driver.find_elements(By.XPATH,'//*[@class="display-flex align-items-center"]')
            Apts = []
            for aptdiv in aptsdiv[:-1]:
                Apts.append(aptdiv.text)
            closebutton = driver.find_element(By.XPATH, '//*[@aria-label= "Descartar"]')
            closebutton.click()
            sleep(1)
            return Apts
        try: self.Apts = aptitudes(driver)
        except: self.Apts = None
        #print(self.Apts)
        self.Description = driver.find_element(By.XPATH,'//*[contains(@class,"jobs-description-content")]').text.replace("Acerca del empleo\n","")
        #print(self.Description)
        return {"Title": self.Title, "Link": self.Link, "Company":self.Company, "Location":self.Location, 
                "Working_day":self.Working_day, "Experience": self.Experience, 
                "Company_size":self.Company_size, "Apts": [self.Apts], "Description":self.Description, "Keyword": keyword}

scraper = Scraper()