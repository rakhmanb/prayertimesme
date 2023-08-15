import requests
import json
from datetime import datetime
from praytimes import PrayTimes
import schedule
import time
import fmt
from datetime import date

now = datetime.now()
now_date = now.strftime("%D")
URL = "https://mkzense.com/webhook/alexa/ae61c4e3aa39ac9ead4826ec6878c921cf701141/"
PRAYERMAPPING = {
    "fajr": "AthanFajr",
    "dhuhr": "AthanDuhr",
    "asr": "AthanAsr",
    "maghrib": "AthanMag",
    "isha": "AthanIsha"
}


def trigger_prayer(name=None):
    print('triggering prayer...')
    requests.get(URL + PRAYERMAPPING[name])
    return schedule.CancelJob


def create_prayer_time_jobs():
    prayTimes = PrayTimes("ISNA")
    prayTimes.tune({"fajr": 8, "maghrib": -17, "isha": 10})
    times = prayTimes.getTimes(date.today(), (47.639282, -122.103020), -7)
    for i in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
        print(i + ": " + times[i.lower()])
        schedule.every().day.at(times[i.lower()]).do(
            trigger_prayer, i.lower())


if __name__ == '__main__':
    create_prayer_time_jobs()

while True:
    current_date = datetime.now()
    current_date_full = current_date.strftime("%D")
    current_date_time = current_date.strftime("%H:%M:%S")
    current_date_hour = current_date.strftime("%H")
    if current_date_full != now_date and current_date_hour == "2":
        print("get all prayer times")
        schedule.clear()
        create_prayer_time_jobs()
    else:
        print(current_date_time)
        print("not next day yet...will try in 30 seconds")
    schedule.run_pending()
    time.sleep(30)
