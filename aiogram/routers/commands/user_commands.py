import json


import requests
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.common_keyboards import ButtonText, get_on_task_kb

router = Router(name=__name__)

class Login(StatesGroup):
    username = State()
    password = State()

class Registration(StatesGroup):
    username = State()
    password = State()
    email = State()


@router.message(F.text == ButtonText.REGISTER)
async def handle_register(message: types.Message, state: FSMContext):
    username = message.from_user.username
    await state.update_data(username=username)
    await message.answer(f"Ваше имя пользователя будет {username}. Введите пароль для регистрации:")
    await state.set_state(Registration.password)


@router.message(Registration.password)
async def handle_email(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer(f"{message.from_user.username}. Введите email, на который будут приходить напоминания о сроке задач:")
    await state.set_state(Registration.email)


@router.message(Registration.email)
async def process_password(message: types.Message, state: FSMContext):
    if await state.get_state() == Registration.email:
        await state.update_data(email=message.text)
        user_data = await state.get_data()
        json_data = json.dumps(user_data, indent=4)
        print(json_data)

        response = requests.post('http://api:8001/api/v1/register/', json=user_data)

        if response.status_code == 201:
            token = response.json().get('access')
            if token:
                await state.update_data(token=token)
                await message.answer("Вы успешно зарегистрированы!", reply_markup=get_on_task_kb())
            else:
                await message.answer("Ошибка получения токена!")
        elif response.status_code == 409:
            await message.answer("Пользователь с таким именем уже существует, нажмите Войти")
        else:
            await message.answer("Длина пароля не менее 8 символов")
        await state.clear()


@router.message(F.text == ButtonText.LOGIN)
async def process_login_username(message: types.Message, state: FSMContext):
    username = message.from_user.username
    await state.update_data(username=username)
    await message.answer(f"Дорогой, {username}. Введите пароль, чтобы войти:")
    await state.set_state(Login.password)


@router.message(Login.password)
async def process_login_password(message: types.Message, state: FSMContext):
    if await state.get_state() == Login.password:
        await state.update_data(password=message.text)
        user_data = await state.get_data()
        response = requests.post('http://api:8001/api/v1/login/', json=user_data)
        if response.status_code == 200:
            token = response.json().get('access')
            if token:
                await state.update_data(token=token)
                await message.answer("Вы успешно вошли в аккаунт", reply_markup=get_on_task_kb())
            else:
                await message.answer("Ошибка получения токена!")
        else:
            await message.answer("Неверные данные для входа.")
        await state.clear()
