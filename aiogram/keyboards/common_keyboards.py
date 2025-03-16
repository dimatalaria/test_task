from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Registration(StatesGroup):
    name = State()
    login = State()
    password = State()

class ButtonAction:
    BACK = "Назад"

class ButtonText:
    REGISTER = "Регистрация"
    LOGIN = "Вход"
    BYE = "Пока"

class ButtonTextTask:
    VIEW = "Просмотреть список задач"
    CREATE = "Создать задачу"
    DELETE = "Удалить задачу"
    CONTROL = "Комментарий"

class ButtonTextComment:
    CREATE = "Создать комментарий"
    CHANGE = "Изменить комментарий"
    DELETE = "Удалить комментарий"

def get_on_task_kb():
    button_view = KeyboardButton(text=ButtonTextTask.VIEW)
    button_create = KeyboardButton(text=ButtonTextTask.CREATE)
    button_delete = KeyboardButton(text=ButtonTextTask.DELETE)
    button_control_comm = KeyboardButton(text=ButtonTextTask.CONTROL)
    buttons_first_row = [button_view, button_create]
    buttons_second_row = [button_delete, button_control_comm]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
    )
    return keyboard

def get_on_start_kb():
    button_hello = KeyboardButton(text=ButtonText.REGISTER)
    button_help = KeyboardButton(text=ButtonText.LOGIN)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    buttons_first_row = [button_hello,button_help]
    buttons_second_row = [button_bye]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
    )
    return keyboard

def get_on_comm_kb():
    button_change = KeyboardButton(text=ButtonTextComment.CHANGE)
    button_delete = KeyboardButton(text=ButtonTextComment.DELETE)
    button_create = KeyboardButton(text=ButtonTextComment.CREATE)
    button_back = KeyboardButton(text=ButtonAction.BACK)
    buttons_first_row = [button_create, button_delete]
    buttons_second_row = [button_change, button_back]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
    )
    return keyboard