import requests

def get_currency() -> dict[str,float]:
  url=f"https://api.nbp.pl/api/exchangerates/tables/a"

  try:
    response = requests.get(url)
    data = response.json()
    rates = data[0]["rates"]
    selected_rates = {rate["code"]:rate["mid"] for rate in rates if rate["code"] in ("USD", "EUR")}
    return selected_rates

  except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
  return {}


if __name__ == "__main__":
  get_currency()