# Название проекта - AI-агент, анализирующий гражданские договоры на соответствие императивным нормам ГК РФ

Задача проекта - проанализировать договор пользователя на соотвествие императивным нормам ГК РФ. Контекст: Согласно ГК РФ условия договора свободно определяются сторонами, за исключением ситуаций, когда закон предписывает содержание тех или иных условий императивно.

# Архитектура проекта
Проект строится на архитектуре агентской системы типа workflow: routing, предложенной компанией Anthropic в исследовании "Building effective agents" от 24/12/2024:
https://www.anthropic.com/research/building-effective-agents

# Ограничения:
- небесспорные исходные положения: в основе проекта лежит гипотеза, согласно которой юридические последствия влечет не весь текст договора, а только та часть текста договора, которая касается установления, изменения или прекращения прав и обязанностей (согласно ГК РФ догоор - это соглашение об установлении/изменении/прекращении прав и обязанностей);
- договор не оценивается целиком: текст договора подается на вход не целиком, а разбитый на фрагменты заданной размерности (чанкование), что не позволяет оценивать договор в целом;
- цели анализа могут не являться исчерпывающими: среди юристов не существует единого подхода к тому, что входит в исчерпывающий анализ договора на риски. В данном проекте проверяется только соответствие условий договора нормам гражданского законодательства;
- расход токенов: проект не ставил целью оптимизировать код в целях экономии токенов;
- для создания коммерческого приложения на базе проекта потребуется rag-СПС или API СПС (гарант или консультант+).

# Методологические замечания
Важно понимать различие между синтаксисом и семантикой текста договора. Установление, изменение и прекращение прав и обязанностей - это семантические категории.
Задача состоит в том, чтобы определить, какие синтаксичекие паттерны релевантны указанным семантическим категориям.

Гипотеза о связи синтаксиса и семантики:
- установление должно сопровождаться либо прямым указанием на действия, совершаемые сторонами (констатация обзанности), либо на обязанность/право совершить или не совершать те или иные действия;
- изменение - аналогичным образом;
- прекращение - формулировками "не имеет права, не несет отвественности, освобождается от ответственности (потому что ответственность - дополнительная обязанность, возникающая при неисполнении начальной обязанности)".

## Структура проекта

```
├── README.md          <- Общая информация о проекте
│
├── data
│   ├── processed      <- Обработанная информация
│   └── raw            <- Необработанная информация на входе
│
├── requirements.txt   <- Необходимые зависимости проета (библиотеки)`
│
└── src                <- Инструменты, позволяющие создать AI-агента
│   ├── __init__.py      <- Файл, делающий содержимое папки модулем пайтон
│   ├── function_call.py <- Как вызвать функцию с помощью ллм
│   ├── json_output.py   <- Как сделать, чтобы ллм отdечала в формате json
│   └── llm_call.py      <- Обращение к ллм по API
├── main.py            <- Основной код проекта
```