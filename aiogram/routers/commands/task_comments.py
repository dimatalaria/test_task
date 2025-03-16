import json

import httpx
import requests
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .user_tasks import get_comment

from keyboards.common_keyboards import ButtonTextTask, get_on_task_kb, get_on_start_kb, get_on_comm_kb, \
    ButtonTextComment, ButtonAction

router = Router(name=__name__)

class Comments(StatesGroup):
    task_id = State()
    content = State()

class DeleteCommentState(StatesGroup):
    waiting_for_comment_id = State()
    waiting_for_change_comment_id = State()
    waiting_for_new_comment_text = State()

@router.message(F.text == ButtonTextTask.CONTROL)
async def handle_create_comments(message: types.Message):
    await message.answer("Выберите необходимое действие",reply_markup=get_on_comm_kb())

@router.message(F.text == ButtonAction.BACK)
async def handle_back(message: types.Message):
    await message.answer('Меню управления', reply_markup=get_on_task_kb())


@router.message(F.text == ButtonTextComment.CREATE)
async def write_task_id(message: types.Message, state: FSMContext):
    await message.answer("Введите ID задачи, к которой необходимо добавить комментарий")
    await state.set_state(Comments.task_id)


@router.message(Comments.task_id)
async def write_comments(message: types.Message, state: FSMContext):
    await state.update_data(task_id=message.text)
    data = await state.get_data()
    await message.answer(f"Введите комментарий к задаче с ID {data.get('task_id')}")
    await state.set_state(Comments.content)


@router.message(Comments.content)
async def create_process_comment(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    comment_data = await state.get_data()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://api_comment:8002/api/v1/aiogram/comments/", json=comment_data)
    if response.status_code == 200:
        await message.answer("Комментарий успешно создан!",reply_markup=get_on_task_kb())
    elif response.status_code == 400:
        await message.answer("Комментарий для этой задачи уже существует",reply_markup=get_on_comm_kb())
    elif response.status_code == 404:
        await message.answer("Задачи с таким ID не существует", reply_markup=get_on_comm_kb())
    await state.clear()


@router.message(F.text == ButtonTextComment.DELETE)
async def delete_comment(message: types.Message, state: FSMContext):
    await message.answer("Введите ID задачи, в которой желаете удалить комментарий")
    await state.set_state(DeleteCommentState.waiting_for_comment_id)


@router.message(DeleteCommentState.waiting_for_comment_id)
async def process_task_id(message: types.Message, state: FSMContext):
    task_id = message.text
    async with httpx.AsyncClient() as client:
        response = await client.delete(f'http://api_comment:8002/api/v1/aiogram/delete/comments/{task_id}/')
    if response.status_code == 200:
        await message.answer("✅ Комментарий успешно удален.", reply_markup=get_on_task_kb())
    elif response.status_code == 404:
        await message.answer(f"❌ Комментарий к данному {task_id} не найден", reply_markup=get_on_task_kb())
    else:
        await message.answer("❌ Произошла ошибка при удалении комментария. Попробуйте ещё раз.", reply_markup=get_on_task_kb())

    await state.clear()


@router.message(F.text == ButtonTextComment.CHANGE)
async def handle_change_comment(message: types.Message, state: FSMContext):
    await message.answer("Введите ID задачи, у которой необходимо изменить комментарий")
    await state.set_state(DeleteCommentState.waiting_for_change_comment_id)


@router.message(DeleteCommentState.waiting_for_change_comment_id)
async def change_comment_content(message: types.Message, state: FSMContext):
    task_id = message.text
    comments = await get_comment(task_id)
    if not comments:
        await message.answer(f"Комментариев для задачи {task_id} нет.", reply_markup=get_on_comm_kb())
        await state.clear()
        return

    await state.update_data(task_id=task_id)
    await message.answer(f"Текущий комментарий: 📝{comments[0]}\nВведите новый текст:")
    await state.set_state(DeleteCommentState.waiting_for_new_comment_text)

@router.message(DeleteCommentState.waiting_for_new_comment_text)
async def update_comment(message: types.Message, state: FSMContext):
    new_content = message.text
    user_data = await state.get_data()
    task_id = user_data.get("task_id")

    payload = {
        "task_id": task_id,
        "content": new_content
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://api_comment:8002/api/v1/aiogram/comments/{task_id}/",
            json=payload
        )

    if response.status_code == 200:
        await message.answer("✅ Комментарий успешно обновлён!", reply_markup=get_on_task_kb())
    elif response.status_code == 404:
        await message.answer("❌ Комментарий не найден.",reply_markup=get_on_comm_kb())
    else:
        await message.answer("❌ Произошла ошибка при обновлении комментария.",reply_markup=get_on_comm_kb())

    await state.clear()
