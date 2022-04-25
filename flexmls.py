from mail import mail
import schedule
import time
from dataScraper import dataScraper




# schedule.every().day.at("21:29:10").do(mail)
# schedule.every().day.at("21:29:30").do(job)
schedule.every().day.at("10:00").do(mail)
schedule.every().day.at("07:00").do(dataScraper)
schedule.every().day.at("03:00").do(dataScraper)
# schedule.every(5).seconds.do(dataScraper)

while True:
    schedule.run_pending()
    time.sleep(1)