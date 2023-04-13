from telethon import TelegramClient
import telebot
import asyncio
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
import sqlite3
import datetime
import string

admin = 1627807288

TOKEN = "5602656872:AAGLvERhlZjsxJrPVy4me7_QuNSnVJ3CCF0"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def post_sql_query(sql_query):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result

def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS user
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        data TEXT,
                        all_message INTEGER NOT NULL,
                        ban INTEGER NOT NULL);'''
    post_sql_query(users_query)

def create_tables2():
    users_query = '''CREATE TABLE IF NOT EXISTS messages
                        (message INTEGER);'''
    post_sql_query(users_query)

    user_check_query = f'SELECT * FROM messages;'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO messages VALUES (0)'
        post_sql_query(insert_to_db_query)

create_tables()
create_tables2()

def register_user(user):
    user_check_query = f'SELECT * FROM user WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO user VALUES ({user}, "2021-07-36 09:00:48.797706", 0, 0)'
        post_sql_query(insert_to_db_query)

def get_usersId_banker():
    try:
        array = []

        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * FROM user").fetchall()

            for row in rows:
                array.append(row[0])

        return array
    except Exception as e:
        print(e)

def update_messages(user):
	users_query = f"UPDATE user SET all_message = all_message + 1 WHERE user_id = {user}"
	post_sql_query(users_query)

def update_messages2():
    users_query = f"UPDATE messages SET message = message + 1"
    post_sql_query(users_query)

def check_messages_all():
    users_query = "SELECT message FROM messages"
    return post_sql_query(users_query)[0][0]

def users_bd():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT `user_id` FROM `user`")
        row = cur.fetchall()
        users = row
        return users

def banan(user):
    banan = f"UPDATE user SET ban = 1 WHERE user_id = {user}"
    post_sql_query(banan)

def unbanan(user):
    unbanan = f"UPDATE user SET ban = 0 WHERE user_id = {user}"
    post_sql_query(unbanan)

def check_banan(user):
    check_banan = f"SELECT ban FROM user WHERE user_id = {user}"
    check_banan = post_sql_query(check_banan)
    return check_banan[0][0]

def check_data(users):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM user WHERE user_id = {users}').fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_hour = 0
    print (row[1][:-10:])
    if str(row[1][:-10:]) == current_time[:-10:]:
        amount_user_hour = 1

    return(amount_user_hour)

def update_data(user):
    f = f"{datetime.datetime.now()}"
    update_datas = f"UPDATE user SET data = '{f}' WHERE user_id = {user}"
    post_sql_query(update_datas)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/start", "/help", "/rules", "/button"]
    keyboard.add(*buttons)
    await message.answer('Выбери одну из кнопок для дальнейших действий!', reply_markup=keyboard)
 
    
@dp.message_handler(commands=['button'])
async def help_message(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id)
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT `user_id` FROM `user`")
        row = cur.fetchall()
        users = row
        cur.execute(f"SELECT all_message FROM user WHERE user_id = {message.from_user.id}")
        row = cur.fetchone()
        messages = row[0]
        await message.answer(f'Вы успешно включили кнопки. Выберите кнопку для дальнейших действий.')

@dp.message_handler(commands=['rules'])
async def start_message(message: types.Message):
    await message.answer(f'🎉 Никаких правил!!! ',parse_mode="html")
    
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id)
    await message.answer(f'👋 Приветствую <b>{message.from_user.full_name}</b> в <code> ANON BOT</code>!\nНажми на кнопку "/help" чтобы понять как использовать бота!',parse_mode="html")

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
        if int(message.from_user.id) == int(admin):
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT user_id FROM user WHERE ban = 1")
                row = cur.fetchall()
                if not len(row) == 0:
                    all_ids = ""
                    await message.answer('⛔ Заблокированные пользователи: ')
                    for cort in row:
                        cort = str(cort[0])
                        all_ids = all_ids + (f"<a href='tg://user?id={cort}'>{cort}</a>" + " ".join("\n"))
                        pass
                    await message.answer(f"{all_ids}", parse_mode="html")
                else:
                    await message.answer("⛔ Заблокированных пользователей нет!")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id)
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT `user_id` FROM `user`")
        row = cur.fetchall()
        users = row
        cur.execute(f"SELECT all_message FROM user WHERE user_id = {message.from_user.id}")
        row = cur.fetchone()
        messages = row[0]
        await message.answer(f'📝 Напишите боту что угодно и это отправится всем пользователям анонимно! \nВсего вами написано сообщений: {str(messages)}\nВсего сообщений в боте: {str(check_messages_all())}\n\nВсего пользователей в боте : {str(len(users))}')

@dp.message_handler(content_types=['text', 'voice', 'video_note', 'sticker', 'audio', 'dice', 'photo', 'video', 'animation'])
async def photo(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id)
    try:
        user = message.from_user.id
        if not int(check_banan(message.from_user.id)) == int(1):
            if f"i{check_data(message.from_user.id)}" == "i1":
                if not int(message.from_user.id) == int(admin):
                    await message.answer("⚠️ Недавно вы уже отправляли сообщение!\n Подождите ровно 1 минуту, после чего вы сможете написать снова!")
                else:
                    rows = get_usersId_banker()
                    update_messages(message.from_user.id)
                    update_messages2()
                    for row in rows:
                        try:
                            if not str(row) == str(message.from_user.id):
                                await bot.copy_message(
                                    row,
                                    message.chat.id,
                                    message.message_id,
                                )
                        except Exception as e:
                            pass
            else:
                if message.content_type in ['photo', 'video', 'animation', 'sticker']:
                    if not int(message.from_user.id) == int(admin):
                        update_data(message.from_user.id)
                    rows = get_usersId_banker()
                    update_messages(message.from_user.id)
                    update_messages2()
                    for row in rows:
                        try:
                            if not str(row) == str(message.from_user.id):
                                await bot.copy_message(
                                    row,
                                    message.chat.id,
                                    message.message_id,
                                )
                                if str(row) == str(admin):
                                    await bot.send_message(admin, f"👤 Пользователь: <code>{message.from_user.id}</code>\nПрофиль: <a href='tg://user?id={message.from_user.id}'>{message.from_user.id}</a>", parse_mode="html")
                        except Exception as e:
                            pass
                else:
                    if message.content_type in ['voice', 'video_note', 'audio', 'dice']:
                        if not int(check_banan(message.from_user.id)) == int(1):
                            if not int(message.from_user.id) == int(admin):
                                update_data(message.from_user.id)
                            rows = get_usersId_banker()
                            update_messages(message.from_user.id)
                            update_messages2()
                            for row in rows:
                                try:
                                    if not str(row) == str(message.from_user.id):
                                        await bot.copy_message(
                                            row,
                                            message.chat.id,
                                            message.message_id,
                                        )
                                except Exception as e:
                                    pass
                    else:
                        if not message.text.startswith("/ban"):
                            if not message.text.startswith("/unban"):
                                if not int(check_banan(message.from_user.id)) == int(1):
                                    rows = get_usersId_banker()
                                    if not int(message.from_user.id) == int(admin):
                                        update_data(message.from_user.id)
                                    update_messages(message.from_user.id)
                                    update_messages2()
                                    for row in rows:
                                        try:
                                            if not str(row) == str(message.from_user.id):
                                                await bot.copy_message(
                                                    row,
                                                    message.chat.id,
                                                    message.message_id,
                                                )
                                            if str(row) == str(admin):
                                                if str(message.from_user.id) != str(row):
                                                    await bot.send_message(admin, f", 👤 Пользователь: <code>{message.from_user.id}</code>\nПрофиль: <a href='tg://user?id={message.from_user.id}'>{message.from_user.id}</a>", parse_mode="html")
                                        except Exception as e:
                                            pass
                        if message.text.startswith("/ban"):
                            if int(message.from_user.id) == int(admin):
                                banan(message.text[5:])
                                await message.answer(f"✅ Заблокирован пользователь: <code>{message.text[5:]}</code>\nПрофиль: <a href='tg://user?id={message.text[5:]}'>{message.text[5:]}</a>", parse_mode="html") 
                        if message.text.startswith("/unban"):
                            if int(message.from_user.id) == int(admin):
                                unbanan(message.text[7:])
                                await message.answer(f"✅ Разблокирован пользователь: <code>{message.text[7:]}</code>\nПрофиль: <a href='tg://user?id={message.text[7:]}'>{message.text[7:]}</a>", parse_mode="html") 
    except Exception as e:
    	print(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)