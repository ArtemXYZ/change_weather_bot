
import os
from dotenv import find_dotenv, load_dotenv  # Для переменных окружения
load_dotenv(find_dotenv())  # Загружаем переменную окружения
# ----------------------------------------------------------------------------------------------------------------------

API_TOKEN = os.environ.get("API_TOKEN")
API_WEATHER = os.environ.get("API_WEATHER")