from json import load

from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy import create_engine

from db.models import (
    Student,
    Book
)

from db.password import (
    verify_password,
    get_hashed_password
)

from bot.utils import (
    ItemGetter,
    ReplyGenerator,
    ItemPaginator
)


with open('E:/tokens.json', 'r') as f:
    db_token = load(f)["db-token"]
    

engine = create_engine(db_token)

START, LOGIN, SHOP, MENU, PROFILE, INVENTORY = range(6)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data

    user_data["student"] = None
    user_data["login_status"] = None
    user_data["inventory"] = []
    user_data["basket"] = []
    user_data["shop_paginator"] = ItemPaginator(
        engine=engine,
        item_model=Book,
        lines=3,
        columns=3
    )

    text = "Привет! Введи свой логин, чтобы продолжить."

    await update.message.reply_text(
        text=text
    )

    return START


async def enter_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    login = update.message.text

    getter = ItemGetter(engine, Student)
    student = getter.get_item("login", login)

    if not student:
        text = "Логин неверный, попробуйте ещё раз."

        await update.message.reply_text(
            text=text
        )

        return START

    user_data["student"] = student

    text = "Введите пароль."

    await update.message.reply_text(
        text=text
    )

    return LOGIN


async def enter_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    password = update.message.text

    student = user_data["student"]

    if not verify_password(password, student.hashed_password):
        text = "Пароль неверный, попробуйте ещё раз."

        await update.message.reply_text(
            text=text
        )

        return LOGIN

    user_data["login_status"] = True

    text = f"Добро пожаловать, {student.last_name} {student.first_name}!"

    await update.message.reply_text(
        text=text,  # можно вместо меню сразу после пароля сделать кнопку "Войти",
        reply_markup=ReplyGenerator.menu_markup()  # чтобы сохранить логику и поставить меню в отдельное состояние
    )

    return MENU


async def show_shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    callback_text = update.message.text
    paginator = user_data["shop_paginator"]

    paginator.do_action(callback_text)

    text, reply_markup = paginator.page_text(), paginator.show_page()

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

    return SHOP


async def show_shop_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # показать айтем в чате с кнопками для взаимодействия
    pass


async def show_basket(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # клавиатура через ItemPaginator со списком всех книг в корзине
    # при нажатии появляется соответствующее описание книги в чате с кнопками
    pass


async def show_inventory(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # две кнопки: "книги в обработке" и "нужно отдать"
    # первая для книг, которые ещё не успел получить
    # вторая для книг, которые нужно будет отдать
    await update.message.reply_text(
        text=update.message.text,
        reply_markup=ReplyGenerator.inventory_markup()
    )

    return INVENTORY


async def books_in_process(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def books_to_give_back(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def show_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text=update.message.text,
        reply_markup=ReplyGenerator.profile_markup()
    )

    return PROFILE


async def change_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # show something like: enter your current password
    # if it's correct show: enter your new password
    # await for new password and after that update password in data base
    # if it's incorrect show: incorrect password
    pass


async def show_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text=update.message.text,
        reply_markup=ReplyGenerator.menu_markup()
    )

    return MENU


async def quit_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # что-то для выхода из бота, скорее всего клавиатура с кнопкой "Войти",
    # чтобы можно было сразу войти обратно
    pass

# ! сделать выход по желанию из ввода логина и пароля (добавить клавиатуру с кнопкой "Выход")
