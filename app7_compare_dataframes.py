import pandas as pd
import os
import glob

path = 'temp/'
extension = 'csv'
os.chdir(path)
csv_files = glob.glob('*.{}'.format(extension))
csv_files.sort(reverse=True)

df1 = pd.read_csv(csv_files[0], sep='\t', header = None)

df2 = pd.read_csv(csv_files[0], sep='\t', header = None)

print(df1.equals(df2))