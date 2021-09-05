# Get Data Script - gdelt
- Description: Saves locally an updated parquet file of the gdeltproject.org event database.
- Data Source: http://data.gdeltproject.org/gdeltv2/lastupdate.txt


The program runs executing `app.py` 


The class-based Python script run as follows:
- Checks if there is a new release of the Events dataset
- If there is a new dataset available, download the CSV file and save it in a `csvfiles` directory *
- Stores up to 2 csv files in the `csvfiles` folder and deletes the older ones
- Open the csv file as a new dataframe using `pandas` and drops the duplicates
- Saves the dataframe as a parquet file into the `parquetfiles` directory *
- As long as it is executing, the program runs every 15 min **(In test phase is executing every 4 secs)** 
```python
# Change to every 5 or 15 min for real case scenario (uncomment second line)
schedule.every(4).seconds.do(mydata.download_extract_save)
# schedule.every(15).minutes.do(mydata.download_extract_save)

while True:
    schedule.run_pending()
    time.sleep(1)
```


> Still to be implemented the creation of the `csvfiles` and `parquetfiles` directories. At the moment this two folder can be created manually.


