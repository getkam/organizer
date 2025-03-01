import requests

def time_service(continent: str, city:str):
    LOCATIONS = ["Europe%2FLondon", "America%2FNew_york", "Asia%2FKolkata"]
    url = f"https://timeapi.io/api/time/current/zone?timeZone={continent}%2F{city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        timezone = response.json()
       
        print(f"Currently in {city} is: {timezone['dayOfWeek']}, {timezone['year']}-{timezone['month']:02d}-{timezone['day']:02d} {timezone['hour']:02d}:{timezone['minute']:02d}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
