# 🤖 AnonForum Bot

> **`🐍 Python`** **`🤖 Telegram Bot`** **`💬 Anonymous Chat`** **`🔒 Secure`**

A powerful anonymous forum bot for Telegram that allows users to create and join private chat rooms with custom display names. Built with aiogram and SQLite.

---

## ✨ Features

- **🎭 Anonymous Chatting**: Join chats with random display names
- **🔗 Private Chat Rooms**: Create custom-named chat rooms
- **📱 Multi-Format Support**: Text, photos, videos, documents, voice messages
- **👥 User Management**: Join/leave chats, change display names
- **📊 Chat Statistics**: View chat info and user counts
- **🔗 Invite System**: Generate unique invitation links

---

## 🚀 Quick Start

### 📋 Prerequisites
- **`🐍 Python 3.7+`**
- **`🤖 Telegram Bot Token`** (from [@BotFather](https://t.me/BotFather))

### 📥 Installation

1. **Clone the repository**
  ```bash
  git clone https://github.com/alas-m/Telegram-AnonForum.git
  cd Telegram-AnonForum
  ```

2. **Install dependencies**
   ```pip install aiogram sqlite3```
   
4. **Configure your bot**
   ```bash
   # config.py
    API = "YOUR_BOT_TOKEN_HERE"
   ```
5. **Run the bot**
   `python main.py `

# 💻 Usage
## 🎯 Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| /start | Start the bot | /start |
| /help | Show help menu | /help |
| /createchat | Create new chat | /createchat My Secret Group |
| /chatinfo | Get chat information | /chatinfo ABC123DEF |
| /setname | Change display name | /setname CyberGhost |
| /leave | Leave current chat | /leave |

# 🏗️ Project Structure
```
anonforum-bot/
├── 🤖 main.py              # Main bot application
├── ⚙️ config.py            # Bot configuration
├── 💾 database.db          # SQLite database
└── 💾 forum.db             # SQLite database
```

# 🎨 How It Works
1. Creating a Chat
   `/createchat Tech Lovers`

   ✅ Creates:
   - Unique chat ID (e.g., aBc123DeFg)
   - Invitation link: t.me/anonforum_bot?start=joinchat_aBc123DeFg

2. Joining a Chat
   User clicks invitation link → assigned random name: `Anonymous1234`

3. Chatting
  -All messages are relayed to chat members
  -Display names shown instead of real usernames
  -Support for all media types

4. Managing Identity
   `/setname CyberExplorer`
   Changes display name across the chat

# 🔧 Technical Details
  
## 🛠️ Built With
- `aiogram` - Async Telegram Bot API
- `SQLite3` - Lightweight database
- `Python 3.7+` - Core programming language

# 🛡️ Privacy & Security
- 🎭 Anonymous Display: Real identities hidden

- 🔐 Private Chats: Invite-only access

- 🗑️ Easy Exit: Leave anytime with `/leave`

- 💾 Local Storage: SQLite database for data persistence

# 📄 License
`⚖️ MIT License` - Feel free to use and modify for your projects.
