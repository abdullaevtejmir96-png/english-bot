import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_stats:
        user_stats[user.id] = {"correct": 0, "wrong": 0, "learned": []}
    
    keyboard = [
        [InlineKeyboardButton("🃏 Учить слова", callback_data="flashcard")],
        [InlineKeyboardButton("📝 Тест", callback_data="test")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ]
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nЯ помогу тебе учить английский!\n\nЧто будем делать?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🃏 Учить слова", callback_data="flashcard")],
        [InlineKeyboardButton("📝 Тест", callback_data="test")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ]
    await update.callback_query.message.edit_text(
        "Главное меню — что будем делать?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def flashcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, translation = random.choice(WORDS)
    keyboard = [
        [InlineKeyboardButton("👁 Показать перевод", callback_data=f"show_{translation}")],
        [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
    ]
    await update.callback_query.message.edit_text(
        f"🃏 Как переводится:\n\n*{word.upper()}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translation = update.callback_query.data.replace("show_", "")
    keyboard = [
        [InlineKeyboardButton("➡️ Следующее слово", callback_data="flashcard")],
        [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
    ]
    await update.callback_query.message.edit_text(
        f"✅ Перевод: *{translation}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, correct = random.choice(WORDS)
    wrong_options = [t for w, t in WORDS if t != correct]
    options = random.sample(wrong_options, 3) + [correct]
    random.shuffle(options)
    
    context.user_data["test_word"] = word
    context.user_data["test_answer"] = correct
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"answer_{opt}")] for opt in options]
    keyboard.append([InlineKeyboardButton("🔙 В меню", callback_data="menu")])
    
    await update.callback_query.message.edit_text(
        f"📝 Выбери перевод слова:\n\n*{word.upper()}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {"correct": 0, "wrong": 0, "learned": []}
    
    chosen = update.callback_query.data.replace("answer_", "")
    correct = context.user_data.get("test_answer", "")
    word = context.user_data.get("test_word", "")
    
    keyboard = [
        [InlineKeyboardButton("➡️ Следующий вопрос", callback_data="test")],
        [InlineKeyboardButton("🔙 В меню", callback_data="menu")],
    ]
    
    if chosen == correct:
        user_stats[user_id]["correct"] += 1
        if word not in user_stats[user_id]["learned"]:
            user_stats[user_id]["learned"].append(word)
        text = f"✅ Правильно! *{word}* = {correct}"
    else:
        user_stats[user_id]["wrong"] += 1
        text = f"❌ Неправильно!\n*{word}* = {correct}\nТы выбрал: {chosen}"
    
    await update.callback_query.message.edit_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {"correct": 0, "wrong": 0, "learned": []}
    
    s = user_stats[user_id]
    total = s["correct"] + s["wrong"]
    percent = int(s["correct"] / total * 100) if total > 0 else 0
    
    keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data="menu")]]
    await update.callback_query.message.edit_text(
        f"📊 Твоя статистика:\n\n"
        f"✅ Правильных ответов: {s['correct']}\n"
        f"❌ Неправильных: {s['wrong']}\n"
        f"🎯 Точность: {percent}%\n"
        f"📚 Изучено слов: {len(s['learned'])}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    
    if data == "menu":
        await menu(update, context)
    elif data == "flashcard":
        await flashcard(update, context)
    elif data == "test":
        await test(update, context)
    elif data == "stats":
        await stats(update, context)
    elif data.startswith("show_"):
        await show_translation(update, context)
    elif data.startswith("answer_"):
        await check_answer(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
