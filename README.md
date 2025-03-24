# Telegram Bot

This project is a simple Telegram bot built using the aiogram library. It serves as a template for creating your own Telegram bots with basic functionality.

## Project Structure

```
telegram-bot
├── bot
│   ├── __init__.py
│   ├── handlers
│   │   └── __init__.py
│   ├── main.py
│   └── config.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telegram-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the bot, you need to set up your bot token. Open `bot/config.py` and replace the placeholder with your actual bot token.

## Running the Bot

To start the bot, run the following command:
```
python bot/main.py
```

## Contributing

Feel free to submit issues or pull requests to improve the bot or add new features.