import aiogram
import asyncio
# import requests
from io import BytesIO
from PIL import Image
import re

import aiohttp
# -------------------------------- Локальные модули
from config_pack.configs import *

# ----------------------------------------------------------------------------------------------------------------------

# Функция для интерпретации данных погоды
# def interpret_weather(data):
#     weather_description = data['weather'][0]['description']
#     temperature = data['main']['temp']
#     feels_like = data['main']['feels_like']
#     temp_min = data['main']['temp_min']
#     temp_max = data['main']['temp_max']
#     pressure = data['main']['pressure']
#     humidity = data['main']['humidity']
#     wind_speed = data['wind']['speed']
#     clouds = data['clouds']['all']
#
#     # Форматирование строки вывода
#     output = (f"Погода в {data['name']}, {data['sys']['country']}: "
#               f"{weather_description},\n"
#               f"температура: {temperature}°C (ощущается как {feels_like}°C),\n"
#               f"мин/макс температура: {temp_min}/{temp_max}°C,\n"
#               f"атмосферное давление: {pressure} гПа,\n"
#               f"влажность: {humidity}%,\n"
#               f"скорость ветра: {wind_speed} м/с,\n"
#               f"облачность: {clouds}%")
#
#     return output


# Маппинг иконок погоды на эмодзи
icon_to_emoji = {
    '01d': '☀️', '01n': '🌑',  # ясное небо
    '02d': '🌤', '02n': '🌥',  # немного облачно
    '03d': '☁️', '03n': '☁️',  # облачно
    '04d': '🌥', '04n': '🌥',  # очень облачно
    '09d': '🌧', '09n': '🌧',  # дождь
    '10d': '🌦', '10n': '🌧',  # сильный дождь
    '11d': '⛈', '11n': '⛈',  # гроза
    '13d': '❄️', '13n': '❄️',  # снег
    '50d': '🌫', '50n': '🌫',  # туман
}


async def get_icon(icon: str):
    """
    Получаем URL-строку иконки от серера по идентификатору из json
    01n.png -> 01d
    """

    # Используем регулярное выражение для замены 'n' на 'd'
    icon_new = re.sub(r'n', 'd', icon)
    url_icon = (f'https://openweathermap.org/img/wn/{icon_new}@2x.png')

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url_icon) as response:
    #
    #         icon_data = await response.read()
    #         icon_png = Image.open(BytesIO(icon_data))
    #
    #         # Сохранение изображения в байтовый поток
    #         img_byte_arr = BytesIO()
    #         icon_png.save(img_byte_arr, format='PNG')
    #         img_byte_arr.seek(0)
    #
    # return img_byte_arr
    return url_icon


async def get_icon_emoji(icon: str):
    """
    Получаем соответствующий эмодзи для иконки погоды
    """
    icon_emoji = icon_to_emoji.get(icon, '')
    return icon_emoji


async def get_country_coordinate(API_WEATHER, input_city_name, input_limit=None):
    """
    Узнаем координаты и код страны для города
    :param API_WEATHER: API ключ для OpenWeatherMap
    :param input_city_name: Название города
    :param input_limit: Лимит результатов (по умолчанию 1)
    :return: Координаты и код страны

    """

    if input_limit is None:

        url = (f'http://api.openweathermap.org/geo/1.0/direct?q={input_city_name}&appid={API_WEATHER}')

    else:

        url = (
            f'http://api.openweathermap.org/geo/1.0/direct?q={input_city_name}&limit={input_limit}&appid={API_WEATHER}'
        )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data:
                return data[0]['lat'], data[0]['lon'], data[0].get('country')
            else:
                print("Город не найден")
                return None, None, None

                # raise ValueError("Город не найден")


async def get_weather_by_coordinate(lat, lon, API_WEATHER, url_type_prognosis: str):
    """
     Узнаем погоду по координатам.

    :param lat: Широта
    :param lon: Долгота
    :param API_WEATHER: API ключ для OpenWeatherMap
    :return: Данные о погоде

    metric  - units	необязательно	Доступны единицы измерения. standard, metric и imperial единицы измерения.
    cnt - Чтобы ограничить количество временных меток в ответе API, пожалуйста, настройте cnt.



    """

    # По условию выдаем тип  url для получения различного рода прогноза, возвращаем json

    if url_type_prognosis == 'now':  # Прогноз сейчас +

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_WEATHER}&units=metric'

    elif url_type_prognosis == '5day':  # Прогноз на 5 дней с разбивкой по 3 часа + (в нашем варианте = 48 часов).

        # Запрос по этому URL возвращает прогноз погоды с часовым интервалом на ближайшие 48 часов и текущие данные,
        # исключая данные по минутам и ежедневные прогнозы.
        url = (f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,'
               f'daily&appid={API_WEATHER}&units=metric')

        # minutely: Исключает данные о погоде по минутам.
        # В запросе /data/2.5/onecall можно получить данные о погоде каждую минуту,
        #  но если вам не нужны такие данные, вы можете исключить их с помощью этого параметра.

        # daily: Исключает данные о погоде по дням.
        # В запросе /data/2.5/onecall вы можете получить ежедневный прогноз на несколько дней вперед.
        # Если вам нужны только краткосрочные данные, например, почасовой прогноз, вы можете исключить эти данные.

    # elif url_type_prognosis == 'week':  # Прогноз на неделю +

    # url = (f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,'
    #        f'alerts&appid={API_WEATHER}&units=metric&lang=ru')

    # elif url_type_prognosis == 'in_date':  # Прогноз на дату

    # url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_WEATHER}&units=metric'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

    # prognosis = []
    # for day in data['daily']:
    #     date = datetime.datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
    #     temperature_day = day['temp']['day']
    #     temperature_night = day['temp']['night']
    #     description = day['weather'][0]['description']
    #     icon = day['weather'][0]['icon']
    #     icon_url = await get_icon_url(icon)
    #
    #     prognosis.append(f"{date} - {description}, днём: {temperature_day}°C, ночью: "
    #                      f"{temperature_night}°C, [Иконка]({icon_url})")


# Выдать погоду (json на выходе)
async def get_weather(input_city_name, API_WEATHER, url_type_prognosis: str = 'now'):
    try:

        # 1. Получаем координаты города
        lat, lon, country_code = await get_country_coordinate(API_WEATHER, input_city_name, input_limit=1)

        # Получаем прогноз в json
        weather_data = await get_weather_by_coordinate(lat, lon, API_WEATHER, url_type_prognosis)
        return weather_data

    except Exception as e:
        print(f'Ошибка: {e}')

# ----------------------------------------------------------------------------------------------------------------------
# f'http://api.openweathermap.org/geo/1.0/direct?q={input_city_name},
# {state code},{country code}&limit={limit}&appid={get_api_weather}')

# Параметры вызова API геокодирования
# q	требуется.
# Название города, код штата (только для США) и код страны через запятую.
# Пожалуйста, используйте коды стран ISO 3166.

# appid	требуется.
# Ваш уникальный ключ API (вы всегда можете найти его на странице своей учетной записи во вкладке "Ключ API")

# limit	необязательно
# Количество местоположений в ответе API (в ответе API может быть возвращено до 5 результатов)
