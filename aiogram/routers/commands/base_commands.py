from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

from keyboards.common_keyboards import get_on_start_kb, ButtonText

router = Router(name=__name__)

@router.message(CommandStart())
async def handle_start(message: types.Message):
    url = "https://w7.pngwing.com/pngs/547/380/png-transparent-robot-waving-hand-bot-ai-robot-thumbnail.png"
    await message.answer(
        text=(
            f"{markdown.hide_link(url)}Привет, {markdown.hbold(message.from_user.full_name)}, "
            f"я твой помощник по управлению задачами!\n"
            f"Если ты уже зарегистрирован, то нажми 'Вход'.\n"
            f"Иначе 'Регистрация'."
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=get_on_start_kb(),
    )


@router.message(Command("description", prefix="!/"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.text(
            markdown.markdown_decoration.bold(
                markdown.text(
                "Привет, с помощью данного бота вы можете:\n"
                "✅Создавать задачи и управлять ими\n"
                "✅Оставлять дополнительные комментарии к задачам\n"

                ),
            ),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )