from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from analyzers.ukrf_analyzer import UKRFAnalyzer
from bot.keyboards import main_keyboard

analyzer = UKRFAnalyzer()

WELCOME_MESSAGE = (
    "👋 Добро пожаловать в UKRF_Analyzer — ваш интеллектуальный помощник в области юриспруденции.\n\n"
    "Бот помогает определить наличие/отсутствие нарушений законодательства РФ в тексте, "
    "а также дать рекомендации по исправлению.\n\n"
    "📌 Сервис находится в разработке — и мы будем благодарны за обратную связь!\n\n"
    "📋 Как пользоваться ботом:\n\n"
    "Нажмите клавишу \"📝 Текст\" и далее просто напишите мне текст для проверки.\n"
    "✅ Когда статья будет найдена, я покажу ее вместе с предупреждением о необходимости "
    "консультации специалиста.\n\n"
    "❓ Используйте \"🆘 Помощь\" для повторного показа инструкций\n\n"
    "🔄 Используйте \"📩 Обратная связь\" для связи с разработчиками\n"
    
)

HELP_MESSAGE = (
    "📋 Как пользоваться ботом:\n\n"
    "Нажмите клавишу \"📝 Текст\" и далее просто напишите мне текст для проверки.\n"
    "✅ Когда статья будет найдена, я покажу ее вместе с предупреждением о необходимости "
    "консультации специалиста.\n\n"
    "❓ Используйте \"🆘 Помощь\" для повторного показа инструкций\n\n"
    "🔄 Используйте \"📩 Обратная связь\" для связи с разработчиками\n"
)

FEEDBACK_MESSAGE = (
    "📩 Обратная связь:\n\n"
    "Разработчиками проекта являются студенты ИМКТ ДВФУ:\n"
    "• @iva_vyacheslav - разработка анализатора \n"
    "• @aristele - разработка и поддержка чат-бота \n\n"
    "Будем рады помочь и ответить на ваши вопросы!"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=main_keyboard())
    context.user_data.clear()
    context.user_data["waiting_for_text"] = False  # По умолчанию ввод заблокирован


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(FEEDBACK_MESSAGE)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == "📝 Текст":
        await update.message.reply_text("✍️ Введите текст для анализа:")
        context.user_data["waiting_for_text"] = True  # Разрешаем ввод
    elif user_text == "🆘 Помощь":
        await help_command(update, context)
    elif user_text == "📩 Обратная связь":
        await feedback(update, context)
    elif not context.user_data.get("waiting_for_text", False):
        await update.message.reply_text(
            "⚠️ Пожалуйста, сначала нажмите кнопку **'📝 Текст'**, чтобы начать анализ."
        )
        return
    else:
        await update.message.chat.send_action(action="typing")
        analysis_result = analyzer.analyze_text(user_text)
        response = f"🔍 Результат анализа:\n\n{analysis_result}\n\n⚠️ Важно: Данный анализ не заменяет консультацию юриста."
        await update.message.reply_text(response)
        context.user_data["waiting_for_text"] = False  # Сбрасываем флаг

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("feedback", feedback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))