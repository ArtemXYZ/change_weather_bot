"""
Генератор кнопок (клавиатуры или инлайн кнопок) в телеграм боте
"""


from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder




def get_keyboard(
    *btns: str,  # список названий кнопок
    placeholder: str = None,  # надпись в поле для ввода
    request_contact: int = None,  # запросить контакт
    request_location: int = None,  # запросить локацию
    sizes: tuple[int] = (2,), # размер кнопки
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона"
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )

    !!!! нужно передать корректный кортеж. Например, (2,) для кортежа с одним элементом
     или (2, 1) для кортежа с двумя элементами.
    '''

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)




# Функция для генерации инлайн кнопок;
def get_callback_btns(
    *, # - запрет на передачу не именнованных аргументов
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()