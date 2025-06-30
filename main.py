import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from bot.handlers import setup_handlers
from telegram.ext import Application
from config.settings import settings

def main():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    setup_handlers(app)
    print("🟢 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()