# TodoListbot

Описание проекта:
Этот проект представляет собой телеграм бота, который написан при помощи библиотеки Aiogram.
Бот позволяет создавать Tasks(задачи), удалять задачи, добавлять комментарий к задачам, а также редактировать и удалять эти комментарии.
Также в TodoListbot есть функция напоминания об истечении срока исполнения задачи(реализованно с помощью Celery).
Бэкенд часть, которая связывает бота и задачи написана с помощью библиотеки Django REST framework.
Бэкенд часть, которая связывает задачи и комментарии написана с помощью библиотеки Fastapi.
Реализована регистрация, используя JWT токены, а также используется Redis для кэширования.
В проекте есть готовый docker-compose.yml для его лёгкого запуска в Docker.
Также есть удобная панель администратора для управления пользователями, реализованна с помощью Django.
В проекте используется Postgresql для хранения задач и управлениями ими.

Project Description:
This project is a telegram bot that is written using the Aiogram library.
The bot allows you to create Tasks, delete tasks, add comments to tasks, as well as edit and delete these comments.
Also TodoListbot has a function to remind you when a task is due (implemented using Celery).
The backend part that connects the bot and tasks is written using Django REST framework library.
The backend part that connects tasks and comments is written using Fastapi library.
Registration is implemented using JWT tokens and also uses Redis for caching.
The project has a ready-made docker-compose.yml to easily run it in Docker.
There is also a handy admin panel for user management, implemented with Django.
The project uses Postgresql to store tasks and manage them.

---

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone <URL репозитория>

2. Установите на свой ПК или виртуальную машину Docker-Desktop или Docker Engine.

3. Перейдите в папку test ,заполните файл .env.template по своим параметрам и переименуйте его в .env.

4. Используйте telegram и BotFather для регистрации своего бота и получения BOT_TOKEN.

5. Запустите Docker на своем ПК и находясь в папке test, через консоль запустите контейнеры командой: docker compose up --build.

6. Перейдите в бота, которого вы создали и проверьте полный функционал.

## Installation

1. Clone the repository:
   ```bash
   git clone <URL of repository>

2. Install Docker-Desktop or Docker Engine on your PC or virtual machine.

3. Go to the test folder, fill the .env.template file with your parameters and rename it to .env.

4. Use telegram and BotFather to register your bot and get BOT_TOKEN.

5. Start Docker on your PC and while in the test folder, start the containers through the console with the command: docker compose up --build.

6. Switch to the bot you created and check the full functionality.
