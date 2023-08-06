# WeatherBot
______

**WeatherBot** - это бот написанный на языке python для платформы telegram,
с его помощью пользователь может узнать погоду. 
Это мой pet project, созданный для изучения программирования и computer science, отработки навыков
работы с языком программирования и его библиотеками.

***Он имеет следующий функционал в виде команд:***
- /start -- основная команда позволяющая узнать:
  - погоду на данный момент времени;
  - погоду на пять дней вперед;
  - получить открытку с погодой на данный момент времени.
- /help -- выводит информацию о функционале бота
- /delete -- полностью чистит чат от сообщений.


## Установка и запуск

Скачиваем репозиторий со всеми файлами с [GitHub](https://github.com/ArtemStriver/WeatherBot).
Создаем виртуальное окружение, но можно в коренную папку, и загружаем туда все необходимые пакеты
с помощью команды: 
``` python
pip install -r requirements.txt
```
Готово, теперь открываем файл `bot.py` и запускаем его.
Переходим в телеграм, ищем бота с именем [PetWeather_Bot](https://t.me/PetWeather_Bot) и начинаем диалог.

## Используемые технологии

![version](https://img.shields.io/badge/python-3.11-blue)


![package](https://img.shields.io/badge/pyTelegramBotAPI-4.12.0-violet)
![package](https://img.shields.io/badge/requests-2.31.0-violet)
![package](https://img.shields.io/badge/OpenCV-4.8.0-violet)

![license](https://img.shields.io/badge/license-Apache__License__V2.0-green)

В проекте использовано логирование, объектно-ориентированное программирование (ООП), работа с JSON-файлами.

## Лицензия

Проект разработан с использованием лицензии [Apache License, Version 2.0](https://opensource.org/license/apache-2-0/)







