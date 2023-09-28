import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject #For arguments in commands
from aiogram import F
from aiogram import html
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

# Хэндлер на команду /Answer
@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("Your answer\!")

# Хэндлер на команду /Reply
@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply("Your reply\!")

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

@dp.message(F.text)#Without F.text it works too
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
        #added_text = f"__Создано в {time_now}__"
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="html") #message.html_text чтобы форматирование текста сохранялась

# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.message.register(cmd_reply, Command("reply"))  # регистарция команды /reply
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
