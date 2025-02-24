# Название проекта
Проект называется 'contract-spotting'. Это название унаследовано от названия таска для llm, в котором от модели требуется извлечь из договора права и обязанности.

# Цель проекта
Цель состоит в том, чтобы попробовать решить юридическую задачу анализа договора на соответствие императивным нормам с помощью агентской системы.

Что такое императивные нормы: согласно ГК РФ условия договора свободно определяются сторонами, за исключением ситуаций, когда закон предписывает содержание тех или иных условий императивно (императивные нормы). Противоречие императивным нормам создает правовой риск недействительности договора в соответствующей части.

Зачем пробовать для этого агентскую систему:
- агентские системы широко обсуждаются;
- для проверки гипотезы о том, что агентская система позволит обойтись без составления трудоемких датасетов для fine-tuning;
- для проверки гипотезы о том, что агентская система инклюзивна для экспертов (меньше хардкодинга = больше экспертной самостоятельности).

# Workflow проекта
Проект построен по примеру агентской системы типа Workflow: Prompt chaining, предложенному компанией Anthropic в исследовании "Building effective agents" от 24/12/2024:
https://www.anthropic.com/research/building-effective-agents

Шаги:
0. На вход подается фрагмент договора (чанкуем договор, исходя из максимально допустимого моделью числа токенов) - файл 1.txt в data/raw.
1. Агент 1 (классификатор, роль - junior-юрист) оценивает, с какой вероятностью фрагмент является фрагментом договора. При вероятности ниже 80 процентов предлагается заменить информацию на входе на фрагмент договора. Реализация гейта служит гардрейлом (guardrail) для остановки анализа на случай подачи нерелевантной информации в целях экономии токенов.
2. При прохождении гейта агент 2 (экстрактивный суммаризатор, роль - специалист в области nlp) извлекает из договора простые предложения, каждое из которых является правом или обязанностью сторон. Результат работы агента - файл rights.txt в data/processed.
3. Агент 3 (роль - middle-юрист) оценивает, существуют ли нормы российского законодательства, которые регламентируют содержание прав и обязанностей, извлеченных агентом 2. Результат - файл rules.txt в data/processed.
4. Агент 4 (роль - senior-юрист) оценивает, есть ли противоречие между правами/обязанностями и релевантными нормами права, и, если есть, порождает ли оно правовой риск. Результат - файл risks.txt в data/processed.
5. Агент 5 (роль - партнер юридической фирмы) готовит окончательное юридическое заключение, в котором излагает суть проделанной работы и рекомендации для клиента.
Результат - файл report.txt в data/processed.

# Архитектура проекта
Проект реализован на python 3.12.9 в виде класса ContractAssessment, содержащего ряд методов, каждый из который содержит обращение к API DeepSeek-V3.
Для запуска проверки достаточно создать экземпляр класса и использовать метод .process

# Ограничения проекта
В основе проекта лежит две открытых для обсуждения гипотезы:
- гипотеза, согласно которой юридические последствия влечет не весь текст договора, а только та часть текста договора, которая касается установления, изменения или прекращения прав и обязанностей (согласно ГК РФ догоор - это соглашение об установлении/изменении/прекращении прав и обязанностей);
- гипотеза о паттерне связи синтаксиса и семантики договора (см. ниже).

Важно понимать различие между синтаксисом и семантикой текста договора. Установление, изменение и прекращение прав и обязанностей - это семантические категории.
Поскольку обрабатывается именно синтаксис текста, задача состоит в том, чтобы определить, какие синтаксичекие паттерны релевантны указанным семантическим категориям. Выдвигается следующее предположение:
- установление должно сопровождаться либо прямым указанием на действия, совершаемые сторонами (констатация обзанности), либо на обязанность/право совершить или не совершать те или иные действия;
- изменение - аналогичным образом;
- прекращение - формулировками "не имеет права, не несет ответственности, освобождается от ответственности (потому что ответственность - дополнительная обязанность, возникающая при неисполнении начальной обязанности).

## Структура проекта

```
├── README.md          <- Общая информация о проекте
│
├── data
│   ├── processed      <- Промежуточные и итоговый результаты обработки фрагмента договора
│   └── raw            <- Необработанная информация на входе (1.txt - тестовый фрагмент договора на входе)
│
├── requirements.txt   <- Необходимые зависимости проекта (библиотеки)`
│
└── src                <- Инструменты, позволяющие создать AI-агента
│   ├── __init__.py      <- Файл, делающий содержимое папки модулем пайтон
│   ├── function_call.py <- Как вызвать функцию с помощью ллм
│   ├── json_output.py   <- Как сделать, чтобы ллм отвечала в формате json
│   └── llm_call.py      <- Обращение к ллм по API
├── main.py            <- Основной код проекта
```