import json
import logging
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
api = os.environ["api_key"]

client = OpenAI(api_key=api, base_url="https://api.deepseek.com")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

messages = [
    {
        "role": "system",
        "content": """Ты - смышленный парень. Тебе нужно проверить, сколько участников в описанной ситуации.
        Ответ дай в формате json.
        Пример информации на входе:
        Двое из ларца одинаковых с лица.
        Пример твоего ответа:
                    {
                    "Первый из ларца": "Первый из одинаковых с лица",
                    "Второй из ларца": "Второй из одинаковых с лица",
                    }
                """,
    },
    {"role": "user", "content": "а и б сидели на трубе"},
]
logger.info("Начинаю")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={"type": "json_object"},
)

logger.info("Закончил")
result = json.loads(response.choices[0].message.content)
print(result)
