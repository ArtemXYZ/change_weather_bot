"""
    pass
"""

import asyncio
import aiohttp
from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------
async def get_response_aiohttp(url):
    """
       Функция для выполнения асинхронных запросов.
    """

    # try:

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

    # except Exception as e:
    #     print(f'Ошибка в "change_weather.get_response_aiohttp": {e}')


# 1. --------------------------------------- Получение точки сетки:
async def get_grid_json(latitude, longitude):
    """
       Получение координатной точки.
       # GET https://api.weather.gov/points/40.7128,-74.0060'

        # Пример ответа (сокращено):
        json = {
          "properties": {
            "gridId": "OKX",
            "gridX": 33,
            "gridY": 35,
            "forecastHourly": "https://api.weather.gov/gridpoints/OKX/33,35/forecast/hourly"
          }
        }
    """

    try:

        return await get_response_aiohttp(f"https://api.weather.gov/points/{latitude},{longitude}")

    except Exception as e:
        print(f'Ошибка в "change_weather.get_grid_point": {e}')


# async def get_grid_point(json):
#
#     try:
#
#         if json:
#             return json["properties"]["gridId"], json["properties"]["gridX"], json["properties"]["gridY"]
#         else:
#             print("координатная точка не найдена.")
#             return None
#
#     except Exception as e:
#         print(f'Ошибка в "change_weather.get_grid_point": {e}')







# 2. --------------------------------------- Получение почасового прогноза:
async def get_hourly_forecast_json(gridId, gridX, gridY):
    """
         Получение почасового прогноза.
         # Пример входящих значений (сокращено):
            "gridId": "OKX",
            "gridX": 33,
            "gridY": 35,

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
    """

    try:
        json = await get_response_aiohttp(
            f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast/hourly"
        )
        return json

    except Exception as e:
        print(f'Ошибка в "change_weather.get_hourly_forecast": {e}')



# ----------------------------------------------------------------------------------------------------------------------



async def get_hourly_forecast(latitude, longitude):
    """
        Получаем погоду, финальная функция.
    """

    grid_json = await get_grid_json(latitude, longitude)

    if grid_json:
            gridId = grid_json["properties"]["gridId"]
            gridX = grid_json["properties"]["gridX"]
            gridY = grid_json["properties"]["gridY"]
    else:
        print("Координатная точка не найдена.")
        # айограмм отправка сообщения

    forecasts_json = await get_hourly_forecast_json(gridId, gridX, gridY)

    if forecasts_json:
        return forecasts_json["properties"]["periods"]  # forecasts

    else:
        print("Получение почасового прогноза завершилось неудачей.")
        # айограмм отправка сообщения











# ----------------------------------------------------------------------------------------------------------------------



