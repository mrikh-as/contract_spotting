import json
import os
import openai

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
api_key = os.environ["api_key"]

# Вызов модели

from openai import OpenAI

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

user_input = """3.1. Стоимость услуг, оказанных Исполнителем по настоящему
                Договору, указывается в Приложении «О стоимости оказанных услуг»
                к настоящему договору.
                3.2. Стоимость услуг, указанная в Приложении к Договору,
                является фиксированной для Заказчика и не подлежит изменению в ходе
                выполнения сторонами его условий, за исключением случая,
                предусмотренного п.3.3. настоящего Договора.
             """

# Создание списка промтов

messages = [
    {
        "role": "system",
        "content": """Извлеки из текста названия всех сторон договора, упоминаемых в тексте (например, Продавец, Покупатель,
                      Арендатор, Арендодатель, Сторона, Стороны и т.п.)
                      и изложи ответ в формате json
                      """,
    },
    {"role": "user", "content": user_input},
]


# Функция ответа модели
def extraction(user_input: str):
    """Вызов модели"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)
    return result


report = extraction(user_input)
print(report)
