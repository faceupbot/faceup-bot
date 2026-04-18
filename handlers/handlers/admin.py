from telegram import Update
from telegram.ext import ContextTypes
from database import get_booking_dict, update_booking_status
from config import SERVICES


async def admin_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, booking_id, client_id = query.data.split("_", 2)
    booking_id = int(booking_id)
    client_id = int(client_id)
    booking = get_booking_dict(booking_id)
    if not booking:
        await query.edit_message_text("⚠️ Запис не знайдено.")
        return
    update_booking_status(booking_id, "confirmed")
    service = SERVICES.get(booking["visit_type"], {})
    await query.get_bot().send_message(
        chat_id=client_id,
        text=(
            f"✅ *Ваш запис підтверджено!*\n\n"
            f"📋 {service.get('name', '')} ({service.get('duration', '')} хв)\n"
            f"🗓 {booking['proposed_datetime']}\n"
            f"💰 1000 грн\n\nЧекаємо на вас! 🌿"
        ),
        parse_mode="Markdown"
    )
    await query.edit_message_text(f"✅ Запис #{booking_id} підтверджено. Клієнта сповіщено.")


async def admin_decline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, booking_id, client_id = query.data.split("_", 2)
    booking_id = int(booking_id)
    client_id = int(client_id)
    update_booking_status(booking_id, "declined")
    await query.get_bot().send_message(
        chat_id=client_id,
        text=(
            "😔 На жаль, запропонований час зайнятий.\n\n"
            "Будь ласка, напишіть інший зручний час — "
            "скористайтесь кнопкою /start → Записатися 📅"
        )
    )
    await query.edit_message_text(f"❌ Запис #{booking_id} відхилено. Клієнта сповіщено.")
