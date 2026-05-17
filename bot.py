import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

WORDS = [
    ("apple", "яблоко"), ("book", "книга"), ("cat", "кошка"),
    ("dog", "собака"), ("house", "дом"), ("water", "вода"),
    ("food", "еда"), ("friend", "друг"), ("love", "любовь"),
    ("time", "время"), ("money", "деньги"), ("work", "работа"),
    ("school", "школа"), ("family", "семья"), ("city", "город"),
    ("car", "машина"), ("phone", "телефон"), ("music", "музыка"),
    ("sun", "солнце"), ("moon", "луна"),
]

user_stats = {}

def get_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🃏 Учить слова", callback_data="flashcard")],
        [InlineKeyboardButton("📝 Тест (кнопки)", callback_data="test")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ])

def init_user(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {"correct": 0, "wrong": 0, "learned": [], "queue": []}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_user(user.id)
    context.user_data["mode"] = None
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nЯ помогу тебе учить английский!\n\nЧто будем делать?",
        reply_markup=get_menu_keyboard()
    )

async def next_flashcard(update, context, edit=True):
    user_id = update.effective_user.id
    init_user(user_id)

    if not user_stats[user_id]["queue"]:
        user_stats[user_id]["queue"] = list(range(len(WORDS)))
        random.shuffle(user_stats[user_id]["queue"])

    idx = user_stats[user_id]["queue"].pop(0)
    word, translation = WORDS[idx]
    context.user_data["current_word"] = word
    context.user_data["current_translation"] = translation
    context.user_data["mode"] = "flashcard"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👁 Показать перевод", callback_data="show_translation")],
        [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
    ])
    text = f"🃏 Напиши перевод слова или нажми кнопку:\n\n*{word.upper()}*"

    if edit:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    init_user(user_id)
    data = query.data

    if data == "menu":
        context.user_data["mode"] = None
        await query.edit_message_text("Главное меню:", reply_markup=get_menu_keyboard())

    elif data == "flashcard":
        await next_flashcard(update, context, edit=True)

    elif data == "show_translation":
        translation = context.user_data.get("current_translation", "?")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующее слово", callback_data="flashcard")],
            [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
        ])
        await query.edit_message_text(
            f"📖 Перевод: *{translation}*\n\nНапиши это слово чтобы запомнить, или жми дальше!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    elif data == "test":
        await next_test(update, context, edit=True)

    elif data == "next_test":
        await next_test(update, context, edit=True)

    elif data.startswith("answer_"):
        chosen = data.replace("answer_", "")
        correct = context.user_data.get("test_answer", "")
        word = context.user_data.get("test_word", "")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next_test")],
            [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
        ])
        if chosen == correct:
            user_stats[user_id]["correct"] += 1
            if word not in user_stats[user_id]["learned"]:
                user_stats[user_id]["learned"].append(word)
            text = f"✅ Правильно! *{word}* = {correct}"
        else:
            user_stats[user_id]["wrong"] += 1
            text = f"❌ Неправильно!\n*{word}* = {correct}\nТы выбрал: {chosen}"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "stats":
        s = user_stats[user_id]
        total = s["correct"] + s["wrong"]
        percent = int(s["correct"] / total * 100) if total > 0 else 0
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 В меню", callback_data="menu")]])
        await query.edit_message_text(
            f"📊 Твоя статистика:\n\n"
            f"✅ Правильных: {s['correct']}\n"
            f"❌ Неправильных: {s['wrong']}\n"
            f"🎯 Точность: {percent}%\n"
            f"📚 Изучено слов: {len(s['learned'])} из {len(WORDS)}",
            reply_markup=keyboard
        )

async def next_test(update, context, edit=True):
    user_id = update.effective_user.id
    init_user(user_id)

    if not user_stats[user_id]["queue"]:
        user_stats[user_id]["queue"] = list(range(len(WORDS)))
        random.shuffle(user_stats[user_id]["queue"])

    idx = user_stats[user_id]["queue"].pop(0)
    word, correct = WORDS[idx]
    wrong_options = [t for w, t in WORDS if t != correct]
    options = random.sample(wrong_options, 3) + [correct]
    random.shuffle(options)
    context.user_data["test_word"] = word
    context.user_data["test_answer"] = correct
    context.user_data["mode"] = "test"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(opt, callback_data=f"answer_{opt}")] for opt in options] +
        [[InlineKeyboardButton("🔙 В меню", callback_data="menu")]]
    )
    text = f"📝 Выбери перевод:\n\n*{word.upper()}*"
    if edit:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    mode = context.user_data.get("mode")
    text = update.message.text.strip().lower()

    if mode == "flashcard":
        correct = context.user_data.get("current_translation", "").lower()
        word = context.user_data.get("current_word", "")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующее слово", callback_data="flashcard")],
            [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
        ])
        if text == correct:
            user_stats[user_id]["correct"] += 1
            if word not in user_stats[user_id]["learned"]:
                user_stats[user_id]["learned"].append(word)
            await update.message.reply_text(
                f"✅ Правильно! *{word}* = {correct}",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            user_stats[user_id]["wrong"] += 1
            await update.message.reply_text(
                f"❌ Неправильно!\nПравильный ответ: *{correct}*\nТы написал: {text}",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
    else:
        await update.message.reply_text(
            "Нажми /start чтобы начать! 👇",
            reply_markup=get_menu_keyboard()
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
