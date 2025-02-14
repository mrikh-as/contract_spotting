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


class ContractAssessment:
    def __init__(self):
        self.input = None
        self.messages = []
        self.rights = None
        self.report = None

    def read(self):
        with open(file_path, mode="r", encoding="utf-8") as file:
            self.input = file.read()

    def evaluation(self):
        logger.info("Проверяю, является ли текст, введенный пользователем,договором")
        logger.debug(f"Текст: {self.input}")
        self.messages.append(
            [
                {
                    "role": "system",
                    "content": """Ты - юрист. Оцени по шкале от 0 до 100 процентов, с какой вероятностью
                    введенный пользователем текст является договором.
                    Ответ дай в формате json. Пример ответа:
                    {
                                "Probability": "80"
                    }
                                """,
                },
                {"role": "user", "content": self.input},
            ],
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        full_message = response.choices[0].message
        self.messages.append(full_message)
        result = json.loads(response.choices[0].message.content)
        logger.info(f"Проверка завершена. Вероятность: {result['Probability']}")
        if result["Probability"] < 80:
            return None
        else:
            logger.info("Перехожу к следующему этапу проверки договора.")
            return result

    def contract_spotting(self):
        logger.info("Извлекаю из договора права и обязанности.")
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - специалист в области обработки естественного языка (nlp).
                Ты хорошо умеешь проводить синтаксический анализ предложений и строить деревья зависимостей слов в предложении.
                Ранее юрист идентифицировал введенный пользователем текст в качестве фрагмента договора. 
                Используя тот же текст, извлеки из него все без исключения самостоятельные глаголы и 
                реконструируй каждый из этих самостоятельных глаголов до полного простого предложения,
                процитировав в простом предложении все зависимые от этого глагола члены предложения.
                Список получившихся предложений оформи в формате json.
                Пример текста, введенного пользователем: 1.1. По договору возмездного оказания услуг Исполнитель обязуется 
                по заданию Заказчика оказать услуги, указанные в п.1.2. настоящего договора,
                а Заказчик обязуется оплатить эти услуги и принять результат этих услуг.
                Пример ответа:
                            {
                                "Исполнитель": "1.1. По договору возмездного оказания услуг Исполнитель обязуется 
                по заданию Заказчика оказать услуги, указанные в п.1.2. настоящего договора",
                                "Заказчик": "1.1. Заказчик обязуется оплатить эти услуги.",
                                "Заказчик": "1.1. Заказчик обязуется принять результат этих услуг
                            }
                            """,
            }
            # "role": "user",
            # "content": "хмм"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        full_message = response.choices[0].message
        self.messages.append(full_message)
        self.rights = json.loads(response.choices[0].message.content)
        logger.info(f"Права и обязанности извлечены:\n{self.rights}")
        return self.rights

    def rule_recall(self):
        return result

    def rule_application(self):
        return result

    def report(self):
        logger.info("Генерирую итоговый доклад.")
        self.messages.append(
            [
                {
                    "role": "system",
                    "content": """Ты - юрист. Оцени по шкале от 0 до 100 процентов, с какой вероятностью
                    введенный пользователем текст является договором.
                    Ответ дай в формате json. Пример ответа:
                    {
                                "Probability": "80"
                    }
                                """,
                },
                {"role": "user", "content": self.input},
            ],
        )
        self.report = "Здесь будет итоговый результат проверки."
        return result

    def process_all(self):
        result = self.evaluation()
        if result:
            self.contract_spotting()
            # self.rule_recall()
            # self.rule_application()
            self.report()
            print(f"{self.report}")
        else:
            print("Проверка остановлена. Загрузите текст договора.")

        #
        return result


file_path = Path(__file__).parent.parent / "data" / "raw" / "1.txt"

example = ContractAssessment()
example.process_all()
