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
        self.analysis = None
        self.report = None

    def read(self):
        file_path = Path(__file__).parent / "data" / "raw" / "1.txt"
        with open(file_path, mode="r", encoding="utf-8") as file:
            self.input = file.read()

    def evaluation(self):
        logger.info("Проверяю, является ли текст, введенный пользователем,договором")
        # logger.debug(f"Текст: {self.input}")
        self.messages.append(
            [
                {
                    "role": "system",
                    "content": """Ты - junior-юрист. Оцени по шкале от 0 до 100 процентов, с какой вероятностью
                    введенный пользователем текст является договором.
                    Ответ дай в формате json. Пример ответа:
                    {
                                "Probability": "80"
                    }
                                """,
                },
                {"role": "user", "content": self.input},
            ]
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        # full_message = response.choices[0].message
        # self.messages.append(full_message)
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

    # def rule_recall(self):
    #    return result

    def rule_application(self):
        logger.info(
            "Проверяю извлеченные права и обязанности на предмет соовтетствия закону, формирую рекомендации."
        )
        self.messages.append(
            {
                "role": "system",
                "content": f"""Ты - middle-юрист.
                Ты хорошо умеешь находить релевантную норму ГК РФ к положению договора, сравнивать положение договора с релевантной нормой права 
                и делать вывод по результатам такого сопоставления.
                Ранее специалист в области обработки естественного языка извлек для тебя список простых предложений из текста договора:{self.rights} 
                Эти предложения являются правами и обязанностями сторон договора. Найди под каждое предложение релевантную норму права и сделай вывод,
                не противоречит ли право или обязанность из договора релевантной норме права. Если противоречие есть - дай рекомендацию.
                Если релевантная норма ГК РФ отсутствует - не выдумывай, прямо скажи об этом.
                Ответ дай на естественном языке.
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
        return self.analysis

    def report(self):
        logger.info("Генерирую итоговый доклад.")
        self.messages.append(
            # [
            {
                "role": "system",
                "content": f"""Ты - senior-юрист, руководитель команды. Твоя задача - кратко рассказать клиенту о проделанной работе
                    и дать клиенту рекомендации, основанные на выводах middle-юриста: {self.analysis}
                    Ответ дай в форме заключения юридической службы на естественном языке, излагающее суть проделанной работы и список рекомендаций.
                    """,
            },
            # {"role": "user", "content": self.input},
            # ],
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
        )
        self.report = json.loads(response.choices[0].message.content)
        logger.info("Заключение подготовлено.")
        print(f"self.report")

    def process_all(self):
        result = self.evaluation()
        if result:
            self.contract_spotting()
            # self.rule_recall()
            self.rule_application()
            self.report()
        else:
            print("Проверка остановлена. Загрузите текст договора.")

        #
        return result


file_path = Path(__file__).parent.parent / "data" / "raw" / "1.txt"

example = ContractAssessment()

example.read()
print(example.input)
type(example.input)
example.evaluation()
