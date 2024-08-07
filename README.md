# dvmn-SupportBot

Бот-помощник для службы поддержки. Он помогает пользователю получить ответы на вопросы, а также при необходимости перенаправляет на операторов. В проекте используется DialogFlow - облачный сервис распознавания естественного языка от Google.

## Подготовка к запуску проекта

1. Python должен быть уже установлен. Склонируйте репозиторий и создайте виртуальную среду командой:

```python
python -m venv venv
```

2. Активируйте виртуальную среду для Windows(в ином случае см. [документацию](https://docs.python.org/3/library/venv.html)):

```python
.\venv\Scripts\activate.bat
```

3. Затем используйте pip для установки зависимостей:

```python
pip install -r requirements.txt
```

4. Зарегистрируйте бота в Telegram и получите его токен. Чтобы сгенерировать токен, вам нужно поговорить с `@BotFather` и выполнить несколько простых шагов описанных [здесь](https://core.telegram.org/bots#6-botfather).
5. Создайте сообщество VK.
6. Cоздайте проект в Google Cloud, используя [документацию](https://cloud.google.com/dialogflow/es/docs/quick/setup). 
7. Cоздайте диалогового агента, который будет выполнять основную работу по общению с пользователем, используя [документацию](https://cloud.google.com/dialogflow/es/docs/quick/build-agent). 
8. Для обращения к сервису через API понадобится JSON-ключ, необходимый для авторизаци. Подробнее [здесь](https://cloud.google.com/docs/authentication/api-keys). Чтобы получить API ключ запустите скрипт:

```python
python .\dialogflow.py
```

9. Чтобы агент начал обрабатывать запросы пользователя, нужно добавить в него Intents (намерения, цели). Подробнее [здесь](https://cloud.google.com/dialogflow/es/docs/quick/api#detect_intent).
10. Добавить тренировочные фразы (Training phrases), на основе которых Dialogflow определяет то или иное намерение пользователя. Иными словами обучить модель Dialogflow. Это можно сделать вручную или запустить скрипт, предварительно присвоив переменной окружения `TRAINING_PHRASES` путь к файлу с тренировочными фразами в формате json.

```python
python .\learning_script.py
```
_Пример файла с тренировочными фразами:_

```python
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    }
}
```
## Переменнные окружения

Часть данных проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и присвойте значения переменным окружения в формате: ПЕРЕМЕННАЯ=значение.

_Переменные окружения проекта:_

`TELEGRAM_BOT_TOKEN` — токен доступа к Telegram-боту.

`PROJECT_ID` — ID от вашего проекта в Google Cloud, который совпадает с ID диалогового "агента".

`GOOGLE_APPLICATION_CREDENTIALS` — переменная окружения, где лежит путь до файла с ключами от Google, credentials.json.

`VK_GROUP_TOKEN` — идентификатор сообщества VK. Токен VK можно получить в настройках сообщества.

`TELEGRAM_CHAT_ID` — идентификатор Telegram-чата для логов.

`TRAINING_PHRASES` — путь к файлу с тренировочными фразами в формате json.

## Как запустить

Убедитесь, что в терминале находитесь в директории кода и запустите бота, используя команды:

```python
python .\telegram_bot.py
```
или

```python
python .\vk_bot.py
```
_Примеры работы ботов:_

![vk_bot](https://github.com/juneshone/dvmn-SupportBot/blob/main/demo_vk_bot.gif)

Ссылка на vk-бота [здесь](https://vk.com/club226476141).

![tg_bot](https://github.com/juneshone/dvmn-SupportBot/blob/main/demo_tg_bot.gif)

Ссылка на telegram-бота [здесь](https://t.me/VerbGame_support_bot).

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).