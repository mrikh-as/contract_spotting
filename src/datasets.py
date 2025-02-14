import os
from pathlib import Path

import spacy
from spacy import displacy

# Путь к файлу
file_path = Path(__file__).parent.parent / "data" / "raw" / "1.txt"

# Чтение содержимого файла
with open(file_path, mode="r", encoding="utf-8") as file:
    text = file.read()

# Загружаем модель Spacy для обработки русского языка
nlp = spacy.load("ru_core_news_sm")

doc = nlp(text)

displacy.render(doc, style="dep", jupyter=True)

# Лемматизация с сохранением структуры текста
formatted_text = "".join(token.lemma_ + token.whitespace_ for token in doc).strip()

# Вывод результата
print("Лемматизированный текст:", formatted_text)

entities = []

for ent in doc.ents:
    entities.append((ent.text, ent.label_))

entities


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

    print(entities)  # , relations


extract_entities_and_relations(text)
