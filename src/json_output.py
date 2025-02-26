import json
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
api_key = os.environ["api_key"]

from openai import OpenAI

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

user_input = "Далеко-далеко ускакала в поле молодая лошадь."

# Создание списка промтов

messages = [
    {
        "role": "system",
        "content": """Ты - специалист по nlp и хорошо умеешь структурировать текст на естественном языке.
                Извлеки из текста пользователя субъекты и предикаты.
                Ответ дай в формате json.
                Пример текста пользователя:
                    Мама мыла Раму.
                Пример твоего ответа:
                    {
                    "Субъект": "Мама",
                    "Предикат": "Мыла"
                    }
                """,
    },
    {"role": "user", "content": user_input},
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={"type": "json_object"},  # здесь зарыта собака
)

result_dictionary = json.loads(response.choices[0].message.content)
result_json = response.choices[0].message.content
print(result_json)
