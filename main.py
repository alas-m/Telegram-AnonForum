import asyncio
import random
import sqlite3
import string
import config
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from functions import (
	create_user, add_user, add_chat, update_chat_user_count,
	get_chat_info, get_users_in_chat, generate_chat_id
)

BOT_TOKEN = config.API
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	create_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
	args = message.get_args()
	if args.startswith("joinchat_"):
		chat_id = args.replace("joinchat_", "")
		chat_info = get_chat_info(chat_id)
		if chat_info:
			chat_name = chat_info[0]
			display_name = f"Anonymous{random.randint(1000, 9999)}"
			add_user(message.from_user.id, chat_id, display_name)
			update_chat_user_count(chat_id)
			await message.reply(f"You joined chat named <b>{chat_name}</b>")
			users = get_users_in_chat(chat_id)
			for user_id, _ in users:
				if user_id != message.from_user.id:
					await bot.send_message(user_id, f"💬: <b>{display_name}</b> joined the chat.")
		else:
			await message.reply("Chat not found or invalid link.")
	else:
		await message.reply("Welcome! Use a valid invitation link to join a chat or create a chat by pressing /createchat.\n\nPress /help to get a list of available commands.")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
	await message.reply("Here is the list of available commands:\n\n/help - This menu\n/createchat <code>[CHAT NAME]</code> - Create a chat\n/chatinfo <code>[CHAT ID]</code>\n/leave - Leave a chat\n/setname <code>[NAME]</code> - Set your name in the chat")

@dp.message_handler(commands=["chatinfo"])
async def chat_info_command(message: types.Message):
	chat_id = message.get_args().strip()
	if not chat_id:
		await message.reply("Please provide a chat id.")
		return
	db_conn = sqlite3.connect("forum.db")
	db_cursor = db_conn.cursor()
	db_cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (chat_id,))
	chat_info = db_cursor.fetchone()
	db_conn.close()
	invite_link = f"https://t.me/anonforum_bot?start=joinchat_{chat_id}"
	await message.reply(f"Chat name: <b>{chat_info[2]}</b>\nChat ID: <code>{chat_info[0]}</code>\nNumber of users: <code>{chat_info[1]}</code>\nInvitation link: {invite_link}")

@dp.message_handler(commands=["createchat"])
async def create_chat_command(message: types.Message):
	chat_name = message.get_args().strip()
	if not chat_name:
		await message.reply("Please provide a name for the chat.")
		return
	chat_id = generate_chat_id()
	add_chat(chat_id, chat_name)
	invite_link = f"https://t.me/anonforum_bot?start=joinchat_{chat_id}"
	await message.reply(f"Chat <b>{chat_name}</b> created!\nInvitation link: {invite_link}")

@dp.message_handler(commands=["setname"])
async def set_name_command(message: types.Message):
	display_name = message.get_args().strip()
	db_conn = sqlite3.connect("forum.db")
	db_cursor = db_conn.cursor()
	db_cursor.execute("SELECT * FROM users_in_chats WHERE user_id = ?", (message.from_user.id,))
	user_info = db_cursor.fetchone()
	if not display_name:
		await message.reply(f"Please provide a new display name. Current one: <b>{user_info[2]}</b>.")
		return
	await message.reply(f"Your new display name <b>{display_name}</b> was set!")
	db_cursor.execute("UPDATE users_in_chats SET display_name = ? WHERE user_id = ?", (display_name, user_info[0],))
	db_conn.commit()
	users = get_users_in_chat(user_info[1])
	for user_id, _ in users:
		if user_id != message.from_user.id:
			await bot.send_message(user_id, f"💬: <b>{user_info[2]}</b> changed his/her name to <b>{display_name}</b>.")
	db_conn.close()

@dp.message_handler(commands=["leave"])
async def leave_chat_command(message: types.Message):
	db_conn = sqlite3.connect("forum.db")
	db_cursor = db_conn.cursor()
	db_cursor.execute("SELECT * FROM users_in_chats WHERE user_id = ?", (message.from_user.id,))
	user_info = db_cursor.fetchone()
	chat_id = user_info[1]
	display_name = user_info[2]
	db_cursor.execute("SELECT chat_name FROM chats WHERE chat_id = ?", (chat_id,))
	chat_name = db_cursor.fetchone()[0]
	users = get_users_in_chat(chat_id)
	for user_id, _ in users:
		if user_id != message.from_user.id:
			await bot.send_message(user_id, f"💬: <b>{display_name}</b> left the chat.")
	db_cursor.execute("UPDATE users_in_chats SET chat_id = NULL WHERE user_id = ?", (message.from_user.id,))
	db_cursor.execute("UPDATE chats SET number_of_users = number_of_users - 1 WHERE chat_id = ?", (chat_id,))
	db_conn.commit()
	db_conn.close()
	await message.reply(f"You have successfully left chat <b>{chat_name}</b>!")

@dp.message_handler(content_types=["any"])
async def content_message_handler(message: types.Message):
	db_conn = sqlite3.connect("forum.db")
	db_cursor = db_conn.cursor()
	db_cursor.execute("SELECT chat_id, display_name FROM users_in_chats WHERE user_id = ?", (message.from_user.id,))
	user_info = db_cursor.fetchone()
	db_conn.close()
	if user_info:
		chat_id, display_name = user_info
		users = get_users_in_chat(chat_id)
		for user_id, _ in users:
			if user_id != message.from_user.id:
				if message.text:
					content = f"👤 <b>{display_name}</b>:\n{message.text}"
					await bot.send_message(user_id, content)
				elif message.photo:
					caption = message.caption or ""
					await bot.send_photo(user_id, message.photo[-1].file_id, caption=f"👤 <b>{display_name}</b>:\n{caption}")
				elif message.video:
					caption = message.caption or ""
					await bot.send_video(user_id, message.video.file_id, caption=f"👤 <b>{display_name}</b>:\n{caption}")
				elif message.document:
					caption = message.caption or ""
					await bot.send_document(user_id, message.document.file_id, caption=f"👤 <b>{display_name}</b>:\n{caption}")
				elif message.audio:
					caption = message.caption or ""
					await bot.send_audio(user_id, message.audio.file_id, caption=f"👤 <b>{display_name}</b>:\n{caption}")
				elif message.voice:
					await bot.send_voice(user_id, message.voice.file_id, caption=f"👤 <b>{display_name} sent a voice message</b>")
				elif message.sticker:
					await bot.send_message(user_id, f"👤 <b>{display_name} sent a sticker</b>")
					await bot.send_sticker(user_id, message.sticker.file_id)
				elif message.video_note:
					await bot.send_message(user_id, f"👤 <b>{display_name} sent a video message</b>")
					await bot.send_video_note(user_id, message.video_note.file_id)
	else:
		await message.reply("You are not part of any chat. Use a valid invitation link to join.")

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
