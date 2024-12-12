
from cores.core_NOAA.change_weather import *
from cores.core_OpenWeathermap.translator import translate_from_language
from cores.core_OpenWeathermap.change import *
from config_pack.configs import API_WEATHER

from cores.coordinate_data import *
# from config_pack.code_printer import beauty_code



async def run_tests():


    input_city_name = input(f'Введите название города: ')

    city_name_eng = await translate_from_language(input_city_name, 'en')
    print(city_name_eng)

    # 1. Получаем координаты города
    # latitude, longitude, country_code = await get_country_coordinate(API_WEATHER, city_name_eng, input_limit=1)
    # print(latitude, longitude,)

    jsson_ = await decode_address(city_name_eng)



    # pogoda = await get_hourly_forecast(latitude, longitude)
    # print(pogoda)

if __name__ == "__main__":
    asyncio.run(run_tests())