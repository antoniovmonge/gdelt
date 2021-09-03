import pandas as pd
import os

path = 'temp'

csv_files = os.listdir(path)
csv_files.sort(reverse=True)
# last_csv=f'{path}/{csv_files[1]}'
print(csv_files)
print(last_csv)
df = pd.read_csv(last_csv, sep='\t', header = None)
df.columns = df.columns.astype(str)
df = df.drop_duplicates()
print('\tSaving parquet file in the "parquetfiles" folder')
df.to_parquet('parquetfiles/updatedfile.parquet')
print('\tDone')
print(df.head())
# print(csv_files==[])