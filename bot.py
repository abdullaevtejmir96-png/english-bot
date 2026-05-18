import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

LESSONS = {
    "g0": {
        "rule": "📗 *Present Perfect vs Past Simple*\n\n✅ *Present Perfect* — действие связано с настоящим:\n• I have lost my keys.\n• She has lived here for 5 years.\n\n✅ *Past Simple* — действие завершено в прошлом:\n• I lost my keys yesterday.\n• She lived in Paris in 2010.\n\n⚠️ *Ключевые слова:*\nPP: already, yet, just, ever, never, for, since\nPS: yesterday, ago, last year, in 2010",
        "hw": "📝 *Домашнее задание:*\n\nНапиши 5 предложений используя Present Perfect и 5 — Past Simple.\n\nПример:\n• I have never been to London.\n• I visited Moscow last summer.",
        "q": [
            {"q": "I ___ my homework already.", "o": ["did", "have done", "do", "done"], "a": "have done", "e": "already → Present Perfect"},
            {"q": "She ___ to Paris in 2019.", "o": ["has gone", "went", "goes", "have gone"], "a": "went", "e": "in 2019 → Past Simple"},
            {"q": "They ___ here for 10 years.", "o": ["lived", "live", "have lived", "are living"], "a": "have lived", "e": "for + незавершённый период → Present Perfect"},
            {"q": "___ you ever tried sushi?", "o": ["Did", "Do", "Have", "Are"], "a": "Have", "e": "ever → Present Perfect"},
        ]
    },
    "g1": {
        "rule": "📗 *Conditionals*\n\n✅ *1st* — реальное будущее:\nIf + Present Simple → will\n• If it rains, I will stay home.\n\n✅ *2nd* — нереальное настоящее:\nIf + Past Simple → would\n• If I were rich, I would travel.\n\n✅ *3rd* — нереальное прошлое:\nIf + Past Perfect → would have\n• If I had studied, I would have passed.",
        "hw": "📝 *Домашнее задание:*\n\nЗакончи предложения:\n1. If I win the lottery, I will...\n2. If I were a teacher, I would...\n3. If I had woken up earlier, I would have...",
        "q": [
            {"q": "If it ___ tomorrow, we'll cancel the trip.", "o": ["rained", "rains", "will rain", "rain"], "a": "rains", "e": "1st Conditional: If + Present Simple"},
            {"q": "If I ___ you, I would apologise.", "o": ["am", "was", "were", "be"], "a": "were", "e": "2nd Conditional: If I were you..."},
            {"q": "If she had studied harder, she ___ the exam.", "o": ["passed", "would pass", "would have passed", "had passed"], "a": "would have passed", "e": "3rd Conditional: would have + past participle"},
            {"q": "If he ___ earlier, he wouldn't have missed the train.", "o": ["left", "leaves", "had left", "would leave"], "a": "had left", "e": "3rd Conditional: If + Past Perfect"},
        ]
    },
    "g2": {
        "rule": "📗 *Passive Voice*\n\n✅ Структура: *be + past participle*\n\n• Present: is written\n• Past: was written\n• Future: will be written\n• Present Perfect: has been written\n\n✅ Когда использовать:\n• Не знаем кто сделал действие\n• В формальном тексте",
        "hw": "📝 *Домашнее задание:*\n\nПереведи в пассивный залог:\n1. They build houses every year.\n2. Someone stole my bag.\n3. They have invented a new vaccine.",
        "q": [
            {"q": "The Mona Lisa ___ by Leonardo da Vinci.", "o": ["painted", "was painted", "has painted", "is painting"], "a": "was painted", "e": "Passive Past: was + past participle"},
            {"q": "English ___ all over the world.", "o": ["speaks", "spoke", "is spoken", "has spoken"], "a": "is spoken", "e": "Passive Present: is + past participle"},
            {"q": "The results ___ tomorrow.", "o": ["will announce", "announce", "will be announced", "are announced"], "a": "will be announced", "e": "Passive Future: will be + past participle"},
            {"q": "The bridge ___ for two years.", "o": ["is building", "has been built", "has been building", "built"], "a": "has been built", "e": "Passive Perfect: has been + past participle"},
        ]
    },
    "v0": {
        "rule": "📘 *Коллокации*\n\n✅ *Make vs Do:*\nMAKE: make a decision, make progress, make a mistake\nDO: do homework, do research, do well\n\n✅ *Have vs Take:*\nHAVE: have a look, have fun, have a rest\nTAKE: take a photo, take part, take a break",
        "hw": "📝 *Домашнее задание:*\n\nВыбери правильное слово:\n1. ___ a decision\n2. ___ research\n3. ___ a photo\n4. ___ fun\n5. ___ a mistake",
        "q": [
            {"q": "She ___ a lot of progress this year.", "o": ["did", "made", "had", "took"], "a": "made", "e": "make progress — коллокация"},
            {"q": "Can you ___ a look at my essay?", "o": ["make", "do", "have", "take"], "a": "have", "e": "have a look — коллокация"},
            {"q": "He ___ part in the competition.", "o": ["made", "did", "had", "took"], "a": "took", "e": "take part — коллокация"},
            {"q": "I need to ___ some research.", "o": ["make", "do", "have", "take"], "a": "do", "e": "do research — коллокация"},
        ]
    },
    "v1": {
        "rule": "📘 *Суффиксы*\n\n✅ *Существительные:*\n-tion: education\n-ment: employment\n-ness: happiness\n-ity: creativity\n\n✅ *Прилагательные:*\n-ful: beautiful\n-less: careless\n-able: reliable\n\n✅ *Наречия:*\n-ly: carefully",
        "hw": "📝 *Домашнее задание:*\n\nОбразуй слова:\n1. CREATE → ___ (noun)\n2. RELY → ___ (adjective)\n3. HAPPY → ___ (adverb)\n4. EMPLOY → ___ (noun)\n5. CARE → ___ (adjective, negative)",
        "q": [
            {"q": "Her ___ (creative) was impressive.", "o": ["create", "creation", "creativity", "creative"], "a": "creativity", "e": "-ity: creativity = творчество"},
            {"q": "He is a very ___ (rely) person.", "o": ["rely", "relying", "reliance", "reliable"], "a": "reliable", "e": "-able: reliable = надёжный"},
            {"q": "She spoke ___ (careful).", "o": ["careful", "carefulness", "carefully", "careless"], "a": "carefully", "e": "-ly для наречий"},
            {"q": "The ___ (employ) rate has risen.", "o": ["employ", "employee", "employment", "employable"], "a": "employment", "e": "-ment: employment = занятость"},
        ]
    },
    "r0": {
        "rule": "📰 *Reading — Стратегия FCE*\n\n✅ *Part 5:*\n1. Прочитай вопросы сначала\n2. Найди нужный абзац\n3. Ищи перефраз\n\n✅ *Part 6:*\n1. Читай текст целиком\n2. Следи за местоимениями\n\n✅ *Part 7:*\n1. Подчёркивай ключевые слова\n2. Сканируй текст быстро",
        "hw": "📝 *Домашнее задание:*\n\nПрочитай статью на английском (BBC):\n1. Выпиши 10 незнакомых слов\n2. Определи главную мысль каждого абзаца\n3. Перескажи в 3-4 предложениях",
        "q": [
            {"q": "Social media enables connectivity but experts warn about addiction and misinformation.\n\nWhat do experts warn about?", "o": ["High cost", "Negative effects", "Lack of users", "Slow speed"], "a": "Negative effects", "e": "Текст: addiction, misinformation — негативные эффекты"},
            {"q": "The Amazon produces 20% of world's oxygen. Deforestation threatens this ecosystem.\n\nWhy is the Amazon important?", "o": ["It is large", "It produces oxygen", "It has animals", "It is old"], "a": "It produces oxygen", "e": "Текст: 'produces 20% of world's oxygen'"},
        ]
    },
    "w0": {
        "rule": "✏️ *Essay Writing (FCE)*\n\n✅ *Структура (180-190 слов):*\n1. Introduction\n2. Body paragraph 1\n3. Body paragraph 2\n4. Conclusion\n\n✅ *Полезные фразы:*\nIntro: Nowadays... / It is argued that...\nAdding: Furthermore, / Moreover,\nContrast: However, / Nevertheless,\nConclusion: In conclusion, / To sum up,\n\n⚠️ Только формальный стиль!",
        "hw": "📝 *Домашнее задание:*\n\nНапиши эссе (180-190 слов):\n*'Social media does more harm than good.'*\n\n• Introduction\n• Para 1: вред\n• Para 2: польза\n• Conclusion",
        "q": [
            {"q": "Какая фраза подходит для введения?", "o": ["Nowadays, lots of people...", "Hey, basically...", "I'm gonna talk...", "Well, it's like..."], "a": "Nowadays, lots of people...", "e": "Формальный стиль: Nowadays..."},
            {"q": "Какое слово показывает КОНТРАСТ?", "o": ["Furthermore", "Moreover", "However", "In addition"], "a": "However", "e": "However = однако"},
            {"q": "Что НЕЛЬЗЯ в формальном тексте?", "o": ["Passive voice", "Сокращения (don't)", "Сложные предложения", "Формальная лексика"], "a": "Сокращения (don't)", "e": "Пиши: do not, cannot"},
        ]
    },
}

GRAMMAR_KEYS = ["g0", "g1", "g2"]
VOCAB_KEYS = ["v0", "v1"]
READING_KEYS = ["r0"]
WRITING_KEYS = ["w0"]

SPEAKING_TIPS = [
    "🗣 *Part 1 — Интервью*\n\nОтвечай развёрнуто!\n*Ответ + причина + пример*\n\n❌ 'Yes'\n✅ 'Yes, I enjoy football because it keeps me fit.'\n\n• As far as I'm concerned...\n• To be honest...",
    "🗣 *Part 2 — Long Turn*\n\nСравнивай фотографии!\n\n1. In the first photo I can see...\n2. In contrast, the second shows...\n3. Both photos seem to be about...",
    "🗣 *Part 3 — Discussion*\n\nОбсуждай с партнёром!\n\n• What do you think about...?\n• I agree because...\n• That's a good point, but...",
]

LISTENING_TIPS = [
    "🎧 *Listening — Советы*\n\n✅ ДО:\n• Читай вопросы\n• Подчёркивай ключевые слова\n\n✅ ВО ВРЕМЯ:\n• Слушай контекст\n• but, however → меняют смысл!\n• actually → исправление!",
    "🎧 *Listening — 4 части*\n\n• Part 1: 8 диалогов — MCQ\n• Part 2: Монолог — пропуски\n• Part 3: 5 говорящих — сопоставь\n• Part 4: Интервью — MCQ",
]

user_store = {}

def init_user(user_id):
    if user_id not in user_store:
        user_store[user_id] = {
            "correct": 0, "wrong": 0,
            "speaking_idx": 0, "listening_idx": 0,
        }

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📗 Грамматика", callback_data="sec_g"),
         InlineKeyboardButton("📘 Словарный запас", callback_data="sec_v")],
        [InlineKeyboardButton("📰 Reading", callback_data="sec_r"),
         InlineKeyboardButton("✏️ Writing", callback_data="sec_w")],
        [InlineKeyboardButton("🗣 Speaking", callback_data="sec_sp"),
         InlineKeyboardButton("🎧 Listening", callback_data="sec_li")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
    ])

def make_lesson_kb(lkey, qidx):
    # Изменили разделитель на двоеточие, чтобы избежать конфликтов
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Начать тест", callback_data=f"Q:{lkey}:{qidx}")],
        [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"HW:{lkey}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_user(user.id)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n🎓 *FCE B2 English Trainer*\n\nВыбери раздел:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def show_question(query, lkey, qidx, user_id):
    lesson = LESSONS[lkey]
    questions = lesson["q"]

    if qidx >= len(questions):
        await query.edit_message_text(
            "🎉 *Тест завершён! Отличная работа!*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Пройти снова", callback_data=f"Q:{lkey}:0")],
                [InlineKeyboardButton("🔙 Меню", callback_data="menu")],
            ])
        )
        return

    q = questions[qidx]
    opts = q["o"][:]
    random.shuffle(opts)
    text = f"❓ *Вопрос {qidx+1}/{len(questions)}*\n\n{q['q']}"

    # Используем ограничение maxsplit=3 для безопасности ответов
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(o, callback_data=f"A:{lkey}:{qidx}:{o}")] for o in opts] +
        [[InlineKeyboardButton("🔙 Меню", callback_data="menu")]]
    )
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    init_user(user_id)
    store = user_store[user_id]
    data = query.data

    if data == "menu":
        await query.edit_message_text("Выбери раздел:", reply_markup=get_main_menu())

    elif data == "sec_g":
        lkey = random.choice(GRAMMAR_KEYS)
        await query.edit_message_text(LESSONS[lkey]["rule"], parse_mode="Markdown", reply_markup=make_lesson_kb(lkey, 0))

    elif data == "sec_v":
        lkey = random.choice(VOCAB_KEYS)
        await query.edit_message_text(LESSONS[lkey]["rule"], parse_mode="Markdown", reply_markup=make_lesson_kb(lkey, 0))

    elif data == "sec_r":
        lkey = random.choice(READING_KEYS)
        await query.edit_message_text(LESSONS[lkey]["rule"], parse_mode="Markdown", reply_markup=make_lesson_kb(lkey, 0))

    elif data == "sec_w":
        lkey = random.choice(WRITING_KEYS)
        await query.edit_message_text(LESSONS[lkey]["rule"], parse_mode="Markdown", reply_markup=make_lesson_kb(lkey, 0))

    elif data == "sec_sp":
        idx = store["speaking_idx"] % len(SPEAKING_TIPS)
        store["speaking_idx"] += 1
        await query.edit_message_text(SPEAKING_TIPS[idx], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_sp")],
            [InlineKeyboardButton("🔙 Меню", callback_data="menu")],
        ]))

    elif data == "sec_li":
        idx = store["listening_idx"] % len(LISTENING_TIPS)
        store["listening_idx"] += 1
        await query.edit_message_text(LISTENING_TIPS[idx], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_li")],
            [InlineKeyboardButton("🔙 Меню", callback_data="menu")],
        ]))

    elif data.startswith("HW:"):
        lkey = data.split(":")[1]
        await query.edit_message_text(LESSONS[lkey]["hw"], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"Q:{lkey}:0")],
            [InlineKeyboardButton("🔙 Меню", callback_data="menu")],
        ]))

    elif data.startswith("Q:"):
        parts = data.split(":")
        lkey = parts[1]
        qidx = int(parts[2])
        await show_question(query, lkey, qidx, user_id)

    elif data.startswith("A:"):
        # Ограничиваем сплит до 3, чтобы текст ответа (parts[3]) не дробился, если в нем есть двоеточия
        parts = data.split(":", 3)
        lkey = parts[1]
        qidx = int(parts[2])
        chosen = parts[3]
        q = LESSONS[lkey]["q"][qidx]
        correct = q["a"]
        exp = q["e"]

        if chosen == correct:
            store["correct"] += 1
            text = f"✅ *Правильно!*\n\n💡 {exp}"
        else:
            store["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct}*\n\n💡 {exp}"

        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"Q:{lkey}:{qidx+1}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="menu")],
        ]))

    elif data == "stats":
        total = store["correct"] + store["wrong"]
        percent = int(store["correct"] / total * 100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 *Статистика:*\n\n✅ Правильных: {store['correct']}\n❌ Неправильных: {store['wrong']}\n🎯 Точность: {percent}%\n\n💪 Продолжай!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]])
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нажми /start чтобы начать! 👇")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
