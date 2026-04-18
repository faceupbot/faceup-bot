import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from config import BOT_TOKEN
from handlers.start import start_handler
from handlers.booking import (
    booking_handler, visit_type_handler, datetime_input_handler,
    confirm_booking_handler, VISIT_TYPE, DATETIME_INPUT
)
from handlers.admin import admin_confirm_handler, admin_decline_handler
from handlers.my_bookings import my_bookings_handler, cancel_booking_handler
from handlers.faq import faq_handler, faq_answer_handler
from database import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    booking_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(booking_handler, pattern="^book$")],
        states={
            VISIT_TYPE: [CallbackQueryHandler(visit_type_handler, pattern="^visit_")],
            DATETIME_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, datetime_input_handler)],
        },
        fallbacks=[CommandHandler("start", start_handler)],
    )

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(booking_conv)
    app.add_handler(CallbackQueryHandler(confirm_booking_handler, pattern="^confirm_booking$"))
    app.add_handler(CallbackQueryHandler(admin_confirm_handler, pattern="^admin_confirm_"))
    app.add_handler(CallbackQueryHandler(admin_decline_handler, pattern="^admin_decline_"))
    app.add_handler(CallbackQueryHandler(my_bookings_handler, pattern="^my_bookings$"))
    app.add_handler(CallbackQueryHandler(cancel_booking_handler, pattern="^cancel_booking_"))
    app.add_handler(CallbackQueryHandler(faq_handler, pattern="^faq$"))
    app.add_handler(CallbackQueryHandler(faq_answer_handler, pattern="^faq_"))

    app.run_polling()

if __name__ == "__main__":
    main()
