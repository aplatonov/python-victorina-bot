## Телеграм-бот "Викторина"

Бот для проведения викторин. Создан в рамках итогового задания курса Python от Mediasoft (май 2021).

### Требования
Должны быть установлены:
- git
- python (>=3.9)
- pipenv

### Установка и запуск

1. Создаем бота в Telegram  
   1.1. Находим в поиске @BotFather, стучимся к нему  
   1.2. Создаем и настраиваем бота (команда /help и/или можно почитать https://core.telegram.org/bots)  
   1.3. Сохраняем "token to access the HTTP API", в дальнейшем этот токен надо будет поместить в конфиг  
2. git clone https://github.com/aplatonov/python-victorina-bot.git
3. cd python-victorina-bot
4. pipenv sync (создание виртуального окружения)
5. pipenv shell (активация виртуального окружения)
6. cp config.example config.py
7. Вносим актуальные значения в config.py
8. Запускаем бота python main.py

### Доступные команды
- /start
- /help
- /go