import string

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.kbd import Button, Row, ManagedCheckboxAdapter, Checkbox, SwitchTo, Cancel
from __init__ import bot, dp
import logging
from aiogram.types import Message

from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, DialogManager, Window, DialogRegistry, StartMode
from aiogram_dialog.widgets.text import Const
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Next, Back
import random

# Поработать с импортами
# Выделить пароль в мобильной версии(черный, белый фон???)
# Инструкция по применению
# Сгенерировать пароль снова - кнопка
# или сгенерировать с такими же параметрами
# Название, описание, ник бота
# Проверка на неверный ввод
# Добавить обычные кнопки вперед, назад, cancel
# Разделить параметры пароля, однвременный вывод
# Раскидать код по папкам


logging.basicConfig(level=logging.INFO)

message_start = "<strong>Привет, я генератор пароля!</strong>\nДавай настроим твой пароль=)"




numbers = string.digits
upper_letters = string.ascii_uppercase
symbols = string.punctuation
password = string.ascii_lowercase



# #
# # Вот тебе краткая инструкция по работе
# #
# # /create  - Создать новый пароль
# # /list      -  Список  сохраненных паролей
# # /clear   -  Очистить экран от всех записей


async def gen(m: CallbackQuery, button: Button, manager: DialogManager):
    await m.message.answer(text="Теперь введи кличество символов")
    # await manager.done()
    await manager.reset_stack()


async def check_changed1(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global check1
    global password
    check1 = True
    print("Check status changed:", checkbox.is_checked())
    check1 = checkbox.is_checked()
    if check1 == False:
        if symbols in password:
            print("Уже есть такие символы")
        else:
            password = password + symbols
            print(password)
    elif check1 == True:
        password = password.replace(symbols, '')
        print(password)




async def check_changed2(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global check2
    global password
    check2 = True
    print("Check status changed:", checkbox.is_checked())
    check2 = checkbox.is_checked()
    if check2 == False:
        if numbers in password:
            print("Уже есть такие символы")
        else:
            password = password + numbers
            print(password)
    elif check2 == True:
        password = password.replace(numbers, '')
        print(password)


async def check_changed3(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global check3
    global password
    print(password)
    check3 = True
    print("Check status changed:", checkbox.is_checked())
    check3 = checkbox.is_checked()
    if check3 == False:
        if upper_letters in password:
            print("Уже есть такие символы")
        else:
            password = password + upper_letters
            print(password)
    elif check3 == True:
        password = password.replace(upper_letters, '')
        print(password)

class DialogSG(StatesGroup):
    first = State()
    second = State()
    third = State()

dialog = Dialog(
    Window(
        Const("Добавить символы?"),
        Row(
            Checkbox(
                    Const("✓ Да"),
                    Const("Убрать символы"),
                    id="check1",
                    default=True,
                    on_state_changed=check_changed1,

                ),

            # SwitchTo(Const("To second"), id="sec", state=DialogSG.second)
            Next(),
        ),
        Cancel(),
        state=DialogSG.first,
    ),
    Window(
        Const("Добавить цифры"),
        Row(
            Back(),
            Checkbox(
                Const("✓ Да"),
                Const("Убрать цифры"),
                id="check2",
                default=True,
                on_state_changed=check_changed2,
            ),
            Next(),
        ),
        Cancel(),
        state=DialogSG.second,
    ),
    Window(
        Const("Добавить верхний регистр?"),
        Row(
            Back(),
            Checkbox(
                    Const("✓ Да"),
                    Const("Убрать цифры"),
                    id="check3",
                    default=True,  # so it will be checked by default,
                    on_state_changed=check_changed3,
                ),
            Button(Const("Сгенерировать"), id="gener", on_click=gen),
        ),
        Cancel(),
        state=DialogSG.third,
    )
)

registry = DialogRegistry(dp)
registry.register(dialog)



@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await bot.send_message(chat_id=m.from_user.id, text=message_start, parse_mode="HTML")
    await dialog_manager.start(DialogSG.first)



@dp.message_handler()
async def load_numberOfCharacters(message: types.Message, state: FSMContext):
    message.text = int(message.text)
    x = "".join(random.sample(password, message.text))
    passw = f'Ваш пароль: <code style="color:#0000ff">{x}</code>'
    await bot.send_message(message.from_user.id, text=passw,parse_mode="HTML")



executor.start_polling(dp, skip_updates=True, )
