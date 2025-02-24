import json
import os

from dotenv import find_dotenv, load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv(find_dotenv())
giga_key = os.environ["giga_key"]

giga = GigaChat(
    credentials=giga_key,
    verify_ssl_certs=False,
    verbose=True,
)

# Создание функции get_current_weather


def get_weather(location):
    weather_info = {"location": location, "temperature": "-12"}
    return json.dumps(weather_info)


# Создание списка сообщений, списка функций и параметров вызова модели

messages = [Messages(role=MessagesRole.USER, content="Какая погода сейчас в Москве?")]

functions = [
    {
        "name": "get_weather",
        "description": "Узнай текущую погоду в заданной локации",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Местоположение, например, название города",
                },
            },
            "required": ["location"],
        },
        "few_shot_examples": [
            {
                "request": "Какая погода в Москве сейчас",
                "params": {
                    "location": "Москва",
                },
            }
        ],
        "return_parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Местоположение, например, название города",
                },
                "temperature": {
                    "type": "int",
                    "description": "Температура для заданного местоположения",
                },
            },
        },
    }
]

payload = Chat(
    messages=messages,
    functions=functions,
    function_call="auto",
    temperature=0.7,
    max_tokens=1000,
)

# Обращение к модели

response = giga.chat(payload)
payload.messages.append(response.choices[0].message)

print(response.choices[0].message.content)

# Извлекаем аргументы
python_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

# Вызываем функцию
report = get_weather(python_args)

# Записываем результат выполнения функции в промты
payload.messages.append(
    {
        "role": "tool",
        "tool_call_id": tool.id,
        "name": "get_current_weather",
        "content": report,
    }
)

payload.messages.append(
    Messages(
        role=MessagesRole.FUNCTION,
        content="Расскажи про Ницше",
    )
)


# Получаем ответ модели с учетом результата выполнения функции
response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

# Печатаем сообщение из ответа модели
print(response2.choices[0].message.content)
