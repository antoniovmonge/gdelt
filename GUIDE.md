# Google BigQuery API in Python

If you are not trying to run a big job with large volume of data, Google BigQuery API is a great candidate. To install, run in your Terminal
```
pip install — upgrade google-cloud-bigquery
```

## Import Packages
```python
from google.cloud import bigquery
import pandas as pd
```

## Read from BigQuery
To read data from BigQuery, you can decide if you want to read with your own credential, or with a service account credential. If you want to use your own credential, the first step is to authorize your Google account by running in your Terminal. 
```
gcloud auth login
```

And then you can proceed in your Python editor:

```python
# Construct a BigQuery client object.
client = bigquery.Client(project=YOUR_PROJECT)query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20
"""
query_job = client.query(query).result().to_dataframe() # Make an API request and convert the result to a Pandas dataframe.
```





