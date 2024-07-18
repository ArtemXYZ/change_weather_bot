"""
Роутер взаимодействия с пользователем
"""

# -------------------------------- Стандартные модули
import asyncio
# from googletrans import Translator
from pprint import pprint

# -------------------------------- Сторонние библиотеки
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.client.default import DefaultBotProperties  # Обработка текста HTML разметкой
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# -------------------------------- Локальные модули
# from handlers.text_message import *  # Список ругательств:
# from filters.chats_filters import *
from core.translator import *

# from aiogram.utils.formatting import as_list, as_marked_section, Bold, Italic

# from menu import keyboard_menu  # Кнопки меню - клавиатура внизу


from menu.button_generator import *  # Кнопки встроенного меню - для сообщений

# from working_databases.query_builder import *
# from working_databases.events import *
from handlers.all_states import *

from core.change import *

# ----------------------------------------------------------------------------------------------------------------------
# Назначаем роутер для всех типов чартов:
user_router = Router()


# фильтрует (пропускает) только личные сообщения и только определенных пользователей:
# oait_router.message.filter(ChatTypeFilter(['private']), TypeSessionFilter(allowed_types=['oait']))
# oait_router.edited_message.filter(ChatTypeFilter(['private']), TypeSessionFilter(allowed_types=['oait']))


# ----------------------------------------------------------------------------------------------------------------------


# =========================  0. Старт бота  ========================:
@user_router.message(CommandStart())
async def start_and_hi_users(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.delete()

    # await state.set_state(InputUser.hi)

    user_id = message.from_user.id

    await bot.send_message(
        chat_id=user_id,
        text=f'Вас приветствует бот отслеживания изменений погоды.\n'
             f'Я умею отправлять уведомления о превышении заданных пороговых значений изменения показателей погоды.'
             f'Например, я могу оповещать тебя, если температура или скорость ветра увеличатся или уменьшатся больше,'
             f' чем на какое то определенное значение и многое другое...\n'
        , reply_markup=get_keyboard('Погода сейчас', 'Прогноз на неделю',
                                    'Прогноз на дату', 'Оповещение по триггеру', sizes=(2, 2,)))


# =========================  1. Погода сейчас  ========================:
@user_router.message(StateFilter(None), F.text == 'Погода сейчас')
async def click_weather_now(message: types.Message, state: FSMContext):  # , bot: Bot

    await message.delete()  # Удаляем текст от кнопки.

    await message.answer(text=f'Введите наименование города.')

    await state.set_state(InputUser.get_city)


@user_router.message(StateFilter(InputUser.get_city), or_f(F.text, ~CommandStart()))  #
async def get_city_weather_now(message: types.Message, state: FSMContext, bot: Bot):
    """

    :param message:
    :param state:
    :param bot:
    :return:

    Интерпритатор:
    {'base': 'stations',   # base: указывает на источник данных (Базовая станция данных, от метеорологических станций
     'clouds': {'all': 0},                       # all: Облачность в процентах
     'cod': 200,                                 # cod: Код состояния HTTP-запроса (200 указывает на успешный запрос).
     'coord': {'lat': 51.2305, 'lon': 58.4738},  # coord: Координаты местоположения. lat: Широта, ...
     'dt': 1719948052,                        # dt: Временная метка в формате UNIX (1719948052).
     'id': 514734,                            # id: Идентификатор города.

     'main': {'feels_like': 20.44,            # main: Основные параметры погоды, feels_like: Ощущаемая температура °C
              'grnd_level': 979,              # grnd_level: Давление на уровне земли (979 гПа).
              'humidity': 77,    +             humidity: Влажность (77%).
              'pressure': 1007,               pressure: Давление (1007 гПа).
              'sea_level': 1007,             - sea_level: Давление на уровне моря (1007 гПа).
              'temp': 20.34,                 + temp: Текущая температура (20.34°C).
              'temp_max': 20.34,             + temp_max: Максимальная температура (20.34°C).
              'temp_min': 20.34},            + temp_min: Минимальная температура (20.34°C).
     'name': 'Orsk',                         +  name: Название города
     'sys': {'country': 'RU',                - sys: Системная информация, country: Страна (RU).
             'id': 9040,                      id: Идентификатор
             'sunrise': 1719964570,          + sunrise: Время восхода солнца в формате UNIX (1719964570).
             'sunset': 1720023854,           + sunset: Время заката солнца в формате UNIX (1720023854).
             'type': 1},                      type: Тип системной информации (1).
     'timezone': 18000,                      + timezone: Часовой пояс в секундах (18000, что соответствует UTC+5).
     'visibility': 10000,                     visibility: Видимость в метрах (10000 м).
     'weather': [{'description': 'clear sky', + weather: Описание погодных условий, description: Описание погоды
                  'icon': '01n',              + icon: Иконка погоды (01n).
                  'id': 800,                  id: Идентификатор погодного состояния (800).
                  'main': 'Clear'}],         + main: Основное состояние (Clear - ясно).
     'wind': {'deg': 280, 'speed': 4}}   + wind: Информация о ветре, deg: Направление ветра, speed: Скорость ветра, м/с


    """

    city_name_no_translate = message.text
    city_name_eng = await translate_from_language(city_name_no_translate, 'en')
    data = await get_weather(city_name_eng, API_WEATHER)

    pprint(data)

    # Интерпритатор:

    weather_description = data['weather'][0]['description']

    # Получаем иконку от серера по идентификатору из json (01n.png -> 01d)
    url_icon = await get_icon(data['weather'][0]['icon'])

    icon_emoji = await get_icon_emoji(data['weather'][0]['icon'])
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    clouds = data['clouds']['all']

    # Определить язык пользователя по координатам по вводу. todo сделать клавиатуру или спрашивать.
    city_name_original = await translate_from_language((data['name']), 'ru')
    weather_description_original = await translate_from_language(weather_description, 'ru')

    # Форматирование строки вывода
    weather_report = (f"В городе {city_name_original}:"  # , {data['sys']['country']}
                      f" {weather_description_original} {icon_emoji}.\n"

                      f"Температура: {temperature}°C (ощущается как {feels_like} °C).\n"
                      f"мин/макс температура: {temp_min}/{temp_max} °C.\n"
                      f"Атмосферное давление: {pressure} гПа.\n"
                      f"Влажность: {humidity}%.\n"
                      f"Скорость ветра: {wind_speed} м/с.\n"
                      f"Облачность: {clouds}%"

                      )

    # await message.reply(text=weather_report, parse_mode='HTML')
    await message.reply_photo(photo=url_icon, caption=weather_report, parse_mode='HTML')
    await state.clear()


# # Отправка изображения как фото вместе с текстовым сообщением
#             await message.reply_photo(photo





# =========================  2. Прогноз на неделю ========================:
@user_router.message(StateFilter(None), F.text == 'Прогноз на неделю')
async def click_weather_week(message: types.Message, state: FSMContext):  # , bot: Bot

    await message.delete()  # Удаляем текст от кнопки.

    await message.answer(text=f'Введите наименование города.')

    await state.set_state(InputUser.get_city)


# @user_router.message(StateFilter(InputUser.get_city), or_f(F.text, ~CommandStart()))  #
# async def get_city_weather_week(message: types.Message, state: FSMContext, bot: Bot):
#
#     ...




# =========================  4. Оповещение по триггерую ========================:
@user_router.message(StateFilter(None), F.text == 'Оповещение по триггеру')
async def click_weather_week(message: types.Message, state: FSMContext):  # , bot: Bot

    await message.delete()  # Удаляем мусорный текст от кнопки.

    await message.answer(text=f'Если тебе не охото мониторить постоянно погоду, я могу это делать за тебя и '
                              f'присылать оповещения, только, если вдруг прогноз погоды изменится свыше заданных'
                              f' тобой параметров. Другими словами - это триггер на изменения. Это удобно.'
                              f' Например, если ты редко наблюдаешь за погодой, но хотел бы знать, если что-то '
                              f'координально изменится или просто хотел бы делегировать мне мониторинг.',
                         reply_markup=get_callback_btns(btns={'Перейти к созданию триггера': 'get_trigger',
                                                              'Отмена': 'go_back'}, sizes=(1,))
                         )


# Предлагаем ввести город
@user_router.callback_query(StateFilter(None), F.data.startswith('get_trigger'))
async def get_trigger(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

    await callback.answer() # ответ для сервера о нажатии кнопки.


    # Изменяем предыдущее состояние
    await callback.message.edit_text(text=f'Хорошо. Для начала определимся с локацией.\n'
                                          f'Для какого города нужно будет отслеживать изменения? '
                                          f'Введите наименование города.')


    await state.set_state(InputUser.get_city_trigger)


# Ожидаем ввода города (работает в паре с get_trigger)
@user_router.message(StateFilter(InputUser.get_city_trigger), or_f(F.text, ~CommandStart()))  #
async def get_city_weather_trigger(message: types.Message, state: FSMContext, bot: Bot):

    city_name_no_translate = message.text
    city_name_eng = await translate_from_language(city_name_no_translate, 'en')

    await state.update_data(city_name_eng=city_name_eng)


    await message.delete()  # Удаляем введенный текст.


    await message.answer(text=f'Где отслеживать, я понял ({city_name_no_translate}).'                             
                              f'Теперь нужно задать параметры триггера.'
                              f'Какие именения нужно будет отслеживать?'
                              f'В стандартный набор параметров входят: температура, скорость ветра'

                              , reply_markup=get_callback_btns(
        btns={'Температуру': 'get_temperature',
              'Атмосферное давление': 'pressure',
              'Влажность': 'humidity',
              'Скорость ветра': 'wind_speed',
              'Облачность': 'clouds',
              'Все параметры': 'all_params',
              'Отмена': 'go_back'}, sizes=(2, 2, 2, 1, ))
                                     )


    # какие параметры добавить и как добавлять придумать механизм
    # Создать обработк с множеством келбеков на вход ( только те параметры с кнопок)
    # далее когда нажимаем кнопки они добавляются в список, а сообщение изменяется записывая на баннер список этих параметров.
    # кнопка далее возьмет этот список и применит кнашему запросу.


    # еще необходим обработчик задающий для каждого параметра значение (больше меньше равно и само значение)


    # достать из стейта город

    # lat, lon, country_code = await get_country_coordinate(API_WEATHER, city_name_eng, input_limit=1) нужно в сл обработчике



    # data = await 'trigger')



    # 'trigger':  # Прогноз по триггеру
    # pprint(data)




#     # Изменяем предыдущее состояние
#     await callback.message.edit_text(text=f'Хорошо. Дя начала определимся с параметрами триггера.\n'
#                                           f'Какие именения нужно будет отслеживать? ', reply_markup=get_callback_btns(
#         btns={'Температуру': 'get_temperature',
#               'Атмосферное давление': 'pressure',
#               'Влажность': 'humidity',
#               'Скорость ветра': 'wind_speed',
#               'Облачность': 'clouds',
#               'Все параметры': 'all_params',
#               'Отмена': 'go_back'}, sizes=(2, 2, 2, 1, ))
#                                      )
#
# # мин/макс температура




# Донор

# @user_router.callback_query(StateFilter(AddRequests.send_message_or_add_doc), F.data.startswith('skip_and_send'))
# async def skip_and_send_message_users(callback: types.CallbackQuery,
#                                       state: FSMContext, session: AsyncSession, bot: Bot):  # message: types.Message,
#
#     # Получаем данные из предыдущего стейта:
#     back_data_tmp = await state.get_data()
#
#     # Передадим на изменение в следущее сообщение:
#     # edit_chat_id_final = back_data_tmp['edit_chat_id']
#     # edit_message_id_final = back_data_tmp['edit_message_id']
#
#     # удаляем их для корректной передачи на запись в бд.
#     del back_data_tmp['edit_chat_id']
#     # edit_chat_id_new = data_write_to_base.get('edit_chat_id')
#     del back_data_tmp['edit_message_id']
#
#     await state.clear()
#
#     await state.set_state(AddRequests.transit_request_message_id)
#
#     # обновляем изменения
#     await state.update_data(back_data_tmp)
#     # Значение для колонки в обращениях, что нет документов (data_request_message['doc_status'] = False)
#     await state.update_data(doc_status=False)
#
#     # Запрос в БД на добавление обращения:
#     data_request_message_to_send = await state.get_data()
#
#     # Вытаскиваем данные из базы после записи (обновленные всю строку полностью) и отправляем ее в другие стейты:
#     # Забираю только айди что бы идентифицировать задачу:
#     refresh_data = await add_request_message(session, data_request_message_to_send)
#     print(f'refresh_data = {refresh_data}')
#
#     await state.update_data(requests_ia=refresh_data)
#     back_data_transit = await state.get_data()
#
#     bot = callback.bot
#     # bot = message.bot
#     await bot.send_message(chat_id=500520383,
#                            text=f'Новая задача, id: {back_data_transit}'  # ЗАМЕНИТЬ НА refresh_data
#                            , reply_markup=get_callback_btns(
#             btns={'📨 ЗАБРАТЬ ЗАЯВКУ': 'pick_up_request',
#                   '📂 ПЕРЕДАТЬ ЗАЯВКУ': 'transfer_request'},
#             sizes=(1, 1))
#                            )
#
#     # # Получаем ID отправленного сообщения
#     # message_id = sent_message.message_id
#     # print(f'ID отправленного сообщения: {message_id}')
#
#     await state.clear()


# Приветствие для ОАИТ
# @oait_router.message(StateFilter(None), F.text == 'next')
# async def hello_after_on_next(message: types.Message):
#     user = message.from_user.first_name  # Имя пользователя
#     await message.answer((hello_users_oait.format(user)),
#                          parse_mode='HTML')


# ) or (F.text == 'Прогноз на дату') or (F.text == 'Создать триггер')
