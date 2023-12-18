from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: Message, l10n: FluentLocalization) -> None:
    """
    Функція для обробки команди start
    :param message: вхідне повідомлення
    :param l10n: локалізатор для отримання перекладу тексту
    :return: None
    """
    value = l10n.format_value(
        msg_id="info",
        args={
            "username": message.from_user.full_name
        }
    )
    await message.answer(value)
