
class Weather():
  ICONS = {
    "clouds": "\u2601\uFE0F",       # ☁️
    "rain": "\U0001F327\uFE0F",      # 🌧️
    "clear": "\u2600\uFE0F",         # ☀️
    "thunderstorm": "\u26C8\uFE0F",  # ⛈️
    "drizzle": "\U0001F326\uFE0F",   # 🌦️
    "snow": "\u2744\uFE0F"  ,         # ❄️
    "mist":"\U0001F32B\uFE0F"

  }

  def __init__(self, data: dict):
    self.current: int = int(data['current']['temp']) - 273
    self.feel_like: int = int(data['current']['feels_like']) - 273
    self.timezone: str = data['timezone']
    self.weather_main:str = data["current"]["weather"][0]["main"]
    self.weather_description:str = data["current"]["weather"][0]['description']

  def get_icon(self):
    return self.ICONS[self.weather_main.lower()]
