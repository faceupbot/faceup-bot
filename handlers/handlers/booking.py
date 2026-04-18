from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SERVICES, ADMIN_ID
from database import create_booking

VISIT_TYPE = 1
DATETIME_INPUT = 2


async def booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🌿 Перший візит — 90 хв / 1000 грн", callback_data="visit_first")],
        [InlineKeyboardButton("✨ Повторний візит — 60 хв / 1000 грн", callback_data="visit_repeat")],
    ]
    await query.edit_message_text("Оберіть тип сеансу:", reply_markup=InlineKeyboardMarkup(keyboard))
    return VISIT_TYPE


async def visit_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    visit_key = query.data.replace("visit_", "")
    service = SERVICES[visit_key]
    context.user_data["visit_type"] = visit_key
    context.user_data["service"] = service
    await query.edit_message_text(
        f"Чудово! Ви обрали: *{service['name']}* ({service['duration']} хв)\n\n"
        f"Напишіть бажану дату та час.\nНаприклад: _15 липня о 14:00_",
        parse_mode="Markdown"
    )
    return DATETIME_INPUT


async def datetime_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    proposed = update.message.text
    context.user_data["proposed_datetime"] = proposed
    service = context.user_data["service"]
    keyboard = [
        [InlineKeyboardButton("✅ Підтвердити", callback_data="confirm_booking")],
        [InlineKeyboardButton("✏️ Змінити час", callback_data="book")],
    ]
    await update.message.reply_text(
        f"Перевірте ваш запит:\n\n📋 *{service['name']}* ({service['duration']} хв)\n"
        f"🗓 {proposed}\n💰 1000 грн\n\nВсе вірно?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return DATETIME_INPUT


async def confirm_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    visit_type = context.user_data.get("visit_type")
    proposed = context.user_data.get("proposed_datetime")
    service = context.user_data.get("service")
    booking_id = create_booking(user.id, user.username or "", user.full_name, visit_type, proposed)
    admin_keyboard = [[
        InlineKeyboardButton("✅ Підтвердити", callback_data=f"admin_confirm_{booking_id}_{user.id}"),
        InlineKeyboardButton("❌ Відхилити", callback_data=f"admin_decline_{booking_id}_{user.id}"),
    ]]
    await query.get_bot().send_message(
        chat_id=ADMIN_ID,
        text=f"📩 *Новий запит!*\n\n👤 {user.full_name}"
             f"{' (@' + user.username + ')' if user.username else ''}\n"
             f"📋 {service['name']} ({service['duration']} хв)\n🗓 {proposed}\n💰 1000 грн",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(admin_keyboard)
    )
    await query.edit_message_text(
        "✅ Ваш запит відправлено!\n\nЯ повідомлю вас, щойно майстер підтвердить час 🙏"
    )
