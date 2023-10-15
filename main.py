import asyncio
import logging
# from aiogram import * #Можно, но не нужно
# from aiogram.filters import *
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject #For arguments in commands
from aiogram import F
from aiogram import html
from aiogram.utils.keyboard import ReplyKeyboardBuilder #For dynamic generetion buttons with Keyboard builder
from aiogram.utils.keyboard import InlineKeyboardBuilder #For URL-buttons
from datetime import datetime #for time link
from config_reader import config #SecretToken
from random import randint
from contextlib import suppress  #Without Bad requests
from aiogram.exceptions import TelegramBadRequest #Without Bad requests

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="MarkdownV2")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("*It's just begin*")
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор\!", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно\!")

# Хэндлер на команду /Answer
@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("_Your answer\!_")

# Хэндлер на команду /Reply
@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply("__Your reply\!__")

@dp.message(Command("testtext"))#Not upregister
async def cmd_testText(message: types.Message):
    await message.answer("<i>Hello</i>, <b>world</b>!", parse_mode="html")
    await message.answer("_Hello_, *world*\! __I am__  ~here~")

@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        # await message.answer(f"Привет, _*{command.args}*_")
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}", parse_mode="html")
    else:
        await message.answer("Please include your name after the /name command\!")

@dp.message(Command("find"))
async def cmd_find(message: types.Message, command: CommandObject):
    if command.args:
        #data = dict()
        data = {
            "url": "<N/A>",
            "email": "<N/A>",
            "code": "<N/A>",
            "bold": "<N/A>"
        }
        entities = message.entities or []
        for item in entities:
            if item.type in data.keys():
                # Неправильно
                # data[item.type] = message.text[item.offset : item.offset+item.length]
                # Правильно
                data[item.type] = item.extract_from(message.text)
        await message.reply(
            "Вот что я нашёл:\n"
            f"Имя: {html.quote(data['bold'])}\n"
            f"URL: {html.quote(data['url'])}\n"
            f"E-mail: {html.quote(data['email'])}\n"
            f"Пароль: {html.quote(data['code'])}", parse_mode="html"
        )
    else:
        await message.answer("Please, include text after the /find command\!")

@dp.message(Command("replybuilder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.add(types.KeyboardButton(text=str("Cancel")))
    builder.adjust(8, 8, 1)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True)#, one_time_keyboard=True),#selective - for pool of users
    )

@dp.message(F.text.lower() == "cancel")
async def without_puree(message: types.Message):
    await message.answer("Cancel\!", reply_markup=types.ReplyKeyboardRemove())

@dp.message(Command("specialbuttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок.
    builder.row(
        types.KeyboardButton(text="Запрос геолокации", request_location=True),
        types.KeyboardButton(text="Создать викторину", request_poll=types.KeyboardButtonPollType(type="quiz")),
        types.KeyboardButton(text="Запрос контакта", request_contact=True)
    )
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    builder.row(
        types.KeyboardButton(text=str("Cancel"))
    )

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )

@dp.message(F.chat_shared)
async def on_chat_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )

@dp.message(Command("inlineurl"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Telegram channel",
        url="tg://resolve?domain=telegram")
    )

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards
    user_id = 460621273#1234567890
    chat_id = -1001533375422
    bot_id = 6407233345
    # chat_info = await bot.get_chat(user_id)
    # chat_info = await bot.get_chat(chat_id)
    chat_info = await bot.get_chat(bot_id)
    # if not chat_info.has_private_forwards:
    #     builder.row(types.InlineKeyboardButton(
    #         text="Какой-то чат:",
    #         # url=f"tg://user?id={user_id}")
    #         # url=f"tg://user?id={chat_id}")
    #         url=f"tg://user?id={bot_id}")
    #     )
    builder.row(types.InlineKeyboardButton(
        text="Какой-то чат:",
        url=f"t.me/OneTwoFourBotChat")
    )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    valueStr = str(randint(1, 10))
    await callback.message.answer(valueStr)
    await callback.answer(
        text="Ваше число: " + valueStr + "!\nСпасибо, " + callback.from_user.username + ", что воспользовались ботом!\n",
        show_alert=True
    )
    # await callback.answer()

#---------------------------------------------------------------------
# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest): #Remove bad requests
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard(), parse_mode="html" #NEED PARSE MODE
        )

@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = -3
    await message.answer("Укажите число: " + str(user_data[message.from_user.id]), reply_markup=get_keyboard(), parse_mode="html") #NEED PARSE MODE

@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]
    # await callback.answer(text="Action = " + action,
    #     show_alert=True
    # )
    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        with suppress(TelegramBadRequest): #Remove bad requests
            await callback.message.edit_text(f"Итого: {user_value}", parse_mode="html") #NEED PARSE MODE

    await callback.answer()
#---------------------------------------------------------------------

@dp.message(F.animation)
async def echo_gif(message: types.Message):
    await message.answer("Here you are\!\n")
    await message.reply_animation(message.animation.file_id)

@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"D:/myDoc/Future/Telebot/testBotAiogram/tmp/{message.photo[-1].file_id}.jpg"
    )
    await message.answer("`Download of picture is complited\!`")

@dp.message(F.sticker)
async def download_sticker(message: types.Message, bot: Bot):
    await bot.download(
        message.sticker,
        # для Windows пути надо подправить
        destination=f"D:/myDoc/Future/Telebot/testBotAiogram/tmp/{message.sticker.file_id}.webp"
    )
    await message.answer("`Download of sticker is complited\!`")

@dp.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Hello there\!, {user.full_name} ")

@dp.message(F.text)#Without F.text it works too
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
        #added_text = f"__Создано в {time_now}__"
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="html") #message.html_text чтобы форматирование текста сохранялась

#Don't check---------------------------------------------------------------------

#---------------------------------------------------------------------

# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.message.register(cmd_reply, Command("reply"))  # регистарция команды /reply
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
