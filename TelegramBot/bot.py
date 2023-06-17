from aiogram import Bot, types
import json
from pathlib import Path
import urllib.request

from src.utils.init_bot import dp, bot
from src.services.pdf import encrypt_pdf
from src.services.txt import encrypt_txt, decrypt_txt
from src.services.video import get_mp3_from_mp4

with open('TelegramBot/messages.json', encoding="utf-8") as f:
    messages = json.load(f)


@dp.message_handler(commands=['start'])
async def process_start_command_pdf(message: types.Message):
    message_text = messages.get('/start', 'Такой команды нет')
    await message.reply(message_text)


@dp.message_handler(commands=['pdf'])
async def start_cmd_handler_pdf(message: types.Message):
    # клавиатура для выбора команды
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    encrypt_btn = types.KeyboardButton('Зашифровать PDF')
    decrypt_btn = types.KeyboardButton('Дешифровать PDF')
    keyboard.add(encrypt_btn, decrypt_btn)
    await message.answer("Добро пожаловать! Что вы хотите сделать с файлом?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ['Зашифровать PDF', 'Дешифровать PDF'])
async def process_file_handler_pdf(message: types.Message):
    command = message.text

    await bot.send_message(message.chat.id, 'Отправьте PDF файл', reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
    async def process_filename_handler_pdf(message: types.Message):

        # проверка файла
        file_name = message.document.file_name
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        if file_name[len(Path(file_name).stem) + 1:] != 'pdf':
            await message.answer(file_name[len(Path(file_name).stem) + 1:])
            return

        file_url = bot.get_file_url(file.file_path)
        filename = str(message.chat.id) + '-' + file_name
        urllib.request.urlretrieve(file_url, f'input/{filename}')

        await message.answer('Введите пароль:')

        @dp.message_handler(lambda msg: msg.text.isdigit() is False)
        async def process_password_handler_pdf(message: types.Message):
            dp.message_handlers.unregister(process_password_handler_pdf)
            password = message.text

            if command == 'Зашифровать PDF':
                await encrypt_pdf(filename, password)
                with open(f'output/{filename}', 'rb') as f:
                    await bot.send_document(chat_id=message.chat.id, document=f,
                                            reply_to_message_id=message.message_id)
            elif command == 'Дешифровать PDF':
                await message.answer('Пока такой функции нет')
            else:
                await message.answer('Неверная команда')


@dp.message_handler(commands=['txt'])
async def start_cmd_handler_txt(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    encrypt_btn = types.KeyboardButton('Зашифровать txt')
    decrypt_btn = types.KeyboardButton('Расшифровать aes')
    keyboard.add(encrypt_btn, decrypt_btn)
    await message.answer("Добро пожаловать! Что вы хотите сделать с файлом?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ['Зашифровать txt', 'Расшифровать aes'])
async def process_file_handler_txt(message: types.Message):
    command = message.text
    if command == 'Зашифровать txt':
        await bot.send_message(message.chat.id, 'Отправьте txt файл', reply_markup=types.ReplyKeyboardRemove())
    elif command == 'Расшифровать aes':
        await bot.send_message(message.chat.id, 'Отправьте aes файл', reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
    async def process_filename_handler_txt(message: types.Message):

        # проверка файла
        file_name = message.document.file_name
        file_id = message.document.file_id
        file = await bot.get_file(file_id)

        file_url = bot.get_file_url(file.file_path)
        filename = str(message.chat.id) + '-' + file_name
        urllib.request.urlretrieve(file_url, f'input/{filename}')

        await message.answer('Введите пароль:')

        @dp.message_handler()
        async def process_password_handler_txt(message: types.Message):
            password = message.text

            if command == 'Зашифровать txt':
                if file_name[len(Path(file_name).stem) + 1:] != 'txt':
                    await message.answer(file_name[len(Path(file_name).stem) + 1:])
                    return
                await encrypt_txt(filename, password)
                with open(f'output/{filename[:-3] + "aes"}', 'rb') as f:
                    await bot.send_document(chat_id=message.chat.id, document=f,
                                            reply_to_message_id=message.message_id)
            elif command == 'Расшифровать aes':
                if file_name[len(Path(file_name).stem) + 1:] != 'aes':
                    await message.answer(file_name[len(Path(file_name).stem) + 1:])
                    return

                try:
                    await decrypt_txt(filename, password)
                except ValueError:
                    await message.answer("Неверный пароль! Попробуйте другой")
                    return

                with open(f'output/{filename[:-3] + "txt"}', 'rb') as f:
                    await bot.send_document(chat_id=message.chat.id, document=f,
                                            reply_to_message_id=message.message_id)
                dp.message_handlers.unregister(process_password_handler_txt)
            else:
                await message.answer('Неверная команда')


@dp.message_handler(commands=['get_mp3_from_mp4'])
async def process_file_handler_mp4(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте .mp4 файл')

    @dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
    async def process_filename_handler_mp4(message: types.Message):
        await bot.send_message(message.chat.id, 'В процессе...')
        # проверка файла
        file_name = message.document.file_name
        file_id = message.document.file_id
        file = await bot.get_file(file_id)

        file_url = bot.get_file_url(file.file_path)
        filename = str(message.chat.id) + '-' + file_name
        urllib.request.urlretrieve(file_url, f'input/{filename}')

        if file_name[len(Path(file_name).stem) + 1:] != 'mp4':
            await message.answer(file_name[len(Path(file_name).stem) + 1:])
            return
        await get_mp3_from_mp4(filename)
        with open(f'output/{filename[:-3] + "mp3"}', 'rb') as f:
            await bot.send_document(chat_id=message.chat.id, document=f,
                                    reply_to_message_id=message.message_id)
