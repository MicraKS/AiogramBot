from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.kbd import Button, Row, ManagedCheckboxAdapter, Checkbox
from __init__ import bot, dp
import logging
from aiogram.types import Message

from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, DialogManager, Window, DialogRegistry, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram.dispatcher.filters.state import StatesGroup, State

logging.basicConfig(level=logging.INFO)

message_start = "<code>Привет, я генератор пароля!</code>\nДавай настроим твой пароль=)"


# #
# # Вот тебе краткая инструкция по работе
# #
# # /create  - Создать новый пароль
# # /list      -  Список  сохраненных паролей
# # /clear   -  Очистить экран от всех записей


class DialogSG(StatesGroup):
    first = State()
    second = State()
    third = State()
    numberOfCharacters = State()


async def to_second(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()


async def go_back(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().back()


async def go_next(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()



async def gen(m: Message, button: Button, manager: DialogManager):
    await bot.send_message(chat_id=m.from_user.id, text="Теперь введи кличество символов")
    # await manager.dialog().close() # Сделать финиш состояния или переход из основного состояния в функцию



async def check_changed(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    print("Check status changed:", checkbox.is_checked())


dialog = Dialog(#Сократить повторы
    Window(
        Const("Добавить символы?"),
        Row(
            Checkbox(
                Const("✓ Да"),
                Const("Убрать символы"),
                id="check",
                default=True,  # so it will be checked by default,
                on_state_changed=check_changed,
            ),
            Button(Const("To second"), id="sec", on_click=to_second),
        ),
        state=DialogSG.first,
    ),
    Window(
        Const("Добавить цифры"),
        Row(
            Button(Const("Back"), id="back2", on_click=go_back),
            Checkbox(
                Const("✓ Да"),
                Const("Убрать цифры"),
                id="check2",
                default=True,  # so it will be checked by default,
                on_state_changed=check_changed,
            ),
            Button(Const("Next"), id="next2", on_click=go_next),
        ),
        state=DialogSG.second,
    ),
    Window(
        Const("Добавить верхний регистр?"),
        Row(
            Button(Const("Back"), id="back3", on_click=go_back),
            Checkbox(
                Const("✓ Да"),
                Const("Убрать цифры"),
                id="check3",
                default=True,  # so it will be checked by default,
                on_state_changed=check_changed,
            ),
            Button(Const("Сгенерировать"), id="next3", on_click=gen),#Что тут с on_click?
        ),
        state=DialogSG.third,
    )
)

registry = DialogRegistry(dp)  # this is required to use `aiogram_dialog`
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await bot.send_message(chat_id=m.from_user.id, text=message_start, parse_mode="HTML")
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    await dialog_manager.start(DialogSG.first)

@dp.message_handler()
async def load_numberOfCharacters(message: types.Message, state: FSMContext): # Не хватает хендркл для последующей работы
    print("ok")
    global password
    async with state.proxy() as data: # Сделать бд
        try:
            data['numberOfCharacters'] = int(message.text)
        except ValueError:
            await message.reply("Сколько символов будет в пароле?")
            data['numberOfCharacters'] = int(message.text)
    print(data['numberOfCharacters'])



executor.start_polling(dp, skip_updates=True, )
