import requests
from dotenv import load_dotenv
import os

from organizer.models.weather import Weather

load_dotenv()
api_key = os.getenv("API_KEY_WEATHER")


def get_weather() -> Weather:
  lat = "52.2585223"
  lon = "21.1582986"
  url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"

  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
  except requests.exceptions.HTTPError as e:
      print(f"HTTP Error: {e}")
  except requests.exceptions.RequestException as e:
      print(f"Error: {e}")
  
  #print(data)
  return Weather(data)


if __name__ == '__main__':
   get_weather()
