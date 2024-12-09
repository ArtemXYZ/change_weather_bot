"""
    3. Логика обработки данных для Телеграм-бота

    Ваша задача — периодически проверять данные и сравнивать их с предыдущими. Так как NOAA API не предоставляет триггеры, вы можете:

    Периодический сбор данных:
    Используйте aiogram3 с BackgroundScheduler или асинхронные таймеры для регулярных запросов (например, каждые 30–60 минут).

    Сравнение прогнозов:

    Сохраняйте последний прогноз (например, в базу данных или кэш).
    При новом запросе сравнивайте ключевые параметры (температура, осадки, ветер).
    Настройка уведомлений:

    Если изменения превышают определенный порог (например, разница температуры более 2°C или добавление дождя), отправляйте уведомление пользователю.

    5. Анализ частоты запросов
    Частота обновлений: NOAA обновляет прогнозы каждые 1–3 часа.
    Оптимизация запросов:
    Не запрашивайте прогнозы чаще, чем каждые 30 минут (иначе запросы становятся избыточными).
    Группируйте запросы: если пользователи в одном регионе, используйте одну точку API для всех.
    Эта стратегия минимизирует нагрузку на API и оптимизирует рентабельность приложения.

"""


# --------------------------------------- 2. Методы NOAA API для прогноза ---------------------------------------

# 2.1. --------------------------------------- Получение точки сетки
# GET https://api.weather.gov/points/40.7128,-74.0060'
Endpoint = 'https://api.weather.gov/points/{latitude},{longitude}'


# Пример ответа (сокращено):
json = {
  "properties": {
    "gridId": "OKX",
    "gridX": 33,
    "gridY": 35,
    "forecastHourly": "https://api.weather.gov/gridpoints/OKX/33,35/forecast/hourly"
  }
}



# 2.2. --------------------------------------- Получение почасового прогноза ---------------------------------------
Endpoint = 'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast/hourly'

# Пример запроса: GET https://api.weather.gov/gridpoints/OKX/33,35/forecast/hourly
# Пример ответа (сокращено):
json = {
  "properties": {
    "periods": [
      {
        "number": 1,
        "startTime": "2024-12-07T10:00:00-05:00",
        "endTime": "2024-12-07T11:00:00-05:00",
        "temperature": 12,
        "temperatureUnit": "C",
        "windSpeed": "5 km/h",
        "shortForecast": "Partly Cloudy"
      },
      {
        "number": 2,
        "startTime": "2024-12-07T11:00:00-05:00",
        "endTime": "2024-12-07T12:00:00-05:00",
        "temperature": 14,
        "temperatureUnit": "C",
        "windSpeed": "7 km/h",
        "shortForecast": "Mostly Sunny"
      }
    ]
  }
}




# # Формируем URL для почасового прогноза
# forecast_url = f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast/hourly"
# response = requests.get(forecast_url)
# forecast_data = response.json()
#
# # Берем прогнозы
# for period in forecast_data["properties"]["periods"]:
#     print(f"{period['startTime']}: {period['shortForecast']} ({period['temperature']}°{period['temperatureUnit']})")





import requests
from datetime import datetime

# 1. Получение координатной точки
def get_grid_point(lat, lon):
    response = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    response.raise_for_status()
    data = response.json()
    return data["properties"]["gridId"], data["properties"]["gridX"], data["properties"]["gridY"]




# 2. Получение почасового прогноза
def get_hourly_forecast(gridId, gridX, gridY):
    url = f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast/hourly"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["properties"]["periods"]



# 3. Проверка изменений и уведомление
def check_weather_changes(last_forecast, current_forecast):
    # Пример сравнения температуры
    if last_forecast["temperature"] != current_forecast["temperature"]:
        return f"Температура изменилась: {last_forecast['temperature']}°C → {current_forecast['temperature']}°C"
    return None

# Пример использования
if __name__ == "__main__":
    latitude = 40.7128
    longitude = -74.0060
    gridId, gridX, gridY = get_grid_point(latitude, longitude)

    # Первый запрос
    forecasts = get_hourly_forecast(gridId, gridX, gridY)
    last_forecast = forecasts[0]  # Берем ближайший прогноз

    # Пример: имитация обновления через час
    current_forecast = get_hourly_forecast(gridId, gridX, gridY)[0]
    message = check_weather_changes(last_forecast, current_forecast)
    if message:
        print(f"Изменение погоды: {message}")