from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import datetime
import glob
import os

# FIXED URL WITH LAST UPDATE
url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'

# This function extract the zip_url
def get_zip_url(url):
    lines_list = []
    data = urlopen(url)
    for line in data:
        line = line.decode("UTF-8").strip('\n')
        lines_list.append(line.split(' '))
        zip_url = lines_list[0][2]

    return zip_url

# Saving the extracted CSV in the given path
def download_extract():
    path = 'temp'
    zipurl = get_zip_url(url)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.printdir()
            info = zfile.infolist()[0]
            # for info in zfile.infolist():
            # Change the extension from CSV to csv (LOWER)
            info.filename = info.filename.lower()
            # Print information of the file
            print('\tFile Name:\t' + info.filename)
            print('\tModified:\t' + str(datetime.datetime(*info.date_time)))
            # print('\tSystem:\t\t' + str(info.create_system) + '(0 = Windows, 3 = Unix)')
            # print('\tZIP version:\t' + str(info.create_version))
            print('\tCompressed:\t' + str(info.compress_size) + ' bytes')
            print('\tUncompressed:\t' + str(info.file_size) + ' bytes')
            
            # Check if there is a new dataset available
            csv_files = os.listdir(path)
            if info.filename not in csv_files:
                
                print('*'*70)
                print('Extracting all the files... ' + '\ttime:\t' + str(datetime.datetime.now()))
                # Extract file
                zfile.extract(member=info,path=path)
                print('\tNew dataset downloaded')
            else:
                print('*'*70)
                print('No new dataset available:\t' + str(datetime.datetime.now()))
                
            print('*'*70)
        
download_extract()


