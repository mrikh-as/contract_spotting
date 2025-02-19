import json
import os
import openai

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
api_key = os.environ["api_key"]

# Вызов модели

from openai import OpenAI

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

messages = [
    {"role": "user", "content": "What's the weather like in Boston!"},
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

print(response.choices[0].message.content)
