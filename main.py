import json
import logging
import os
from src.utils import BasicSetup


user_input = """1.1. Исполнитель обязуется собственными либо привлеченными
силами оказать услуги в соответствии с условиями настоящего Договора,
Заявками Заказчика, а также приложениями к настоящему Договору, а Заказчик
обязуется создать Исполнителю необходимые условия для оказания услуг и
оплатить обусловленную Договором цену. 
            """


class IfContract(BasicSetup):
    def __init__(self):
        self.input = user_input
        self.response = None

    def start(self):
        super().setup

    def evaluation(self):
        # super().logger.info(
        #    "Проверяю, является ли текст, введенный пользователем,договором"
        # )
        # super().logger.debug(f"Текст: {self.input}")
        self.response = super().client.chat.completions.create(
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
        # super().logger.info(f"Проверка завершена. Вероятность: {result['Probability']}")
        return result

    def run(self):
        result = self.evaluation()
        return result


example = IfContract()
example.run()
