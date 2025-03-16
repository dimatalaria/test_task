import json

import httpx
import requests
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from datetime import datetime

from keyboards.common_keyboards import ButtonTextTask, get_on_task_kb, get_on_start_kb

router = Router(name=__name__)

class DeleteTaskState(StatesGroup):
    waiting_for_task_id = State()

class TaskCreation(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()

async def get_comment(task_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api_comment:8002/api/v1/aiogram/view/comments/{task_id}/")
        response_json = response.json()
        print(response_json.get('contents'))
        return response_json.get("contents")


def format_date(date_string):
    parsed_date = datetime.fromisoformat(date_string)
    return parsed_date.strftime("%d.%m.%Y %H:%M")


@router.message(F.text == ButtonTextTask.CREATE)
async def handle_create_task(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок задачи:")
    await state.set_state(TaskCreation.title)


@router.message(TaskCreation.title)
async def process_task_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(TaskCreation.description)


@router.message(TaskCreation.description)
async def process_task_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите дату выполнения задачи (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    await state.set_state(TaskCreation.due_date)


@router.message(TaskCreation.due_date)
async def process_task_due_date(message: types.Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    await message.answer("Введите категорию задачи:")
    await state.set_state(TaskCreation.category)


@router.message(TaskCreation.category)
async def process_task_category(message: types.Message, state: FSMContext):
    await state.update_data(category={"name": message.text})
    task_data = await state.get_data()
    task_data['user'] = message.from_user.username
    json_data = json.dumps(task_data, indent=4)
    print(json_data)
    async with httpx.AsyncClient() as client:
        response = await client.post('http://api:8001/api/v1/create/', json=task_data)
    if response.status_code == 201:
        await message.answer("Задача успешно создана!", reply_markup=get_on_task_kb())
    else:
        await message.answer("Произошла ошибка при создании задачи. Попробуйте снова.",reply_markup=get_on_task_kb())
    await state.clear()


@router.message(F.text == ButtonTextTask.VIEW)
async def views_tasks(message: types.Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://api:8001/api/v1/task/{message.from_user.username}')
    if response.status_code == 500:
        await message.answer(
            "Произошла ошибка при просмотре задач, пользователь с вашим именем был удален администратором\n Зарегистрируйтесь заново",
            reply_markup=get_on_start_kb()
        )
        return

    try:
        tasks = response.json()
    except requests.exceptions.JSONDecodeError:
        await message.answer("Ошибка сервера задач")
        return

    if not tasks:
        await message.answer("Нет задач для отображения.")
        return

    formatted_tasks = []
    for task in tasks:
        comments = await get_comment(task['id'])
        formatted_task = (
            f"🆔 **ID**: {task['id']}\n"
            f"📌 **Задача**: {task['title']}\n"
            f"📖 **Описание**: {task['description']}\n"
            f"📅 **Дата создания**: {format_date(task['created_at'])}\n"
            f"📅 **Срок исполнения**: {format_date(task['due_date'])}\n"
            f"📂 **Категория задачи**: {task['category']['name']}\n"
            f"📝 **Комментарии**: {', '.join(comments) if comments else 'Нет комментариев'}\n"
        )
        formatted_tasks.append(formatted_task)
    await message.answer("\n\n".join(formatted_tasks))



@router.message(F.text == ButtonTextTask.DELETE)
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer("Введите ID задачи, которую хотите удалить")
    await state.set_state(DeleteTaskState.waiting_for_task_id)


@router.message(DeleteTaskState.waiting_for_task_id)
async def process_task_id(message: types.Message, state: FSMContext):
    task_id = message.text
    async with httpx.AsyncClient() as client:
        response = await client.delete(f'http://api:8001/api/v1/delete/{task_id}/')

    if response.status_code == 204:
        await message.answer("✅ Задача успешно удалена.",reply_markup=get_on_task_kb())
    elif response.status_code == 404:
        await message.answer("❌ Задача с указанным ID не найдена.",reply_markup=get_on_task_kb())
    else:
        await message.answer("❌ Произошла ошибка при удалении задачи. Попробуйте ещё раз.",reply_markup=get_on_task_kb())

    await state.clear()