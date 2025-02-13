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

import spacy
from spacy import displacy
import networkx as nx
import matplotlib.pyplot as plt

# Загружаем модель Spacy для обработки русского языка
nlp = spacy.load("ru_core_news_sm")


# Функция для извлечения сущностей и отношений
def extract_entities_and_relations(text):
    doc = nlp(text)

    # Извлекаем сущности
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # Извлекаем отношения
    relations = []
    for token in doc:
        if token.dep_ == "ROOT":
            subject = [w for w in token.lefts if w.dep_ == "nsubj"]
            object = [w for w in token.rights if w.dep_ == "dobj"]
            if len(subject) > 0 and len(object) > 0:
                relations.append((subject[0].text, token.text, object[0].text))

    return entities, relations


# Пример текста
text = """
Илон Маск основал компанию Tesla в 2003 году. 
Tesla производит электромобили и солнечные батареи.
"""

entities, relations = extract_entities_and_relations(text)

# Создаем граф
G = nx.MultiDiGraph()

for entity in entities:
    G.add_node(entity[0], label=entity[1])

for relation in relations:
    G.add_edge(relation[0], relation[2], label=relation[1])

# Визуализируем граф
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=700)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, font_size=14, font_family="sans-serif")
edge_labels = {(e[0], e[1]): e[2]["label"] for e in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
plt.show()
