import json
import logging
import os

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


class ContractAssessment:
    def __init__(self):
        self.input = user_input
        self.response = None

    def evaluation(self):
        logger.info("Проверяю, является ли текст, введенный пользователем,договором")
        logger.debug(f"Текст: {self.input}")
        self.response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """Пользователь ввел текст. Оцени,
                        с какой вероятностью введенный пользователем текст
                        является договором, по шкале от 0 до 100 процентов.
                        Ответ дай в формате json. Пример ответа:
                            {
                                "Probability": "80"
                            }
                            """,
                },
                {"role": "user", "content": self.input},
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(self.response.choices[0].message.content)
        logger.info(f"Проверка завершена. Вероятность: {result['Probability']}")
        return result

    def contract_spotting(self):
        return result

    def rule_recall(self):
        return result

    def rule_application(self):
        return result

    def process_all(self):
        self.evaluation()
        self.contract_spotting()
        self.rule_recall()
        self.rule_application()
        return result


user_input = """1.1. Исполнитель обязуется собственными либо привлеченными
силами оказать услуги в соответствии с условиями настоящего Договора,
Заявками Заказчика, а также приложениями к настоящему Договору, а Заказчик
обязуется создать Исполнителю необходимые условия для оказания услуг и
оплатить обусловленную Договором цену. 
            """
example = ContractAssessment()
example.process_all()
