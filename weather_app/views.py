#first core python, then external
import datetime
import requests
from django.shortcuts import render

# Create your views/endpoints here.

def index(request):
    
    API_KEY = ""
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST": 
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None) #city 2 is optional

        weather_data_1, daily_forecasts_1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data_2, daily_forecasts_2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data_2, daily_forecasts_2 = None, None

        context = {
            "weather_data_1" : weather_data_1,
            "daily_forecasts_1": daily_forecasts_1,
            "weather_data_2" : weather_data_2,
            "daily_forecasts_2": daily_forecasts_2,
        }

        return render(request, "weather_app/index.html", context)
    
    else:
        #if it's a get request we render our html template
        return render(request, "weather_app/index.html")
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    
    current_weather_response = requests.get(current_weather_url.format(city, api_key)).json()
    print(current_weather_response)
    lat, lon = current_weather_response['coord']['lat'], current_weather_response['coord']['lon']
    
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    print(forecast_response)
    #Dictionary to pass data to the html template
    weather_data = {
        "city": city,
        "temperature": round(current_weather_response['main']['temp'] - 273.15, 2), #it's in kelvin originally
        "description": current_weather_response['weather'][0]['description'],
        "icon": current_weather_response['weather'][0]['icon']
    }

    daily_forecasts = []
    #daily_data -> datos de cada día
    for daily_data in forecast_response['daily'][:5] :
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return  weather_data, daily_forecasts