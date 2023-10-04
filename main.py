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
from datetime import datetime #for time link
from config_reader import config #SecretToken

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
    builder.add(types.KeyboardButton(text=str("Cansel")))
    builder.adjust(8, 8, 1)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True) #, one_time_keyboard=True),#selective - for pool of users
    )

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

@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор\!", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно\!")

@dp.message(F.text.lower() == "cansel")
async def without_puree(message: types.Message):
    await message.reply("Cansel\!", reply_markup=types.ReplyKeyboardRemove())

async def without_puree(message: types.Message):
    await message.reply("Так невкусно\!")

@dp.message(F.text)#Without F.text it works too
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
        #added_text = f"__Создано в {time_now}__"
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="html") #message.html_text чтобы форматирование текста сохранялась

@dp.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Hello there\!, {user.full_name} ")



#Don't check-------------------------------------------------------------------

#-------------------------------------------------------------------

# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.message.register(cmd_reply, Command("reply"))  # регистарция команды /reply
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
