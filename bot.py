import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен берется из переменных окружения Railway, либо используется стандартный
TOKEN = os.environ.get("TOKEN", "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs")

# Общая база данных материалов уровней B1+ / B2
LESSONS = {
    "grammar": {
        "title": "📗 Grammar (Present Perfect vs Past Simple)",
        "rule": "📗 *Present Perfect vs Past Simple (B2)*\n\n✅ *Present Perfect* — связь с настоящим, результат или незавершенное время:\n• _I have lost my keys (I don't have them now)._\n• _She has lived here for 5 years (still lives here)._\n\n✅ *Past Simple* — действие полностью завершено в прошлом:\n• _I lost my keys yesterday._\n• _She lived in Paris in 2010 (doesn't live there now)._\n\n⚠️ *Маркеры времени:*\n• PP: already, yet, just, ever, never, for, since\n• PS: yesterday, ago, last year, in 2015",
        "hw": "📝 *Домашнее задание (Grammar):*\n\nРаскрой скобки и отправь преподавателю:\n1. I (not see) him since last Tuesday.\n2. In 2022, they (visit) London for the first time.\n3. (you / ever / try) baking traditional dumplings?",
        "q": [
            {"q": "I ___ my homework already.", "o": ["did", "have done", "do", "done"], "a": 1, "e": "already требует Present Perfect (have + V3)"},
            {"q": "She ___ to Paris in 2019.", "o": ["has gone", "went", "goes", "have gone"], "a": 1, "e": "указание точного времени в прошлом (in 2019) требует Past Simple"}
        ]
    },
    "use_of_english": {
        "title": "🔬 Use of English (Conditionals)",
        "rule": "🔬 *Conditionals (1st, 2nd, 3rd)*\n\n✅ *1st Conditional* (Реальное будущее):\nIf + Present Simple, will + V1\n• _If it rains, we will stay at home._\n\n✅ *2nd Conditional* (Нереальное настоящее):\nIf + Past Simple, would + V1\n• _If I had more time, I would learn Spanish (but I don't)._\n\n✅ *3rd Conditional* (Нереальное прошлое, сожаление):\nIf + Past Perfect, would have + V3\n• _If I had studied harder, I would have passed the exam._",
        "hw": "📝 *Домашнее задание (Use of English):*\n\nДопиши предложения в соответствующем типе условного наклонения:\n1. If I win the lottery tomorrow, I...\n2. If I were the President, I...\n3. If we hadn't missed the train yesterday, we...",
        "q": [
            {"q": "If it ___ tomorrow, we'll cancel the trip.", "o": ["rained", "rains", "will rain", "rain"], "a": 1, "e": "В 1st Conditional после If используется Present Simple"},
            {"q": "If I ___ you, I would apologise to her.", "o": ["am", "was", "were", "be"], "a": 2, "e": "В устойчивых советах 2nd Conditional используется 'If I were you'"}
        ]
    },
    "suffixes": {
        "title": "⚙️ Word Formation (Suffixes)",
        "rule": "⚙️ *Suffixes (B1+ / B2)*\n\n✅ *Noun Suffixes (Существительные):*\n• *-ment:* employment, development\n• *-tion / -sion:* education, decision\n• *-ness:* happiness, kindness\n• *-ity:* creativity, flexibility\n\n✅ *Adjective Suffixes (Прилагательные):*\n• *-ful* (наличие качества): beautiful, helpful\n• *-less* (отсутствие качества): homeless, careless\n• *-able / -ible:* reliable, sensible",
        "hw": "📝 *Домашнее задание (Suffixes):*\n\nОбразуй правильную форму слова из скобок:\n1. The (EMPLOY) rate has dropped this month.\n2. She is an exceptionally (CREATE) person.\n3. Don't be so (CARE)! You broke the vase.",
        "q": [
            {"q": "Her ___ (creative) surprised everyone.", "o": ["creativity", "creation", "createness", "creative"], "a": 0, "e": "Суффикс -ity образует абстрактные существительные от прилагательных"},
            {"q": "He is a very ___ (rely) business partner.", "o": ["rely", "reliance", "reliable", "relyable"], "a": 2, "e": "Суффикс -able образует прилагательное со значением 'надежный'"}
        ]
    },
    "vocabulary": {
        "title": "📘 Vocabulary (Make vs Do)",
        "rule": "📘 *Vocabulary Collocations: Make vs Do*\n\n✅ *Используй MAKE, когда создаешь что-то новое или принимаешь решения:*\n• make a decision, make a mistake, make progress, make a phone call, make money.\n\n✅ *Используй DO для повседневных дел, работы или обязанностей:*\n• do homework, do research, do business, do housework, do sport, do your best.",
        "hw": "📝 *Домашнее задание (Vocabulary):*\n\nВставь MAKE или DO в правильной форме:\n1. I need to ___ a quick phone call.\n2. Have you ___ your English homework yet?\n3. It's difficult to ___ a choice under pressure.",
        "q": [
            {"q": "She ___ a lot of progress in English this term.", "o": ["did", "made", "had", "took"], "a": 1, "e": "Progress всегда сочетается с глаголом 'make'"},
            {"q": "I have to ___ some scientific research now.", "o": ["make", "do", "take", "give"], "a": 1, "e": "Research (исследование) сочетается с глаголом 'do'"}
        ]
    },
    "reading": {
        "title": "📰 Reading (FCE Strategy)",
        "rule": "📰 *Reading — Стратегия экзамена B2*\n\n✅ *Skimming (Просмотровое чтение):* Быстро пробегись глазами по тексту, чтобы понять общую тему и структуру. Не цепляйся за незнакомые слова.\n\n✅ *Scanning (Поисковое чтение):* Ищи в тексте конкретные ключевые слова, даты или имена из вопроса.\n\n⚠️ *Ловушка:* Никогда не выбирай ответ только потому, что в нем есть то же самое слово, что и в тексте. Ищи *синонимы и перифраз*!",
        "hw": "📝 *Домашнее задание (Reading):*\n\nНайди любую статью на английском (например, BBC / Сulture) уровня B2. Выпиши 7 новых фраз и составь краткий пересказ текста (5-6 предложений).",
        "q": [
            {"q": "Text: 'The Amazon produces 20% of the world's oxygen. Deforestation threatens this area.'\n\nQuestion: Why is the Amazon critical?", "o": ["It is under threat", "It generates oxygen", "It has unique animals", "It is old"], "a": 1, "e": "'Produces oxygen' перефразировано в вопросе как 'generates oxygen'"}
        ]
    },
    "listening": {
        "title": "🎧 Listening Tips",
        "rule": "🎧 *Listening — Разбор ловушек*\n\n1. *Дистракторы (Отвлекающие факторы):* В аудировании спикер часто упоминает *все* варианты ответа из теста, но правильным будет только один. \n2. *Следи за союзами:* Слова `but`, `however`, `actually`, `in fact` полностью меняют смысл сказанного секунду назад!\n\n💡 *Совет:* Используй первые 45 секунд до начала записи, чтобы подчеркнуть ключевые слова в вопросах.",
        "hw": "📝 *Домашнее задание (Listening):*\n\nПослушай любой подкаст (например, 6 Minute English от BBC). Запиши основные тезисы и выпиши 5 выражений, которые использовал спикер для выражения согласия/несогласия.",
        "q": [
            {"q": "Speaker: 'I planned to go by train, but my friend offered me a lift, so we drove.'\n\nHow did he travel?", "o": ["By train", "By car", "On foot", "By bus"], "a": 1, "e": "'Offered a lift, so we drove' означает поездку на машине (By car)"}
        ]
    },
    "speaking": {
        "title": "🗣 Speaking Part",
        "rule": "🗣 *Speaking Part 2 (FCE) — Сравнение фото*\n\nТебе даются 2 фотографии. Твоя задача — говорить 1 минуту, сравнивая их и отвечая на вопрос.\n\n✅ *Шаблон ответа (Полезные фразы):*\n• _Both pictures show people who are..._\n• _In the first photo... whereas in the second one..._\n• _One obvious difference is that..._\n• _They might be feeling tired because..._ (Строим предположения: must be, might be, looks like)",
        "hw": "📝 *Домашнее задание (Speaking):*\n\nНайди любые 2 картинки людей за работой. Запиши голосовое сообщение на 1.5 минуты, сравнивая их, используя фразы из правила.",
        "q": [
            {"q": "Какая фраза НЕ подходит для сравнения картинок?", "o": ["In contrast to...", "On the other hand...", "As far as I'm concerned...", "First of all, I can see a cat."], "a": 3, "e": "Простое перечисление объектов без сравнения не выполняет задачу Speaking Part 2"}
        ]
    },
    "writing": {
        "title": "✏️ Writing (Essay)",
        "rule": "✏️ *Writing — Структура Эссе B2*\n\nЭссе должно состоять из 140–190 слов и иметь строго формальный стиль.\n\n📐 *Структура:* \n1. *Introduction:* Введение, перефраз темы.\n2. *Body 1:* Аргумент №1 (из задания).\n3. *Body 2:* Аргумент №2 (из задания).\n4. *Body 3:* Твой собственный аргумент №3.\n5. *Conclusion:* Заключение, четкое подведение итогов.\n\n⚠️ *Запрещено:* Сокращения (_don't, can't_ — пиши _do not, cannot_) и разговорные слова (_slang, guys_).",
        "hw": "📝 *Домашнее задание (Writing):*\n\nНапиши эссе на тему: *'Should team sports be compulsory at school?'* (140-190 слов). Используй формальные линкеры: _Furthermore, However, In conclusion_.",
        "q": [
            {"q": "Какое выражение допустимо в формальном эссе?", "o": ["What's up guys", "Furthermore, it is believed", "I don't think that", "To my mind, it's cool"], "a": 1, "e": "'Furthermore, it is believed' — идеальный вводный оборот для формального стиля"}
        ]
    }
}

user_store = {}

def init_user(user_id):
    if user_id not in user_store:
        user_store[user_id] = {"correct": 0, "wrong": 0}

def get_main_menu():
    keyboard = []
    # Динамически собираем меню из всех имеющихся разделов по парам
    keys = list(LESSONS.keys())
    for i in range(0, len(keys), 2):
        row = [InlineKeyboardButton(LESSONS[keys[i]]["title"], callback_data=f"sec:{keys[i]}")]
        if i + 1 < len(keys):
            row.append(InlineKeyboardButton(LESSONS[keys[i+1]]["title"], callback_data=f"sec:{keys[i+1]}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📊 Моя статистика", callback_data="stats")])
    return InlineKeyboardMarkup(keyboard)

def get_lesson_menu(lkey):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Начать тест", callback_data=f"test:{lkey}:0")],
        [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"hw:{lkey}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\n\n"
        f"Добро пожаловать в тренажер *English B1+ / B2 (FCE)*.\n"
        f"Здесь ты сможешь выучить правила, пройти тесты и закрепить знания на практике.\n\n"
        f"Выбери интересующий раздел ниже:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def show_question(query, lkey, qidx):
    lesson = LESSONS[lkey]
    questions = lesson["q"]

    if qidx >= len(questions):
        await query.edit_message_text(
            "🎉 *Вы прошли все вопросы в этом разделе!* Отличная работа.\nМожешь выбрать другой предмет или повторить этот.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Пройти тест заново", callback_data=f"test:{lkey}:0")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]
            ])
        )
        return

    q_data = questions[qidx]
    
    # Чтобы не портить оригинальный массив, делаем копию вариантов с индексами
    options_with_idx = list(enumerate(q_data["o"]))
    random.shuffle(options_with_idx)

    text = f"📝 *Раздел:* {lesson['title']}\n" \
           f"❓ *Вопрос {qidx + 1} из {len(questions)}:*\n\n" \
           f"{q_data['q']}"

    # Передаем только ИНДЕКС ответа, данные кнопки будут ультра-короткими и не вызовут ошибку
    keyboard = []
    for idx, option_text in options_with_idx:
        keyboard.append([InlineKeyboardButton(option_text, callback_data=f"ans:{lkey}:{qidx}:{idx}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Прервать и выйти в меню", callback_data="menu")])
    
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    init_user(user_id)
    data = query.data

    if data == "menu":
        await query.edit_message_text(
            "Выбери раздел для изучения английского уровня B1+/B2:", 
            reply_markup=get_main_menu()
        )

    elif data.startswith("sec:"):
        lkey = data.split(":")[1]
        lesson = LESSONS[lkey]
        await query.edit_message_text(
            lesson["rule"], 
            parse_mode="Markdown", 
            reply_markup=get_lesson_menu(lkey)
        )

    elif data.startswith("hw:"):
        lkey = data.split(":")[1]
        lesson = LESSONS[lkey]
        await query.edit_message_text(
            lesson["hw"], 
            parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Начать тест по теме", callback_data=f"test:{lkey}:0")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]
            ])
        )

    elif data.startswith("test:"):
        _, lkey, qidx_str = data.split(":")
        await show_question(query, lkey, int(qidx_str))

    elif data.startswith("ans:"):
        _, lkey, qidx_str, chosen_idx_str = data.split(":")
        qidx = int(qidx_str)
        chosen_idx = int(chosen_idx_str)
        
        q_data = LESSONS[lkey]["q"][qidx]
        correct_idx = q_data["a"]
        explanation = q_data["e"]

        if chosen_idx == correct_idx:
            user_store[user_id]["correct"] += 1
            result_text = f"✅ *Правильно!*\n\n💡 {explanation}"
        else:
            user_store[user_id]["wrong"] += 1
            correct_text = q_data["o"][correct_idx]
            result_text = f"❌ *Неверно!*\n\nПравильный ответ: `{correct_text}`\n\n💡 {explanation}"

        await query.edit_message_text(
            result_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"test:{lkey}:{qidx + 1}")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]
            ])
        )

    elif data == "stats":
        stats = user_store[user_id]
        total = stats["correct"] + stats["wrong"]
        accuracy = int((stats["correct"] / total) * 100) if total > 0 else 0
        
        text = f"📊 *Твоя личная статистика:*\n\n" \
               f"✅ Решено верно: {stats['correct']}\n" \
               f"❌ Ошибок: {stats['wrong']}\n" \
               f"🎯 Общая точность: {accuracy}%\n\n" \
               f"Отличный способ готовиться к экзамену FCE B2! Продолжай в том же духе!"
        
        await query.edit_message_text(
            text, 
            parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]])
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, используй кнопки меню или введи команду /start 📝")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("Бот успешно инициализирован и запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()я
