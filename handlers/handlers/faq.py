
import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ANTHROPIC_API_KEY

FAQ_QUESTIONS = {
    "what": "Що таке Face Up™?",
    "who": "Кому підходить масаж?",
    "prepare": "Як підготуватися до сеансу?",
    "how_many": "Скільки сеансів потрібно?",
    "result": "Які результати очікувати?",
}

SYSTEM_PROMPT = """Ти — помічник майстра масажу обличчя Face Up™.
Відповідай коротко, тепло і по суті, українською мовою.
Face Up™ — метод масажу обличчя, що поєднує остеопатію та психосоматику.
Сеанс: 90 хв (перший візит) або 60 хв (повторний). Ціна: 1000 грн.
Не давай медичних рекомендацій."""

async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(label, callback_data=f"faq_{key}")]
        for key, label in FAQ_QUESTIONS.items()
    ]
    keyboard.append([InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu")])
    await query.edit_message_text(
        "❓ *Питання про метод*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def faq_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("faq_", "")
    question = FAQ_QUESTIONS.get(key, "")
    if not question:
        return
    await query.edit_message_text("⏳ Шукаю відповідь...")
    try:
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        message = await client.messages.create(
            model="claude-opus-4-6",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}]
        )
        answer = message.content[0].text
    except Exception as e:
        answer = "Наразі не можу відповісти. Зверніться до майстра 🙏"
    keyboard = [
        [InlineKeyboardButton("⬅️ Інші питання", callback_data="faq")],
        [InlineKeyboardButton("📅 Записатися", callback_data="book")]
    ]
    await query.edit_message_text(
        f"*{question}*\n\n{answer}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
