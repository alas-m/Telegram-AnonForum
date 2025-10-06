import sqlite3
import random
import string

db_conn = sqlite3.connect("forum.db")
db_cursor = db_conn.cursor()

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS users_in_chats (
	user_id INTEGER PRIMARY KEY,
	chat_id TEXT,
	display_name TEXT
)
""")
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
	chat_id TEXT PRIMARY KEY,
	number_of_users INTEGER DEFAULT 0,
	chat_name TEXT
)
""")
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
	user_id INTEGER PRIMARY KEY,
	first_name TEXT,
	username TEXT
)
""")
db_conn.commit()

def create_user(user_id, first_name, username):
	db_cursor.execute(
		"INSERT OR REPLACE INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
		(user_id, first_name, username)
	)
	db_conn.commit()

def generate_chat_id():
	return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def add_user(user_id, chat_id, display_name):
	db_cursor.execute(
		"INSERT OR REPLACE INTO users_in_chats (user_id, chat_id, display_name) VALUES (?, ?, ?)",
		(user_id, chat_id, display_name)
	)
	db_conn.commit()

def add_chat(chat_id, chat_name):
	db_cursor.execute(
		"INSERT OR IGNORE INTO chats (chat_id, number_of_users, chat_name) VALUES (?, 0, ?)",
		(chat_id, chat_name)
	)
	db_conn.commit()

def update_chat_user_count(chat_id, increment=True):
	db_cursor.execute(
		"UPDATE chats SET number_of_users = number_of_users + ? WHERE chat_id = ?",
		(1 if increment else -1, chat_id)
	)
	db_conn.commit()

def get_chat_info(chat_id):
	db_cursor.execute("SELECT chat_name FROM chats WHERE chat_id = ?", (chat_id,))
	return db_cursor.fetchone()

def get_users_in_chat(chat_id):
	db_cursor.execute("SELECT user_id, display_name FROM users_in_chats WHERE chat_id = ?", (chat_id,))
	return db_cursor.fetchall()
