import requests
import smtplib

# TODO: Update your email, password and recipient
my_email = "" # here you have to write the email
# Don't let anyone see your password!
password = "" # here you have to write the password of the email that is going to send the mssg
recipient = "" # here you have to write the email recipient

##### Weather Alert Code #####
open_weather_map_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = # write your API Key from Weather Alert Code

##### Weather parameters #####
# TODO: Change your latitude and longitude to your current place
# these parameters name are according to the API, this one:
# https://api.openweathermap.org/data/2.5/onecall?lat=25.679041600&lon=-100.2815700&appid=2e24842b55023e6c9f9d2387841f4aa7
# but instead of writing everything, it's easier to have it like this as well.
weather_params = {
    "lat": 100,
    "lon": 200,
    "units": "metric",
    "appid": api_key,
    "exclude": "current,minutely,hourly"
}

###### API INFORMATION ########
response = requests.get(open_weather_map_endpoint, params = weather_params)
response.raise_for_status()
data = response.json()
daily_weather_data = data["daily"]

###### Taking the weather data for the next 12 hours ########
#first_seven_days = daily_weather_data[0]
#print(first_seven_days[0])

day = 0
not_finished = True

for i in daily_weather_data:
    if day >= 1:
        not_finished = True
        break
    else:
        first_seven_days_temperature = daily_weather_data[day]
        # for checking a dictionary
        temperature = first_seven_days_temperature["temp"]
        day_temperature = temperature["day"]
        day_min_temperature = temperature["min"]
        print(f"The daily weather is {day_temperature} and the minimum temperature is {day_min_temperature}")

        # for checking the list
        first_seven_days_weather = first_seven_days_temperature["weather"]
        first_seven_days_weather_number = first_seven_days_weather[0]["id"]
        print(f"And the weather will be: {first_seven_days_weather_number}")

        day += 1

###### Dictionary to save the variables inside ########

weather_of_the_day = {}
weather_of_the_day["Daily Weather"] = day_temperature
weather_of_the_day["Minimum Temperature"] = day_min_temperature
weather_of_the_day["Clouds"] = first_seven_days_weather_number
print(weather_of_the_day)

###### Clouds in the sky ########
if weather_of_the_day["Clouds"] == 800:
    cloud_message = "Cielo Despejado"
elif weather_of_the_day["Clouds"] == 801:
    cloud_message = "Pocas Nubes"
elif weather_of_the_day["Clouds"] == 802:
    cloud_message = "Cielo Medionublado"
elif weather_of_the_day["Clouds"] == 803:
    cloud_message = "Cielo Parcialmente Nublado"
elif weather_of_the_day["Clouds"] == 804:
    cloud_message = "Cielo Nublado"
else:
    cloud_message = "Cielo que no está bien identificado como estará durante el día, mejor revisar en las noticias"

message = f"La temperatura de hoy es {weather_of_the_day['Daily Weather']} con una minima de {weather_of_the_day['Minimum Temperature']} y un {cloud_message}"
print(message)

##### Send Message #####
with smtplib.SMTP("smtp.gmail.com") as connection:
    # tls stands for transport layer security and is a way of securing our connection to our email server
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=recipient,
                        msg=f"Subject: Temperatura de Monterrey\n\nPadre, desarrolle este algoritmo que te estara mandando la temperatura en Monterrey, aqui aparece desglozada\n\n{message}")