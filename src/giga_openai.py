import json
import os
import uuid
import httpx

import requests
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
giga_key = os.environ["giga_key"]

# Получаем авторизационный токен

rq_uid = str(uuid.uuid4())
url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
payload = {"scope": "GIGACHAT_API_PERS"}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "RqUID": rq_uid,
    "Authorization": f"Basic {giga_key}",
}
response = requests.request("POST", url, headers=headers, data=payload, verify=False)
pair = json.loads(response.text)
access_token = pair["access_token"]

# Создаем экземпляр OpenAI

client = OpenAI(
    api_key=access_token,
    base_url="https://gigachat.devices.sberbank.ru/api/v1",
    http_client=httpx.Client(verify=False),
)

# Создание функции get_current_weather


def get_current_weather(location):
    weather_info = {"location": location, "temperature": "72"}
    return json.dumps(weather_info)


# Создание списка функций, доступных для function call

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

# Создание списка промтов

messages = [
    {"role": "user", "content": "What's the weather like in Boston!"},
]

# Обращение к модели и запись ответа в переменную response
response = client.chat.completions.create(
    model="GigaChat",
    messages=messages,
    tools=tools,
    tool_choice="required",
)

# Записываем сообщение из ответа в переменную
full_message = response.choices[0].message

print(full_message)
