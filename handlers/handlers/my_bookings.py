from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_active_bookings, update_booking_status
from config import SERVICES, ADMIN_ID

STATUS_LABELS = {
    "pending": "⏳ Очікує підтвердження",
    "confirmed": "✅ Підтверджено",
}

async def my_bookings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    bookings = get_user_active_bookings(user_id)
    if not bookings:
        keyboard = [[InlineKeyboardButton("📅 Записатися", callback_data="book")]]
        await query.edit_message_text("У вас немає активних записів.\n\nБажаєте записатися?", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    text = "📋 *Ваші записи:*\n\n"
    keyboard = []
    for b in bookings:
        service = SERVICES.get(b["visit_type"], {})
        status_label = STATUS_LABELS.get(b["status"], b["status"])
        text += f"🗓 {b['proposed_datetime']}\n   {service.get('name', '')} ({service.get('duration', '')} хв)\n   {status_label}\n\n"
        keyboard.append([InlineKeyboardButton(f"❌ Скасувати ({b['proposed_datetime']})", callback_data=f"cancel_booking_{b['id']}")])
    keyboard.append([InlineKeyboardButton("🏠 Головне меню", callback_data="start")])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def cancel_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    booking_id = int(query.data.replace("cancel_booking_", ""))
    update_booking_status(booking_id, "cancelled")
    user = query.from_user
    await query.get_bot().send_message(
        chat_id=ADMIN_ID,
        text=f"⚠️ *Клієнт скасував запис #{booking_id}*\n\n👤 {user.full_name}{' (@' + user.username + ')' if user.username else ''}",
        parse_mode="Markdown"
    )
    await query.edit_message_text("✅ Ваш запис скасовано.\n\nЯкщо захочете записатися знову — я тут 🙏\n\n/start")
