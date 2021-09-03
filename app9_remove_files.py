import os

path = 'temp'
csv_files = os.listdir(path)

if len(csv_files) > 2:
    os.remove(csv_files[2])