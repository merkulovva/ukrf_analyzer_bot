from telegram import ReplyKeyboardMarkup

def main_keyboard():
    keyboard = [
        ["📝 Текст", "🆘 Помощь"],
        ["📩 Обратная связь"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)