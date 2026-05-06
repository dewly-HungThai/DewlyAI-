import numpy as np
import pandas as pd 

class DataAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print(f"Loaded. Data have {len(self.df)} rows and {len(self.df.columns)} columns")
        print(self.df.dtypes)
        
    def cleaning_data(self):
        print("=== Missing Values (before) ===")
        print(self.df.isnull().sum(), "\n")
        for column in self.df.columns:
            if self.df[column] in [np.float64, np.int64]:
                self.df[column].fillna(self.df[column].median(), inplace=True)
            else:
                self.df[column].dropna()
        print("=== Missing Values (after) ===")
        print(self.df.isnull().sum(), "\n")
        
    def compute_status(self, column):
        arr = self.df[column].dropna().to_numpy()
        status = {
            "mean" : np.mean(arr),
            "median" : np.median(arr),
            "std" : np.std(arr),
            "max" : np.max(arr),
            "min" : np.min(arr),
            "q25" : np.percentile(arr, 25),
            "q75" : np.percentile(arr, 75)
        }
        print(f"Mean: {status["mean"]}")
        print(f"Median: {status["media"]}")
        print(f"Standard Deviation: {status["std"]}")
        print(f"Max: {status["max"]}")
        print(f"Min: {status["min"]}")
        print(f"Q25: {status["q25"]}, Q75: {status["q75"]}")
        
        return status
        
    
        
