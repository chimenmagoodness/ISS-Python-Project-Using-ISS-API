import time
import smtplib
import requests
import ssl
import datetime as dt

MY_LAT = 37.09024
MY_LNG = -95.712891
MY_EMAIL = "1stpassabite@gmail.com"
MY_PASSWORD = "ntilkwogugibwqko"
EMAIL_TO = "sweetnessgoodness10@gmail.com"
SMTP_SEVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_CONTEXT = ssl.create_default_context()

# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()
# data = response.json()["iss_position"]
#
# latitude = data["latitude"]
# longitude = data["longitude"]
#
# current_position = (latitude, longitude)
# print(current_position)
parameters = {
        "lat": MY_LAT,
        "lgn": MY_LNG,
        "formatted": 0
    }


def is_iss_overhead():
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()

    iss_latitude = data["latitude"]
    iss_longitude = data["longitude"]

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True


def is_night():

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    today_time = dt.datetime.now().hour

    if today_time >= sunset or today_time <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        try:
            print("connecting to server.....")
            with smtplib.SMTP(SMTP_SEVER, SMTP_PORT) as connection:
                connection.starttls(context=EMAIL_CONTEXT)
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                print("Connected to Server :-)")

                print()
                print(f"Sending Email to - {EMAIL_TO}")
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=EMAIL_TO,
                    msg=f"Subject:Look Up👆👆\n\nISS Satelite is overhear"
                )
                print(f"Email Successfully Sent to - {EMAIL_TO}")

        except Exception as e:
            print(e)