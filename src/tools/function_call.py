import json
import os
import openai

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
api_key = os.environ["api_key"]

# Вызов модели

from openai import OpenAI

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

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
    model="deepseek-chat",
    messages=messages,
    tools=tools,
)

# Записываем сообщение из ответа в переменную
full_message = response.choices[0].message

# Добавляем сообщение ответа модели в промты
messages.append(full_message)

# Записываем номер обращения к инструменту из ответа в переменную
tool = full_message.tool_calls[0]

# Записываем аргументы функции из ответа в переменную
json_args = tool.function.arguments

# Переводим аргументы из ответа в словарь пайтон

python_args = json.loads(json_args)

# Вызываем функцию и записываем ответ в переменную
report = get_current_weather(python_args)

# Записываем результат выполнения функции в промты
messages.append(
    {
        "role": "tool",
        "tool_call_id": tool.id,
        "name": "get_current_weather",
        "content": report,
    }
)

# Получаем ответ модели с учетом результата выполнения функции
response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

# Печатаем сообщение из ответа модели
print(response2.choices[0].message.content)
