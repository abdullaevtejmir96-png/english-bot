import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

# ===== ГРАММАТИКА =====
GRAMMAR_RULES = [
    {
        "title": "Present Perfect vs Past Simple",
        "rule": "📗 *Present Perfect vs Past Simple*\n\n"
                "✅ *Present Perfect* — действие связано с настоящим:\n"
                "• I have lost my keys. (они всё ещё потеряны)\n"
                "• She has lived here for 5 years. (живёт до сих пор)\n\n"
                "✅ *Past Simple* — действие завершено в прошлом:\n"
                "• I lost my keys yesterday.\n"
                "• She lived in Paris in 2010.\n\n"
                "⚠️ *Ключевые слова:*\n"
                "PP: already, yet, just, ever, never, for, since\n"
                "PS: yesterday, ago, last year, in 2010",
        "homework": "📝 *Домашнее задание:*\n\nНапиши 5 предложений о своей жизни используя Present Perfect и 5 — используя Past Simple.\n\nПример:\n• I have never been to London.\n• I visited Moscow last summer.",
        "questions": [
            {"q": "I ___ my homework already.", "options": ["did", "have done", "do", "done"], "a": "have done", "exp": "already → Present Perfect"},
            {"q": "She ___ to Paris in 2019.", "options": ["has gone", "went", "goes", "have gone"], "a": "went", "exp": "in 2019 — конкретная дата → Past Simple"},
            {"q": "They ___ here for 10 years.", "options": ["lived", "live", "have lived", "are living"], "a": "have lived", "exp": "for + незавершённый период → Present Perfect"},
            {"q": "___ you ever tried sushi?", "options": ["Did", "Do", "Have", "Are"], "a": "Have", "exp": "ever → Present Perfect"},
        ]
    },
    {
        "title": "Conditionals (1, 2, 3)",
        "rule": "📗 *Условные предложения (Conditionals)*\n\n"
                "✅ *1st Conditional* — реальное будущее:\n"
                "If + Present Simple → will + infinitive\n"
                "• If it rains, I will stay home.\n\n"
                "✅ *2nd Conditional* — нереальное настоящее:\n"
                "If + Past Simple → would + infinitive\n"
                "• If I were rich, I would travel the world.\n\n"
                "✅ *3rd Conditional* — нереальное прошлое:\n"
                "If + Past Perfect → would have + past participle\n"
                "• If I had studied, I would have passed.",
        "homework": "📝 *Домашнее задание:*\n\nЗакончи предложения:\n1. If I win the lottery, I will...\n2. If I were a teacher, I would...\n3. If I had woken up earlier, I would have...",
        "questions": [
            {"q": "If it ___ tomorrow, we'll cancel the trip.", "options": ["rained", "rains", "will rain", "rain"], "a": "rains", "exp": "1st Conditional: If + Present Simple"},
            {"q": "If I ___ you, I would apologise.", "options": ["am", "was", "were", "be"], "a": "were", "exp": "2nd Conditional: If I were you..."},
            {"q": "If she had studied harder, she ___ the exam.", "options": ["passed", "would pass", "would have passed", "had passed"], "a": "would have passed", "exp": "3rd Conditional: would have + past participle"},
            {"q": "If he ___ earlier, he wouldn't have missed the train.", "options": ["left", "leaves", "had left", "would leave"], "a": "had left", "exp": "3rd Conditional: If + Past Perfect"},
        ]
    },
    {
        "title": "Passive Voice",
        "rule": "📗 *Passive Voice (Страдательный залог)*\n\n"
                "✅ Структура: *be + past participle*\n\n"
                "• Present: The book is written.\n"
                "• Past: The book was written.\n"
                "• Future: The book will be written.\n"
                "• Present Perfect: The book has been written.\n\n"
                "✅ Когда использовать:\n"
                "• Когда не знаем кто сделал действие\n"
                "• В формальном/академическом тексте\n"
                "• Когда объект важнее субъекта",
        "homework": "📝 *Домашнее задание:*\n\nПереведи в пассивный залог:\n1. They build houses every year.\n2. Someone stole my bag.\n3. They have invented a new vaccine.",
        "questions": [
            {"q": "The Mona Lisa ___ by Leonardo da Vinci.", "options": ["painted", "was painted", "has painted", "is painting"], "a": "was painted", "exp": "Passive Past Simple: was + past participle"},
            {"q": "English ___ all over the world.", "options": ["speaks", "spoke", "is spoken", "has spoken"], "a": "is spoken", "exp": "Passive Present Simple: is + past participle"},
            {"q": "The results ___ tomorrow.", "options": ["will announce", "announce", "will be announced", "are announced"], "a": "will be announced", "exp": "Passive Future: will be + past participle"},
            {"q": "The bridge ___ for two years.", "options": ["is building", "has been built", "has been building", "built"], "a": "has been built", "exp": "Passive Present Perfect: has been + past participle"},
        ]
    },
]

# ===== СЛОВАРНЫЙ ЗАПАС =====
VOCAB_RULES = [
    {
        "title": "Коллокации (Collocations)",
        "rule": "📘 *Коллокации — устойчивые словосочетания*\n\n"
                "Коллокации нужно запоминать как единое целое!\n\n"
                "✅ *Make vs Do:*\n"
                "MAKE: make a decision, make an effort, make a mistake, make progress\n"
                "DO: do homework, do research, do damage, do well\n\n"
                "✅ *Have vs Take:*\n"
                "HAVE: have a shower, have a look, have fun, have a rest\n"
                "TAKE: take a photo, take part, take a break, take a risk",
        "homework": "📝 *Домашнее задание:*\n\nВыбери правильное слово (make/do/have/take):\n1. ___ a decision\n2. ___ research\n3. ___ a photo\n4. ___ fun\n5. ___ a mistake",
        "questions": [
            {"q": "She ___ a lot of progress this year.", "options": ["did", "made", "had", "took"], "a": "made", "exp": "make progress — коллокация"},
            {"q": "Can you ___ a look at my essay?", "options": ["make", "do", "have", "take"], "a": "have", "exp": "have a look — коллокация"},
            {"q": "He ___ part in the competition.", "options": ["made", "did", "had", "took"], "a": "took", "exp": "take part — коллокация"},
            {"q": "I need to ___ some research on this topic.", "options": ["make", "do", "have", "take"], "a": "do", "exp": "do research — коллокация"},
        ]
    },
    {
        "title": "Суффиксы и словообразование",
        "rule": "📘 *Словообразование (Word Formation)*\n\n"
                "✅ *Существительные:*\n"
                "-tion: education, information\n"
                "-ment: employment, achievement\n"
                "-ness: happiness, darkness\n"
                "-ity: creativity, curiosity\n\n"
                "✅ *Прилагательные:*\n"
                "-ful: beautiful, careful\n"
                "-less: careless, useless\n"
                "-able: reliable, comfortable\n"
                "-ive: creative, effective\n\n"
                "✅ *Наречия:*\n"
                "-ly: carefully, quickly, strongly",
        "homework": "📝 *Домашнее задание:*\n\nОбразуй слова:\n1. CREATE → ___ (noun)\n2. RELY → ___ (adjective)\n3. HAPPY → ___ (adverb)\n4. EMPLOY → ___ (noun)\n5. CARE → ___ (adjective, negative)",
        "questions": [
            {"q": "Her ___ (creative) was impressive.", "options": ["create", "creation", "creativity", "creative"], "a": "creativity", "exp": "-ity: creativity = творчество"},
            {"q": "He is very ___ (rely) person.", "options": ["rely", "relying", "reliance", "reliable"], "a": "reliable", "exp": "-able: reliable = надёжный"},
            {"q": "She spoke ___ (careful) about the topic.", "options": ["careful", "carefulness", "carefully", "careless"], "a": "carefully", "exp": "-ly для наречий: carefully"},
            {"q": "The ___ (employ) rate has risen.", "options": ["employ", "employee", "employment", "employable"], "a": "employment", "exp": "-ment: employment = занятость"},
        ]
    },
]

# ===== READING =====
READING_LESSONS = [
    {
        "title": "Стратегия чтения FCE",
        "rule": "📰 *Reading — Стратегия FCE*\n\n"
                "✅ *Part 5 (Multiple Choice):*\n"
                "1. Прочитай вопросы сначала\n"
                "2. Найди нужный абзац в тексте\n"
                "3. Ищи перефраз, не точные слова\n"
                "4. Исключай неправильные ответы\n\n"
                "✅ *Part 6 (Gapped text):*\n"
                "1. Читай текст целиком\n"
                "2. Обращай внимание на местоимения (he, she, they)\n"
                "3. Ищи связующие слова (however, moreover)\n\n"
                "✅ *Part 7 (Multiple matching):*\n"
                "1. Читай вопросы, подчёркивай ключевые слова\n"
                "2. Сканируй каждый текст быстро",
        "homework": "📝 *Домашнее задание:*\n\nПрочитай любую статью на английском (BBC, The Guardian) и:\n1. Выпиши 10 незнакомых слов\n2. Определи главную мысль каждого абзаца\n3. Перескажи статью в 3-4 предложениях",
        "questions": [
            {
                "text": "Social media has transformed communication. While it enables instant global connectivity, experts warn about addiction, privacy issues, and misinformation spreading rapidly online.",
                "q": "What is the main concern experts have about social media?",
                "options": ["It is too expensive", "It has negative effects", "It is not popular", "It is too slow"],
                "a": "It has negative effects",
                "exp": "Текст упоминает addiction, privacy issues, misinformation — всё негативные эффекты"
            },
            {
                "text": "The Amazon rainforest, often called 'the lungs of the Earth', produces 20% of the world's oxygen. However, deforestation threatens this vital ecosystem.",
                "q": "Why is the Amazon called 'the lungs of the Earth'?",
                "options": ["It is very large", "It produces oxygen", "It has many animals", "It is very old"],
                "a": "It produces oxygen",
                "exp": "Текст: 'produces 20% of the world's oxygen'"
            },
        ]
    },
]

# ===== WRITING =====
WRITING_LESSONS = [
    {
        "title": "Essay Writing",
        "rule": "✏️ *Essay Writing (FCE Part 1)*\n\n"
                "✅ *Структура (180-190 слов):*\n"
                "1. Introduction — представь тему (2-3 предложения)\n"
                "2. Body paragraph 1 — первый аргумент + пример\n"
                "3. Body paragraph 2 — второй аргумент + пример\n"
                "4. Conclusion — вывод, своё мнение\n\n"
                "✅ *Полезные фразы:*\n"
                "Intro: It is often argued that... / Nowadays...\n"
                "Adding: Furthermore, / Moreover, / In addition,\n"
                "Contrast: However, / Nevertheless, / On the other hand,\n"
                "Conclusion: In conclusion, / To sum up, / All in all,\n\n"
                "⚠️ *Не забудь:*\n"
                "• Формальный стиль (no contractions!)\n"
                "• Разнообразные структуры предложений\n"
                "• Проверь грамматику и орфографию",
        "homework": "📝 *Домашнее задание — Essay:*\n\n"
                    "Напиши эссе (180-190 слов) на тему:\n\n"
                    "*'Social media does more harm than good. Discuss.'*\n\n"
                    "Структура:\n"
                    "• Введение: что такое соцсети\n"
                    "• Абзац 1: вред (addiction, misinformation)\n"
                    "• Абзац 2: польза (communication, information)\n"
                    "• Заключение: твоё мнение",
        "questions": [
            {"q": "Which phrase is appropriate for a formal essay introduction?", "options": ["Nowadays, lots of people...", "Hey, so basically...", "I'm gonna talk about...", "Well, it's like..."], "a": "Nowadays, lots of people...", "exp": "Формальный стиль: Nowadays, lots of people... — подходит для эссе"},
            {"q": "Which linking word shows CONTRAST?", "options": ["Furthermore", "Moreover", "However", "In addition"], "a": "However", "exp": "However = однако — слово контраста"},
            {"q": "Which is NOT allowed in formal writing?", "options": ["Passive voice", "Contractions (don't)", "Complex sentences", "Formal vocabulary"], "a": "Contractions (don't)", "exp": "В формальном стиле: do not, cannot, will not (не don't, can't)"},
        ]
    },
]

# ===== SPEAKING =====
SPEAKING_TIPS = [
    "🗣 *Part 1 — Интервью (2 мин)*\n\n"
    "Отвечай развёрнуто! Используй структуру:\n"
    "*Ответ + причина + пример*\n\n"
    "❌ 'Do you like sport?' → 'Yes'\n"
    "✅ 'Yes, I really enjoy playing football because it keeps me fit. For example, I play twice a week with my friends.'\n\n"
    "💡 Полезные фразы:\n"
    "• As far as I'm concerned...\n"
    "• To be honest...\n"
    "• What I really enjoy is...",

    "🗣 *Part 2 — Long Turn (1 мин)*\n\n"
    "Описывай и *сравнивай* фотографии!\n\n"
    "✅ Структура:\n"
    "1. In the first photo I can see...\n"
    "2. In contrast, the second photo shows...\n"
    "3. Both photos seem to be about...\n"
    "4. Answering the question: I think...\n\n"
    "💡 Не молчи! Говори даже если не знаешь слова:\n"
    "• I'm not sure what it's called, but it looks like...\n"
    "• It seems to be some kind of...",

    "🗣 *Part 3 — Discussion (3 мин)*\n\n"
    "Обсуждай с партнёром, не монолог!\n\n"
    "✅ Полезные фразы:\n"
    "• What do you think about...?\n"
    "• I agree with you because...\n"
    "• That's a good point, but...\n"
    "• Shall we move on to...?\n"
    "• I see what you mean, however...\n\n"
    "⚠️ Не доминируй! Давай партнёру говорить тоже.",
]

# ===== LISTENING =====
LISTENING_TIPS = [
    "🎧 *FCE Listening — Общие советы*\n\n"
    "✅ ДО прослушивания:\n"
    "• Читай вопросы внимательно\n"
    "• Подчёркивай ключевые слова\n"
    "• Предугадывай тип ответа\n\n"
    "✅ ВО ВРЕМЯ:\n"
    "• Слушай контекст, не только слова\n"
    "• Обращай внимание на интонацию\n"
    "• Не паникуй если пропустил — слушай дальше\n\n"
    "✅ Опасные слова:\n"
    "• but, however, although → часто меняют смысл!\n"
    "• actually, in fact → исправление сказанного!",

    "🎧 *FCE Listening — 4 части*\n\n"
    "• *Part 1:* 8 коротких диалогов — MCQ (3 варианта)\n"
    "• *Part 2:* Монолог — заполни 10 пропусков\n"
    "• *Part 3:* 5 говорящих — сопоставь с вариантами\n"
    "• *Part 4:* Интервью — MCQ (7 вопросов)\n\n"
    "💡 *Совет для Part 2:*\n"
    "Пиши то что слышишь — проверка орфографии минимальная!\n\n"
    "💡 *Совет для Part 3:*\n"
    "Слушай сначала о чём говорит каждый, потом сопоставляй.",
]

user_data_store = {}

def init_user(user_id):
    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "correct": 0,
            "wrong": 0,
            "grammar_idx": 0,
            "vocab_idx": 0,
            "reading_idx": 0,
            "writing_idx": 0,
            "speaking_idx": 0,
            "listening_idx": 0,
            "current_questions": [],
            "q_index": 0,
            "section": None,
        }

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📗 Грамматика", callback_data="sec_grammar"),
         InlineKeyboardButton("📘 Словарный запас", callback_data="sec_vocab")],
        [InlineKeyboardButton("📰 Reading", callback_data="sec_reading"),
         InlineKeyboardButton("✏️ Writing", callback_data="sec_writing")],
        [InlineKeyboardButton("🗣 Speaking", callback_data="sec_speaking"),
         InlineKeyboardButton("🎧 Listening", callback_data="sec_listening")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_user(user.id)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"🎓 Добро пожаловать в *FCE B2 English Trainer*!\n\n"
        f"Здесь ты найдёшь:\n"
        f"• Объяснение правил\n"
        f"• Тесты для закрепления\n"
        f"• Домашние задания\n\n"
        f"Выбери раздел:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def show_lesson(query, context, lesson, section):
    user_id = query.from_user.id
    init_user(user_id)
    user_data_store[user_id]["section"] = section
    user_data_store[user_id]["current_questions"] = lesson["questions"]
    user_data_store[user_id]["q_index"] = 0

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Начать тест", callback_data="start_test")],
        [InlineKeyboardButton("🏠 Домашнее задание", callback_data="homework")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
    ])
    await query.edit_message_text(lesson["rule"], parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    init_user(user_id)
    data = query.data
    store = user_data_store[user_id]

    if data == "menu":
        store["section"] = None
        await query.edit_message_text("Выбери раздел:", reply_markup=get_main_menu())

    elif data == "sec_grammar":
        idx = store["grammar_idx"] % len(GRAMMAR_RULES)
        store["grammar_idx"] += 1
        await show_lesson(query, context, GRAMMAR_RULES[idx], "grammar")

    elif data == "sec_vocab":
        idx = store["vocab_idx"] % len(VOCAB_RULES)
        store["vocab_idx"] += 1
        await show_lesson(query, context, VOCAB_RULES[idx], "vocab")

    elif data == "sec_reading":
        idx = store["reading_idx"] % len(READING_LESSONS)
        store["reading_idx"] += 1
        await show_lesson(query, context, READING_LESSONS[idx], "reading")

    elif data == "sec_writing":
        idx = store["writing_idx"] % len(WRITING_LESSONS)
        store["writing_idx"] += 1
        await show_lesson(query, context, WRITING_LESSONS[idx], "writing")

    elif data == "sec_speaking":
        idx = store["speaking_idx"] % len(SPEAKING_TIPS)
        store["speaking_idx"] += 1
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_speaking")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.edit_message_text(SPEAKING_TIPS[idx], parse_mode="Markdown", reply_markup=keyboard)

    elif data == "sec_listening":
        idx = store["listening_idx"] % len(LISTENING_TIPS)
        store["listening_idx"] += 1
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_listening")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.edit_message_text(LISTENING_TIPS[idx], parse_mode="Markdown", reply_markup=keyboard)

    elif data == "homework":
        section = store["section"]
        hw = ""
        if section == "grammar":
            idx = (store["grammar_idx"] - 1) % len(GRAMMAR_RULES)
            hw = GRAMMAR_RULES[idx]["homework"]
        elif section == "vocab":
            idx = (store["vocab_idx"] - 1) % len(VOCAB_RULES)
            hw = VOCAB_RULES[idx]["homework"]
        elif section == "reading":
            idx = (store["reading_idx"] - 1) % len(READING_LESSONS)
            hw = READING_LESSONS[idx]["homework"]
        elif section == "writing":
            idx = (store["writing_idx"] - 1) % len(WRITING_LESSONS)
            hw = WRITING_LESSONS[idx]["homework"]

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data="start_test")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.edit_message_text(hw, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "start_test":
        questions = store["current_questions"]
        if not questions:
            await query.edit_message_text("Нет вопросов для этого раздела.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]]))
            return
        store["q_index"] = 0
        await send_question(query, store)

    elif data == "next_q":
        await send_question(query, store)

    elif data.startswith("ans_"):
        chosen = data[4:]
        questions = store["current_questions"]
        q_idx = store["q_index"] - 1
        if q_idx < 0 or q_idx >= len(questions):
            await query.edit_message_text("Ошибка. Начни заново.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]]))
            return

        q = questions[q_idx]
        correct = q["a"]
        exp = q["exp"]

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next_q")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])

        if chosen == correct:
            user_data_store[user_id]["correct"] += 1
            text = f"✅ *Правильно!*\n\n💡 {exp}"
        else:
            user_data_store[user_id]["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct}*\n\n💡 {exp}"

        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "stats":
        s = user_data_store[user_id]
        total = s["correct"] + s["wrong"]
        percent = int(s["correct"] / total * 100) if total > 0 else 0
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]])
        await query.edit_message_text(
            f"📊 *Твоя статистика:*\n\n"
            f"✅ Правильных: {s['correct']}\n"
            f"❌ Неправильных: {s['wrong']}\n"
            f"🎯 Точность: {percent}%\n\n"
            f"Продолжай заниматься! 💪",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

async def send_question(query, store):
    questions = store["current_questions"]
    q_idx = store["q_index"]

    if q_idx >= len(questions):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Пройти снова", callback_data="start_test")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.edit_message_text(
            "🎉 *Тест завершён!*\n\nОтличная работа! Не забудь выполнить домашнее задание!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return

    q = questions[q_idx]
    store["q_index"] += 1

    options = q["options"][:]
    random.shuffle(options)

    text = f"❓ *Вопрос {q_idx + 1}/{len(questions)}*\n\n"
    if "text" in q:
        text += f"📄 _{q['text']}_\n\n"
    text += q["q"]

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(opt, callback_data=f"ans_{opt}")] for opt in options] +
        [[InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]]
    )
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Используй кнопки для навигации! 👇\nНажми /start чтобы начать.",
        reply_markup=get_main_menu()
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("FCE Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
