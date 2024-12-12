"""
    Модуль содержит функции асинхронного подключения к базам данных.
    Для асинхронного подключения обязательно использовать конфиг типа: CONFIG_RNAME=postgresql+asyncpg.
    Обязательна установка библиотеки asyncpg.
"""
# check_telegram_id
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек
# import logging
# import pprint
# ---------------------------------- Импорт сторонних библиотек
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# -------------------------------- Локальные модули
from config.configs import *


# ======================================================================================================================
# Создаем URL строку:
def get_url_string(ANY_CONFIG: dict | URL | str) -> object:
    # Проверка типа входной конфигурации подключения:
    # Если на вход конфигурация в словаре:
    if isinstance(ANY_CONFIG, dict) == True:
        url_string = URL.create(**ANY_CONFIG)  # 1. Формируем URL-строку соединения с БД.
        #  Эквивалент: url_conf_locdb = (f'{drivername}://{username}:{password}@{host}:{port}/{database}')

    # Если на вход url_conf_locdb:
    elif isinstance(ANY_CONFIG, str) == True:
        url_string = ANY_CONFIG
    else:
        url_string = None

    return url_string
    # return create_async_engine(url_conf_locdb)

# ----------------------------------------------------------------------------------------------------------------------
# Синхронные подключения:
url_string = get_url_string(CONFIG_MART_SV)
sinc_engine_mart_sv = create_engine(url_string) # , echo=True

# ----------------------------------------------------------------------------------------------------------------------
#                                                           ***
# ----------------------------------------------------------------------------------------------------------------------
# Асинхронные подключения:
# ------------------------------------------- Создаем общую сессию с локальной бд для всех модулей:
locdb_conf = get_url_string(CONFIG_LOCAL_DB)
locdb_engine = create_async_engine(locdb_conf)  # , echo=True (Для логирования)!
LOCDB_SESSION = async_sessionmaker(bind=locdb_engine, class_=AsyncSession, expire_on_commit=False)  #

# ------------------------------------------- Создаем общую сессию с удаленными бд для всех модулей:
sky_conf = get_url_string(CONFIG_SKY_NET_ASYNCPG)
sky_engine = create_async_engine(sky_conf)  # , echo=True (Для логирования)!
SKY_SESSION = async_sessionmaker(bind=sky_engine, class_=AsyncSession, expire_on_commit=False)  #False


async def get_ldb_session(session: AsyncSession = LOCDB_SESSION) -> AsyncSession:
    """
        Функция возвращает готовый объект сессии (AsyncSession) с локальной базой данных.
        Предназначена для передачи как вложенной в другие функции, что позволит при необходимости менять сессию
        только в 1 месте.
    """

    return session()


async def get_rdb_session(session: AsyncSession = SKY_SESSION) -> AsyncSession:
    """
        Функция возвращает готовый объект сессии (AsyncSession) с удаленной базой данных.
        Предназначена для передачи как вложенной в другие функции, что позволит при необходимости менять сессию
        только в 1 месте.
    """
    return session()



# async def _get_rdb_session() -> AsyncSession:
#     """
#         Функция возвращает готовый объект сессии (AsyncSession) с удаленной базой данных.
#         Предназначена для передачи как вложенной в другие функции, что позволит при необходимости менять сессию
#         только в 1 месте.
#     """
#
#     return SKY_SESSION()


# async def get_rdb_session() -> AsyncSession:
#     """
#         Функция возвращает готовый объект сессии (AsyncSession) с удаленной базой данных.
#         Предназначена для передачи как вложенной в другие функции, что позволит при необходимости менять сессию
#         только в 1 месте.
#     """
#     # создание сессии
#     session = SKY_SESSION()
#     return session
