import schedule
import time

from app4_get_csv import download_extract

schedule.every(4).seconds.do(download_extract)
# schedule.every(15).minutes.do(download_extract)

while True:
    schedule.run_pending()
    time.sleep(1)
