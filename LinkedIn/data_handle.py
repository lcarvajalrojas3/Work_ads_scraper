import os
from datetime import datetime, timedelta
import pandas as pd

class Data:
    def check_data_folder(self, keyword):
        print("Revisando existencia de carpetas necesarias")
        self.self_path = os.path.dirname(os.path.realpath(__file__))
        self.data_folderpath = os.path.join(self.self_path, "Data")
        if not os.path.exists(self.data_folderpath):
            os.mkdir(self.data_folderpath)
            print("Subcarpeta Data creada\n\n")
        else: print("Subcarpeta Data Existente")
        return self.data_folderpath
    
    def check_log_folder(self, keyword):
        print("Revisando existencia de carpetas log necesarias")
        self.self_path = os.path.dirname(os.path.realpath(__file__))
        self.log_folderpath = os.path.join(self.self_path, "Log")
        if not os.path.exists(self.log_folderpath):
            os.mkdir(self.log_folderpath)
            print("Subcarpeta Log creada\n\n")
        else: print("Subcarpeta Log Existente")
        return self.log_folderpath
    
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