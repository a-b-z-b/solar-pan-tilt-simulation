import os
import time
import schedule
import serial

from qweather import solar_angles
from datetime import datetime, time as dt_time
from dotenv import load_dotenv

COUNT = 0


def scheduled_request(url, arduino):
    global COUNT

    solar_data = solar_angles.make_request(url)
    print(f"\nResponse at {datetime.now()}\n")
    print(f"\nelevation: {solar_data['solarElevationAngle']}, azimuth: {solar_data['solarAzimuthAngle']}\n")

    message = f"{solar_data['solarAzimuthAngle']},{solar_data['solarElevationAngle']}\n"
    arduino.write(message.encode('utf-8'))

    time.sleep(0.1)
    while arduino.in_waiting:
        print(f"\nARDUINO SAID: {arduino.readline().decode('utf-8').strip()}\n")

    COUNT += 1
    print(f"COUNT: {COUNT}")
    if COUNT >= len(schedule.jobs):
        print("\nDone for today! Exiting.\n")
        exit()


def main():
    load_dotenv()

    KEY = os.getenv("API_KEY")
    if not KEY:
        raise Exception("API key not found in environment! Exiting.")

    DATE = datetime.today().strftime("%Y%m%d")

    day_distribution = ["0700", "0800", "0900", "1000", "1100", "1130", "1200",
                        "1230", "1300", "1330", "1400", "1500", "1600", "1700"]

    now = datetime.now().time()

    arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)
    time.sleep(2)

    for t in day_distribution:
        url = (
            f"https://devapi.qweather.com/v7/astronomy/solar-elevation-angle?"
            f"location=2.9833,34.6667&alt=549&date={DATE}&time={t}&tz=0100&key={KEY}"
        )

        sched_time = dt_time(int(t[:2]), int(t[2:]))

        if sched_time >= now:
            print(f"Scheduling call at {t[:2]}:{t[2:]}")
            schedule.every().day.at(f"{t[:2]}:{t[2:]}").do(lambda url=url, arduino=arduino: scheduled_request(url, arduino))
        else:
            print(f"Skipping past time {t[:2]}:{t[2:]}")

    # If no future calls remain, we exit.
    if not schedule.jobs:
        print("\nNo remaining times to schedule today. Exiting.\n")
        return

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    main()
