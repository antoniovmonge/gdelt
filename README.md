# Get Data Script - gdelt
- Description: Creates and saves a updated parquet file the gdeltproject.org event database.
- Data Source: http://data.gdeltproject.org/gdeltv2/lastupdate.txt


The program runs executing `app.py` 


The class-based Python script run as follows:
- Checks if there is a new release of the Events dataset.
- If there is a new dataset available, download the CSV file and save it in the "temp" folder *
- Stores up to 2 csv files in the `temp` folder and deletes the older one
- Open the file with the right parameters
- Creates a df using `pandas` and drops the duplicates
- Saves the df as a parquet file into the `parquetfiles` directory *
- The program runs every 15 min (actually running 4 secs - testing phase) 
```python
# Change to every 5 or 15 min for real case scenario (uncomment second line)
schedule.every(4).seconds.do(mydata.download_extract_save)
# schedule.every(15).minutes.do(mydata.download_extract_save)

while True:
    schedule.run_pending()
    time.sleep(1)
```


> Still to be implemented the creation of the `temp` and `parquetfiles` directories. At the moment this two folder can be created manually.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for gdelt in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/gdelt`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "gdelt"
git remote add origin git@github.com:{group}/gdelt.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
gdelt-run
```

# Install

Go to `https://github.com/{group}/gdelt` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/gdelt.git
cd gdelt
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
gdelt-run
```
