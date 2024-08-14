# Бот с интеграцией dialogflow

Dialogflow, ведущая платформа диалогового искусственного интеллекта, позволяет разработчикам и предприятиям создавать насыщенные, интуитивно понятные чаты и голосовые интерфейсы.
Пример работы:

![image info](https://dvmn.org/filer/canonical/1569214094/323/)

![image info](https://dvmn.org/filer/canonical/1569214089/322/)

[DEMO tg bot](https://t.me/vgame_support_dfbot)

[DEMO  vk club](https://vk.com/club226944360)

### Требования:

- Создать телеграм бот, получить токен от него
- Создать сообщество ВК, получить api ключ, включить longpolling
- Как создать проект в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/setup)
- Создать агент в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/build-agent)
- [Включить API DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) на вашем Google-аккаунте
- Получить ключи credentials.json c помощью [google cli](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
- [Создать токен](https://cloud.google.com/docs/authentication/api-keys) DialogFlow

### Установка:

- Склонировать этот репозиторий
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- в корне проекта создать файл .env и прописать значения:

```
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json - путь к файлу credentials
TG_TOKEN=Токен от телеграма
VK_TOKEN=Токен от группы ВК
TG_LOGS_CHAT_ID=id чата для отправки логов

```

### Обучение DialogFlow
```
python teach_df.py questions.json
```

### Запуск:
```
python tg_bot.py
python vk_async.py
```

