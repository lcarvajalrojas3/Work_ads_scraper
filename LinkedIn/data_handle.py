import os
from datetime import datetime, timedelta
import pandas as pd

class Data:
    def create_folders(self, keyword):
        print("Revisando existencia de carpetas necesarias")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.folderpath = "Data" #keyword.replace(" ", "_") + "_" + str(datetime.now().date())
        self.folderpath = os.path.join(self.dir_path, self.folderpath)
        if not os.path.exists(self.folderpath):
            os.mkdir(self.folderpath)
            print("Subcarpeta Data creada\n\n")
        else: print("Subcarpeta Data Existente")
        return self.folderpath
    
    def save_data(self, folderpath, df):
        print("Recopilando y guardando datos de sesión")
        for filename in os.listdir(folderpath):
            if filename.endswith(".csv"):
                # Read the CSV file into a DataFrame
                self.file_path = os.path.join(folderpath, filename)
                self.df_temp = pd.read_csv(self.file_path)
                
                # Concatenate the DataFrame onto the combined DataFrame
                df = pd.concat([df, self.df_temp])
        return df
data = Data()