from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import datetime
import os
import schedule
import time
import pandas as pd

# URL WITH LAST UPDATE
url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'

# Path to directory where csv files are stored: 
# (It deletes the older file each time it saves a new one)
path = 'temp'


# This function extract the zip_url
def get_zip_url(url):
    '''
    it return the url to the zip file (the third element of the first line)
    '''
    lines_list = []
    data = urlopen(url)
    for line in data:
        line = line.decode("UTF-8").strip('\n')
        lines_list.append(line.split(' '))
        zip_url = lines_list[0][2]

    return zip_url

# Saving the extracted CSV in the given path
def download_extract_save():
    print(os.listdir(path))
    '''
    1: open the url and read and print the csv info
    2: check if the new file inside the zip is already in the temp directory
    3: if it is a new one, extract and save the file changing
    its extension from .CSV to .csv
    '''
    zipurl = get_zip_url(url)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.printdir()
            info = zfile.infolist()[0]
            # for info in zfile.infolist():
            # Change the extension from CSV to csv (LOWER)
            info.filename = info.filename.lower()
            file_name = info.filename
            # Print information of the file
            print('\tFile Name:\t' + info.filename)
            print('\tModified:\t' + str(datetime.datetime(*info.date_time)))
            # print('\tSystem:\t\t' + str(info.create_system) + '(0 = Windows, 3 = Unix)')
            # print('\tZIP version:\t' + str(info.create_version))
            print('\tCompressed:\t' + str(info.compress_size) + ' bytes')
            print('\tUncompressed:\t' + str(info.file_size) + ' bytes')
            
            def extract_save():
                print('*'*70)
                print('\tExtracting all the files... ' + '\ttime:\t' + str(datetime.datetime.now()))
                # Extract file
                zfile.extract(member=info,path=path)
                print(f'\tNEW DATASET downloaded into "{path}" folder')

            def save_parquet():
                csv_files = os.listdir(path)
                csv_files.sort(reverse=True)
                last_csv=f'{path}/{csv_files[0]}'
                df = pd.read_csv(last_csv, sep='\t', header = None)
                df.columns = df.columns.astype(str)
                df = df.drop_duplicates()
                print('\tSaving parquet file in the "parquetfiles" folder')
                df.to_parquet('parquetfiles/updatedfile.parquet')
                print('\tDone')

            # update "csv_files" variable to check if there are already files inside
            csv_files = os.listdir(path)
            # first run
            if csv_files == []:
                print('1: Empty list. Downloading data for the first time')
                extract_save()
                # print('First if statement')
                # df = pd.read_csv(f'{path} + /*.csv')
                df = pd.read_csv('temp/' + file_name, sep='\t', header = None)
                df.columns = df.columns.astype(str)
                df = df.drop_duplicates()
                print('\tSaving parquet file in the "parquetfiles" folder')
                df.to_parquet('parquetfiles/updatedfile.parquet')

            else:
                print('2: Checking for new datasets')
                # Check if there is a new dataset available
                if info.filename not in csv_files:
                    print('2.1 (New data set available)')
                    extract_save()
                    save_parquet()

                    csv_files = os.listdir(path)
                    print(len(csv_files))
                    # clean files if there are more than 2
                    if len(csv_files) > 2:
                        print(f'2.1.1 - More than 2 csv files in "{path}" folder')
                        csv_files = os.listdir(path)
                        print('deleting older csv...')
                        os.remove(f'{path}/{csv_files[2]}')
                        print('\tOlder .csv deleted')
                    else:
                        print('2.1.2')
                        
                else:
                    print('2.2')
                    print('*'*70)
                    print('\tNo new dataset available:\t' + str(datetime.datetime.now()))
                
            print('*'*70)
            print('\t####### END OF THE EXECUTION (NEXT IN 15 MIN) #########')
            print()
            print()



# Setting the timer to execute the script every 15 min.

schedule.every(4).seconds.do(download_extract_save)
# schedule.every(15).minutes.do(download_extract)

while True:
    schedule.run_pending()
    time.sleep(1)

