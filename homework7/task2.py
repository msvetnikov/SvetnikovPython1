import requests

API_KEY = "ВАШ_API_КЛЮЧ"
city = input("Введите название города: ")

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "ru"
}

response = requests.get(url, params=params)
data = response.json()

if response.status_code == 200:
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"Температура в {city}: {temp}°C")
    print(f"Описание погоды: {description}")
else:
    print("Ошибка:", data.get("message", "Не удалось получить данные"))
