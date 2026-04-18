from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Записатися", callback_data="book")],
        [InlineKeyboardButton("📋 Мої записи", callback_data="my_bookings")],
        [InlineKeyboardButton("❓ Про метод Face Up™", callback_data="faq")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Вітаю! 👋\n\n"
        "Я бот-помічник майстра масажу обличчя Face Up™.\n\n"
        "Тут ви можете:\n"
        "• записатися на сеанс\n"
        "• дізнатися більше про метод\n"
        "• переглянути або скасувати свій запис\n\n"
        "Що вас цікавить?"
    )

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
