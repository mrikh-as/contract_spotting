# Название проекта - contract_spotting (извлечение прав и обязанностей из текста договора)

## Контекст проекта

Договор, по смыслу российского законодательства, является соглашением об установлении, изменении или прекращении прав и обязанностей (далее - пио).

Это определение очерчивает юридически релевантные семантические элементы текста договора. Иными словами, слова, фразы и предложения в тексте договора могут иметь четыре юридических роли - установление пио, изменение пио, прекращение пио, юридически нерелевантное.

Таким образом, юридический анализ договора начинается с задачи по определению семантических ролей слов, фраз и предложений из текста договора.

Уровень чанкования текста для данной задачи - простые предложения (отдельно стоящие или в составе сложных предложений).

Отдельное внимание следует уделить придаточным предложениям (в превую очередь - придаточным предложениям условия).

Оптимально использование синтаксического анализа (дерево зависимостей, глагольные группы).

Деревья предпочтительны по отношению к графам.

Вопрос: какими словами-триггерами в тексте сопровождается установление/изменение/прекращение пио? Нужна ли тонкая настройка (берт, датасет с примерами), или задача решаема с помощью других методов обработки естественного языка?

Установление пио должно сопровождаться либо прямым указанием на действия, совершаемые сторонами, либо на обязанность/право совершить или не совершать такие действия. Изменение пио - аналогичным образом. Прекращение пио - не имеет права, не несет отвественности, освобождается от ответственности (потому что ответственность - дополнительная обязанность, возникающая при неисполнении начальной обязанности).


## Структура проекта

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    │    
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations 
    │
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── __init__.py 
```

--------