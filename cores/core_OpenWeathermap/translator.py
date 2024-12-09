
from googletrans import Translator




# Определить язык пользователя по координатам по вводу.
async def translate_from_language(input_text: str, input_dest: str):

    """

    :param input_dest:'ru'
    :return:
    """

    translator = Translator()

    result = translator.translate(text=input_text, dest=input_dest).text

    return result