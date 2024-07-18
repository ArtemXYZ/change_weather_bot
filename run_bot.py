# ----------------------------------------------------------------------------------------------------------------------
"""
Чат бот отслеживания изменения погоды
"""
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- Стандартные модули
import os
import asyncio
# import logging
# logging.basicConfig(level=logging.INFO)
# -------------------------------- Сторонние библиотеки
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties  # Обработка текста HTML разметкой

# -------------------------------- Локальные модули
from config_pack.configs import *
from handlers.user_module import *

# ----------------------------------------------------------------------------------------------------------------------
# Для переменных окружения
bot: Bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

# --------------------------------------------- Инициализация диспетчера событий
# Принимает все события и отвечает за порядок их обработки в асинхронном режиме.
dp = Dispatcher()

# Назначаем роутеры:
# dp.include_routers(general_router, admin_router, oait_manager_router, oait_router, retail_router) #

#  Распределение роутеров - порядок записи имеет значение. не трогать!
dp.include_router(user_router)








# ---------------------------------------------------- Зацикливание работы бота
# Отслеживание событий на сервере тг бота:
async def run_bot():
    # ---------------------
    async def on_startup(bot):
        # Удаление Webhook и всех ожидающих обновлений
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook удален и ожидающие обновления сброшены.")


    async def on_shutdown(bot):

        ...

    # ---------------------
    dp.startup.register(on_startup)  # действия при старте бота +
    dp.shutdown.register(on_shutdown)  # действия при остановке бота +

    # -------------------------------------------------------------------------------
    # Установка промежуточного слоя (сразу для диспетчера, не для роутеров):
    # dp.update.middleware(DataBaseSession(session_pool=session_pool_LOCAL_DB))

    await bot.delete_webhook(drop_pending_updates=True)  # Сброс отправленных сообщений, за время, что бот был офлайн.
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # если надо удалить  команды из меню.


    # await bot.set_my_commands(commands=default_menu, scope=types.BotCommandScopeDefault())  # Список команд в меню.
    # BotCommandScopeAllPrivateChats - для приват чартов  # todo здесь переделать разобраться!
    # BotCommandScopeDefault - для всех чартов

    await dp.start_polling(bot, skip_updates=True, polling_timeout = 1, close_bot_session = True,
                           allowed_updates=['message', 'edited_message', 'callback_query'])
    # , interval=1, polling_timeout = 10 - Задержка в получении обновлений:
    #  allowed_updates=ALLOWED_UPDATES, - передаем туда список разрешенных
    #  событий для бота с сервера
    # , interval=2 интервал запросов на обновление.



# Запуск асинхронной функции run_bot:
if __name__ == "__main__":
    asyncio.run(run_bot())