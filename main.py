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
        self.messages = []
        self.data = None
        self.rights = None
        self.rules = None
        self.risks = None
        self.full_report = None

    def evaluate(self):
        logger.info("Проверяю, является ли текст, введенный пользователем,договором.")
        with open(
            Path(__file__).parent / "data" / "raw" / "1.txt", mode="r", encoding="utf-8"
        ) as file:
            self.data = file.read()
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - junior-юрист. Оцени по шкале от 0 до 100 процентов, с какой вероятностью
                    введенный пользователем текст является договором.
                    Ответ дай в формате json. Пример ответа:
                    {
                                "Probability": "80"
                    }
                    """,
            }
        )
        self.messages.append({"role": "user", "content": self.data})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        full_message = response.choices[0].message
        self.messages.append(full_message)
        result = json.loads(response.choices[0].message.content)
        probability = int(result["Probability"])
        logger.info(f"Проверка завершена. Вероятность: {probability}")
        if probability < 80:
            return None
        else:
            logger.info("Перехожу к следующему этапу проверки договора.")
            return result

    def extract(self):
        logger.info("Извлекаю из договора права и обязанности.")
        with open(
            Path(__file__).parent / "data" / "raw" / "1.txt", mode="r", encoding="utf-8"
        ) as file:
            self.data = file.read()
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - специалист в области обработки естественного языка (nlp).
                Ты хорошо умеешь проводить синтаксический анализ предложений и строить деревья зависимостей слов в предложении.
                Ранее юрист идентифицировал введенный пользователем текст в качестве фрагмента договора. 
                Используя тот же текст, извлеки из него все без исключения самостоятельные глаголы и 
                реконструируй каждый из этих самостоятельных глаголов до полного простого предложения,
                процитировав в простом предложении все зависимые от этого глагола члены предложения.
                Ответ дай в формате json.
                Пример текста, введенного пользователем:
                1.1. По договору возмездного оказания услуг Исполнитель обязуется 
                по заданию Заказчика оказать услуги, указанные в п.1.2. настоящего договора,
                а Заказчик обязуется оплатить эти услуги и принять результат этих услуг.
                Пример твоего ответа:
                    {
                    "Исполнитель": "1.1. По договору возмездного оказания услуг Исполнитель обязуется 
                по заданию Заказчика оказать услуги, указанные в п.1.2. настоящего договора",
                    "Заказчик": "1.1. Заказчик обязуется оплатить эти услуги.",
                    "Заказчик": "1.1. Заказчик обязуется принять результат этих услуг"
                }
                """,
            }
        )
        self.messages.append({"role": "user", "content": self.data})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        logger.info("Права и обязанности извлечены.")
        full_message = response.choices[0].message
        self.messages.append(full_message)
        with open("rights.txt", "w", encoding="utf-8") as file:
            file.write(full_message.content)
        logger.info("Права и обязанности сохранены в файле rights.txt.")
        self.rights = json.loads(response.choices[0].message.content)
        return self.rights

    def recall(self):
        logger.info("Подбираю нормы права для извлеченных прав и обязанностей.")
        with open(
            Path(__file__).parent / "rights.txt",
            mode="r",
            encoding="utf-8",
        ) as file:
            self.rights = file.read()
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - middle-юрист.Ты хорошо умеешь подбирать нормы права, применимые
                к условиям договоров.
                Ты хорошо знаешь, что в силу ГК РФ условия договора определяются по усмотрению сторон,
                кроме случаев, когда содержание соответствующего условия предписано законом. В последнем
                случае договор должен соответствовать обязательным для сторон правилам, установленным законом
                (императивным нормам).
                Тебе дается в пользовательском промте набор предложений из договора в формате json, которые специалист в области обработки естественного языка (nlp) для твоего удобства
                извлек из фрагмента договора, и каждое из которых является
                правом или обязанностью одной или нескольких сторон по договору.
                Тебе нужно проверить, предписано ли законом РФ (в частности - ГК РФ) содержание того или иного права или обязанности
                из фрагмента договора. Если предписано - нужно указать релевантное положение закона. Если нет - не выдумывай и прямо скажи,
                что релевантное положение закона отсутствует.
                Ответ дай в формате json.
                Пример полученных тобой прав и обязанностей:
                    {
                    "Перевозчик": "2.3. Перевозчик в случае утраты груза возмещает ущерб и провозную плату.",
                    "Продавец": "1.3. Продавец освобождается от ответственности за истребование товара у покупателя третьими лицами.",
                    "Подрядчик": "3.1. Подрядчик обязан выполнить работу лично, без привлечения третьих лиц.",
                    "Займодавец": "5.3. Замодавец имеет право на проценты за пользование займом.",
                    "Арендодатель": "4.1. Арендодатель вправе осуществлять проверки чистоты арендованного помещения.",
                    "Исполнитель": "Исполнитель обеспечивает наличие свободных вагонов на Казанском вокзале каждый понедельник"
                    }
                Пример твоего ответа:
                    {
                    "Перевозчик": ["2.3. Перевозчик в случае утраты груза возмещает ущерб и провозную плату.", "Пункт 3 статьи 796 ГК РФ"],
                    "Продавец": ["1.3. Продавец освобождается от ответственности за истребование товара у покупателя третьими лицами.", "Пункт 2 статьи 461 ГК РФ"],
                    "Подрядчик": ["3.1. Подрядчик обязан выполнить работу лично, без привлечения третьих лиц.", "Пункт 1 статьи 706 ГК РФ"],
                    "Займодавец": ["5.3. Замодавец имеет право на проценты за пользование займом.", "Пункт 1 статьи 809 ГК РФ"]
                    "Арендодатель": ["4.1. Арендодатель вправе осуществлять проверки чистоты арендованного помещения.", "Не найдено положение закона"],
                    "Исполнитель": ["Исполнитель обеспечивает наличие свободных вагонов на Казанском вокзале каждый понедельник", "Не найдено положение закона"]
                }
                """,
            }
        )
        self.messages.append({"role": "user", "content": self.rights})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        logger.info("Нормы права подобраны.")
        full_message = response.choices[0].message
        self.messages.append(full_message)
        with open("rules.txt", "w", encoding="utf-8") as file:
            file.write(full_message.content)
        logger.info("Нормы права сохранены в файле rules.txt.")
        self.rules = json.loads(response.choices[0].message.content)
        return self.rules

    def conclude(self):
        logger.info(
            "Проверяю извлеченные права и обязанности на предмет соовтетствия закону, оцениваю риски."
        )
        with open(
            Path(__file__).parent / "rules.txt",
            mode="r",
            encoding="utf-8",
        ) as file:
            self.rules = file.read()
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - senior-юрист.
                Ты хорошо умеешь сравнивать положение договора с релевантным положением закона и делать вывод по результатам такого сопоставления.
                Ты хорошо понимаешь, что диспозитивные положения закона допускают установление иного в договоре, но противоречие императивной норме
                влечет риск недействительности соответствующего положения договора.
                Ранее middle-юрист подобрал для тебя релевантные положения закона к набору прав и обязанностей из фрагмента договора.
                Тебе нужно сравнить права и обязанности с релевантными положениям закона и сделать выводы о наличии или отсутствии риска.
                Ответ дай в формате json.
                Пример полученных тобой прав и обязанностей:
                {
                    "Перевозчик": ["2.3. Перевозчик в случае утраты груза возмещает ущерб и провозную плату.", "Пункт 3 статьи 796 ГК РФ"],
                    "Продавец": ["1.3. Продавец освобождается от ответственности за истребование товара у покупателя третьими лицами.", "Пункт 2 статьи 461 ГК РФ"],
                    "Подрядчик": ["3.1. Подрядчик обязан выполнить работу лично, без привлечения третьих лиц.", "Пункт 1 статьи 706 ГК РФ"],
                    "Займодавец": ["5.3. Замодавец имеет право на проценты за пользование займом.", "Пункт 1 статьи 809 ГК РФ"]
                    "Арендодатель": ["4.1. Арендодатель вправе осуществлять проверки чистоты арендованного помещения.", "Не найдено положение закона"],
                    "Исполнитель": ["Исполнитель обеспечивает наличие свободных вагонов на Казанском вокзале каждый понедельник", "Не найдено положение закона"]
                }
                Пример твоего ответа:
                {
                    "Перевозчик": ["2.3. Перевозчик в случае утраты груза возмещает ущерб и провозную плату.", "Пункт 3 статьи 796 ГК РФ", "Риск отсутствует. Норма права
                    императивна, поскольку не позволяет установить иное в договоре, но договор не противоречит этой императивной норме."],
                    "Продавец": ["1.3. Продавец освобождается от ответственности за истребование товара у покупателя третьими лицами.", "Пункт 2 статьи 461 ГК РФ",
                    "Риск присутствует. Норма права императивна, поскольку соглашение об ином ничтожно, и иное предусмотрено договором."],
                    "Подрядчик": ["3.1. Подрядчик обязан выполнить работу лично, без привлечения третьих лиц.", "Пункт 1 статьи 706 ГК РФ", "Риск отсутствует.
                    Норма права диспозитивна, договор устанавливает иное, что допустимо."],
                    "Займодавец": ["5.3. Замодавец имеет право на проценты за пользование займом.", "Пункт 1 статьи 809 ГК РФ", "Риск отсутствует.
                    Норма права диспозитивна, договор не устанавливает иное."]
                    "Арендодатель": ["4.1. Арендодатель вправе осуществлять проверки чистоты арендованного помещения.", "Не найдено положение закона"],
                    "Исполнитель": ["Исполнитель обеспечивает наличие свободных вагонов на Казанском вокзале каждый понедельник", "Не найдено положение закона"]
                }
                """,
            }
        )
        self.messages.append({"role": "user", "content": self.rules})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            response_format={"type": "json_object"},
        )
        logger.info("Риски оценены.")
        full_message = response.choices[0].message
        self.messages.append(full_message)
        with open("risks.txt", "w", encoding="utf-8") as file:
            file.write(full_message.content)
        logger.info("Риски сохранены в файле risks.txt.")
        self.risks = json.loads(response.choices[0].message.content)
        return self.risks

    def report(self):
        logger.info("Генерирую итоговое заключение.")
        with open(
            Path(__file__).parent / "risks.txt",
            mode="r",
            encoding="utf-8",
        ) as file:
            self.risks = file.read()
        self.messages.append(
            {
                "role": "system",
                "content": """Ты - партнер юридической фирмы. Твоя задача - на основании информации о рисках, полученной от senior-юриста,
                кратко и исчерпывающе рассказать клиенту о всей проделанной работе, рисках и рекомендациях.
                Ответ дай в форме заключения юридической фирмы на естественном языке, излагающее суть проделанной работы,
                имеющиеся риски и рекомендации.
                """,
            }
        )
        self.messages.append({"role": "user", "content": self.risks})
        response = client.chat.completions.create(
            model="deepseek-chat", messages=self.messages
        )
        logger.info("Заключение готово.")
        full_message = response.choices[0].message
        self.messages.append(full_message)
        with open("report.txt", "w", encoding="utf-8") as file:
            file.write(full_message.content)
        logger.info("Доклад сохранен в файле report.txt.")
        self.full_reportreport = json.loads(response.choices[0].message.content)
        return self.full_reportreport

    def process(self):
        result = self.evaluate()
        if result:
            self.extract()
            self.recall()
            self.conclude()
            self.report()
        else:
            print("Проверка остановлена. Загрузите текст договора.")


assessment = ContractAssessment()

assessment.process()
