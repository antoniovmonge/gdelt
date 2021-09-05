from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import datetime
import os
import schedule
import time
import pandas as pd
import pyarrow.parquet as pq

# FIXED URL WITH LAST UPDATE

class GdeltData:
    def __init__(self, url, path):
        self.url = url
        self.path = path

    # Saving the extracted CSV in the given path
    def download_extract_save(self):
        '''
        1: open the url and read and print the csv info
        2: check if the new file inside the zip is already in the temp directory
        3: if it is a new one, extract and save the file changing
        its extension from .CSV to .csv
        '''
        # This function extract the zip_url
        def get_zip_url(url):
            lines_list = []
            data = urlopen(url)
            for line in data:
                line = line.decode("UTF-8").strip('\n')
                lines_list.append(line.split(' '))
                zip_url = lines_list[0][2]

            return zip_url

        zipurl = get_zip_url(url)

        with urlopen(zipurl) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                print('*'*70)
                print('RUNNING','\ttime: ',str(datetime.datetime.now()))
                print('-'*70)
                print('Actual file in url: ')
                zfile.printdir()
                info = zfile.infolist()[0]
                info.filename = info.filename.lower() # Change the extension from CSV to csv (LOWER)
                file_name = info.filename # Variable used to read the .csv file in the first run of the program
                print('\tFile Name:\t' + info.filename) # Print information of the file
                print('\tModified:\t' + str(datetime.datetime(*info.date_time)))
                print('\tCompressed:\t' + str(info.compress_size) + ' bytes')
                print('\tUncompressed:\t' + str(info.file_size) + ' bytes')
                
                def extract_save():
                    '''
                    Extracts and save the .csv file in the "temp" directory
                    '''
                    print('*'*70)
                    print('\tExtracting all the files... ' + '\ttimestamp:\t' + str(datetime.datetime.now()))
                    # Extract file
                    zfile.extract(member=info,path=path)
                    print('\tNew dataset downloaded')
                
                def save_parquet():
                    '''
                    - Open the csv file with pandas
                    - give the csv the right format
                    - and save the parquet file
                    '''
                    # CREATING THE DATA FRAME from the csv file 
                    df = pd.read_csv('temp/' + file_name, sep='\t', header = None)
                    # changes the columns name to strings to avoid problems with parquet
                    df.columns = df.columns.astype(str)
                    df = df.drop_duplicates() # Drop duplicates
                    print('\t- Saving parquet file into the "parquetfiles" folder')
                    # SAVING THE DATAFRAME AS PARQUET FILE (into "parquetfiles" directory)
                    df.to_parquet('parquetfiles/updatedfile.parquet')
                    print('\t- Done')
                    print()
                    # Read and print the parquet file metadata
                    parquet_file = pq.ParquetFile('parquetfiles/updatedfile.parquet')
                    print('-'*70)
                    print('\t* NEW PARQUET FILE AVAILABLE IN "parquetfiles" folder')
                    print()
                    print(parquet_file.metadata)
                    print()

                # Updating "csv_files" (list variable) --> check if there are already files saved
                csv_files = os.listdir(path) # Remember path = 'temp'

                # FIRST RUN OF THE PROGRAM (No files in temp directory)
                if csv_files == []: # Check that there are still no items in the temp directory folder
                    print('1: Empty list. Downloading data for the first time')
                    # CALLING THE FUNCTIONS
                    extract_save()
                    save_parquet()

                else:
                    print('-'*70)
                    print('2: Checking for new datasets')
                    # Check if there is a new dataset available
                    csv_files = os.listdir(path)
                    if info.filename not in csv_files:
                        print('2.1 - New data set available')
                        extract_save()
                        save_parquet()
                        csv_files = os.listdir(path)
                        # clean files if there are more than 2
                        if len(csv_files) > 2:
                            print(f'2.1.1 - More than 2 csv files in "{path}" folder')
                            csv_files = os.listdir(path)
                            print('\tdeleting older csv...')
                            os.remove(f'{path}/{csv_files[2]}')
                            print('\tOlder .csv deleted')
                        else:
                            pass
                    else:
                        print('-'*70)
                        print('No new dataset available:\t' + str(datetime.datetime.now()))
                    
                print('-'*70)
                print('END OF THE EXECUTION (NEXT IN 15 MIN)')
                print('*'*70)
                print()
                print()
                return None


url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
path = 'temp'

# Instantiate the data object
mydata = GdeltData(url,path)

# SETTING THE TIMMER TO EXECUTE EVERY X MIN (FOR CONTROL VERSION EVERY 4 SECS)
# Change to every 5 or 15 min for real case scenario.

schedule.every(4).seconds.do(mydata.download_extract_save)
# schedule.every(15).minutes.do(mydata.download_extract_save)

while True:
    schedule.run_pending()
    time.sleep(1)
