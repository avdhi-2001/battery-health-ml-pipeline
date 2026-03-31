import pandas as pd

metadata = pd.read_csv('cleaned_dataset/metadata.csv')

print(metadata.head())             

print("Shape:", metadata.shape) 

print("Columns:", metadata.columns.tolist()) 

print ("Test types count",metadata['type'].value_counts())

print("batteries in datatset", metadata['battery_id'].unique())

print("null values per column", metadata.isnull().sum())

discharge_only= metadata[metadata["type"]=="discharge"]
print(discharge_only)
print(discharge_only[['battery_id','type','Capacity']].head(10))

discharge_only = metadata[metadata['type'] == 'discharge'].copy()
