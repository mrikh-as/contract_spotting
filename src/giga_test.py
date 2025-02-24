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
payload = Chat(
    messages=[
        Messages(
            role=MessagesRole.USER,
            content="КТо такой Лавкрафт?",
        )
    ],
    temperature=0.7,
    max_tokens=1000,
)
response = giga.chat(payload)
# print(response.choices[0].message.content)
payload.messages.append(response.choices[0].message)

payload.messages.append(
    Messages(
        role=MessagesRole.USER,
        content="Расскажи про Ницше",
    )
)
response = giga.chat(payload)
# print(response.choices[0].message.content)
payload.messages.append(response.choices[0].message)
payload.messages.append(
    Messages(
        role=MessagesRole.USER,
        content="что общего между моим первым и вторым вопросом?",
    )
)
response = giga.chat(payload)
# print(response.choices[0].message.content)
payload.messages.append(response.choices[0].message)
payload.messages.append(
    Messages(
        role=MessagesRole.USER,
        content="о чем был мой второй вопрос?",
    )
)
response = giga.chat(payload)
print(response.choices[0].message.content)
payload.messages.append(response.choices[0].message)
