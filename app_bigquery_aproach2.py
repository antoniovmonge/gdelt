from google.cloud import bigquery

client = bigquery.Client()

# query = """
#     SELECT GLOBALEVENTID AS event_id, Actor1Name AS actor1, Actor2Name AS actor2
#     FROM `gdelt-bq.gdeltv2.events`
#     FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
# """

query = """
    SELECT COUNT(*) AS total,
    FROM `gdelt-bq.gdeltv2.events`
    FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
"""

job_config = bigquery.job.QueryJobConfig(use_query_cache=False)
results = client.query(query, job_config=job_config)

# for row in results:
#     event_id = row['event_id']
#     actor1 = row['actor1']
#     actor2 = row['actor2']
#     print(f'{event_id} | {actor1} | {actor2}')

for row in results:
    total = row['total']

print(f'TOTAL ROWS: {total}')
print('-'*60)
print(f'Created: {results.created}')
print(f'Ended:   {results.ended}')
print(f'Bytes:   {results.total_bytes_processed:,}')
