import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

GRAMMAR_RULES = [
    {
        "title": "Present Perfect vs Past Simple",
        "rule": "📗 *Present Perfect vs Past Simple*\n\n✅ *Present Perfect* — действие связано с настоящим:\n• I have lost my keys.\n• She has lived here for 5 years.\n\n✅ *Past Simple* — действие завершено в прошлом:\n• I lost my keys yesterday.\n• She lived in Paris in 2010.\n\n⚠️ *Ключевые слова:*\nPP: already, yet, just, ever, never, for, since\nPS: yesterday, ago, last year, in 2010",
        "homework": "📝 *Домашнее задание:*\n\nНапиши 5 предложений используя Present Perfect и 5 — Past Simple.\n\nПример:\n• I have never been to London.\n• I visited Moscow last summer.",
        "questions": [
            {"q": "I ___ my homework already.", "options": ["did", "have done", "do", "done"], "a": "have done", "exp": "already → Present Perfect"},
            {"q": "She ___ to Paris in 2019.", "options": ["has gone", "went", "goes", "have gone"], "a": "went", "exp": "in 2019 — конкретная дата → Past Simple"},
            {"q": "They ___ here for 10 years.", "options": ["lived", "live", "have lived", "are living"], "a": "have lived", "exp": "for + незавершённый период → Present Perfect"},
            {"q": "___ you ever tried sushi?", "options": ["Did", "Do", "Have", "Are"], "a": "Have", "exp": "ever → Present Perfect"},
        ]
    },
    {
        "title": "Conditionals",
        "rule": "📗 *Условные предложения (Conditionals)*\n\n✅ *1st Conditional* — реальное будущее:\nIf + Present Simple → will + infinitive\n• If it rains, I will stay home.\n\n✅ *2nd Conditional* — нереальное настоящее:\nIf + Past Simple → would + infinitive\n• If I were rich, I would travel the world.\n\n✅ *3rd Conditional* — нереальное прошлое:\nIf + Past Perfect → would have + past participle\n• If I had studied, I would have passed.",
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
        "rule": "📗 *Passive Voice (Страдательный залог)*\n\n✅ Структура: *be + past participle*\n\n• Present: The book is written.\n• Past: The book was written.\n• Future: The book will be written.\n• Present Perfect: The book has been written.\n\n✅ Когда использовать:\n• Когда не знаем кто сделал действие\n• В формальном тексте\n• Когда объект важнее субъекта",
        "homework": "📝 *Домашнее задание:*\n\nПереведи в пассивный залог:\n1. They build houses every year.\n2. Someone stole my bag.\n3. They have invented a new vaccine.",
        "questions": [
            {"q": "The Mona Lisa ___ by Leonardo da Vinci.", "options": ["painted", "was painted", "has painted", "is painting"], "a": "was painted", "exp": "Passive Past Simple: was + past participle"},
            {"q": "English ___ all over the world.", "options": ["speaks", "spoke", "is spoken", "has spoken"], "a": "is spoken", "exp": "Passive Present Simple: is + past participle"},
            {"q": "The results ___ tomorrow.", "options": ["will announce", "announce", "will be announced", "are announced"], "a": "will be announced", "exp": "Passive Future: will be + past participle"},
            {"q": "The bridge ___ for two years.", "options": ["is building", "has been built", "has been building", "built"], "a": "has been built", "exp": "Passive Present Perfect: has been + past participle"},
        ]
    },
]

VOCAB_RULES = [
    {
        "title": "Коллокации",
        "rule": "📘 *Коллокации — устойчивые словосочетания*\n\n✅ *Make vs Do:*\nMAKE: make a decision, make an effort, make a mistake, make progress\nDO: do homework, do research, do damage, do well\n\n✅ *Have vs Take:*\nHAVE: have a shower, have a look, have fun, have a rest\nTAKE: take a photo, take part, take a break, take a risk",
        "homework": "📝 *Домашнее задание:*\n\nВыбери правильное слово:\n1. ___ a decision\n2. ___ research\n3. ___ a photo\n4. ___ fun\n5. ___ a mistake",
        "questions": [
            {"q": "She ___ a lot of progress this year.", "options": ["did", "made", "had", "took"], "a": "made", "exp": "make progress — коллокация"},
            {"q": "Can you ___ a look at my essay?", "options": ["make", "do", "have", "take"], "a": "have", "exp": "have a look — коллокация"},
            {"q": "He ___ part in the competition.", "options": ["made", "did", "had", "took"], "a": "took", "exp": "take part — коллокация"},
            {"q": "I need to ___ some research.", "options": ["make", "do", "have", "take"], "a": "do", "exp": "do research — коллокация"},
        ]
    },
    {
        "title": "Суффиксы",
        "rule": "📘 *Словообразование (Word Formation)*\n\n✅ *Существительные:*\n-tion: education, information\n-ment: employment, achievement\n-ness: happiness, darkness\n-ity: creativity, curiosity\n\n✅ *Прилагательные:*\n-ful: beautiful, careful\n-less: careless, useless\n-able: reliable, comfortable\n\n✅ *Наречия:*\n-ly: carefully, quickly",
        "homework": "📝 *Домашнее задание:*\n\nОбразуй слова:\n1. CREATE → ___ (noun)\n2. RELY → ___ (adjective)\n3. HAPPY → ___ (adverb)\n4. EMPLOY → ___ (noun)\n5. CARE → ___ (adjective, negative)",
        "questions": [
            {"q": "Her ___ (creative) was impressive.", "options": ["create", "creation", "creativity", "creative"], "a": "creativity", "exp": "-ity: creativity = творчество"},
            {"q": "He is a very ___ (rely) person.", "options": ["rely", "relying", "reliance", "reliable"], "a": "reliable", "exp": "-able: reliable = надёжный"},
            {"q": "She spoke ___ (careful) about the topic.", "options": ["careful", "carefulness", "carefully", "careless"], "a": "carefully", "exp": "-ly для наречий: carefully"},
            {"q": "The ___ (employ) rate has risen.", "options": ["employ", "employee", "employment", "employable"], "a": "employment", "exp": "-ment: employment = занятость"},
        ]
    },
]

READING_LESSONS = [
    {
        "title": "Стратегия чтения FCE",
        "rule": "📰 *Reading — Стратегия FCE*\n\n✅ *Part 5 (Multiple Choice):*\n1. Прочитай вопросы сначала\n2. Найди нужный абзац\n3. Ищи перефраз, не точные слова\n4. Исключай неправильные ответы\n\n✅ *Part 6 (Gapped text):*\n1. Читай текст целиком\n2. Обращай внимание на местоимения\n3. Ищи связующие слова\n\n✅ *Part 7:*\n1. Подчёркивай ключевые слова\n2. Сканируй текст быстро",
        "homework": "📝 *Домашнее задание:*\n\nПрочитай статью на английском (BBC, The Guardian):\n1. Выпиши 10 незнакомых слов\n2. Определи главную мысль каждого абзаца\n3. Перескажи статью в 3-4 предложениях",
        "questions": [
            {"text": "Social media has transformed communication. While it enables instant global connectivity, experts warn about addiction, privacy issues, and misinformation spreading rapidly online.", "q": "What is the main concern experts have about social media?", "options": ["It is too expensive", "It has negative effects", "It is not popular", "It is too slow"], "a": "It has negative effects", "exp": "Текст упоминает addiction, privacy issues, misinformation — всё негативные эффекты"},
            {"text": "The Amazon rainforest produces 20% of the world's oxygen. However, deforestation threatens this vital ecosystem.", "q": "Why is the Amazon important?", "options": ["It is very large", "It produces oxygen", "It has many animals", "It is very old"], "a": "It produces oxygen", "exp": "Текст: 'produces 20% of the world's oxygen'"},
        ]
    },
]

WRITING_LESSONS = [
    {
        "title": "Essay Writing",
        "rule": "✏️ *Essay Writing (FCE Part 1)*\n\n✅ *Структура (180-190 слов):*\n1. Introduction — представь тему\n2. Body paragraph 1 — первый аргумент\n3. Body paragraph 2 — второй аргумент\n4. Conclusion — вывод\n\n✅ *Полезные фразы:*\nIntro: It is often argued that... / Nowadays...\nAdding: Furthermore, / Moreover,\nContrast: However, / Nevertheless,\nConclusion: In conclusion, / To sum up,\n\n⚠️ Формальный стиль — no contractions!",
        "homework": "📝 *Домашнее задание:*\n\nНапиши эссе (180-190 слов):\n*'Social media does more harm than good.'*\n\n• Введение\n• Абзац 1: вред\n• Абзац 2: польза\n• Заключение",
        "questions": [
            {"q": "Какая фраза подходит для введения эссе?", "options": ["Nowadays, lots of people...", "Hey, so basically...", "I'm gonna talk about...", "Well, it's like..."], "a": "Nowadays, lots of people...", "exp": "Формальный стиль: Nowadays, lots of people..."},
            {"q": "Какое слово показывает КОНТРАСТ?", "options": ["Furthermore", "Moreover", "However", "In addition"], "a": "However", "exp": "However = однако — слово контраста"},
            {"q": "Что НЕЛЬЗЯ в формальном тексте?", "options": ["Passive voice", "Сокращения (don't)", "Сложные предложения", "Формальная лексика"], "a": "Сокращения (don't)", "exp": "В формальном стиле: do not, cannot (не don't, can't)"},
        ]
    },
]

SPEAKING_TIPS = [
    "🗣 *Part 1 — Интервью (2 мин)*\n\nОтвечай развёрнуто!\nСтруктура: *Ответ + причина + пример*\n\n❌ 'Yes'\n✅ 'Yes, I really enjoy football because it keeps me fit.'\n\n💡 Полезные фразы:\n• As far as I'm concerned...\n• To be honest...\n• What I really enjoy is...",
    "🗣 *Part 2 — Long Turn (1 мин)*\n\nОписывай и сравнивай фотографии!\n\n✅ Структура:\n1. In the first photo I can see...\n2. In contrast, the second photo shows...\n3. Both photos seem to be about...\n\n💡 Если не знаешь слово:\n• It looks like...\n• It seems to be some kind of...",
    "🗣 *Part 3 — Discussion (3 мин)*\n\nОбсуждай с партнёром!\n\n✅ Полезные фразы:\n• What do you think about...?\n• I agree with you because...\n• That's a good point, but...\n• Shall we move on to...?",
]

LISTENING_TIPS = [
    "🎧 *FCE Listening — Советы*\n\n✅ ДО прослушивания:\n• Читай вопросы внимательно\n• Подчёркивай ключевые слова\n\n✅ ВО ВРЕМЯ:\n• Слушай контекст, не только слова\n• Не паникуй если пропустил\n\n⚠️ Опасные слова:\n• but, however → меняют смысл!\n• actually → исправление!",
    "🎧 *FCE Listening — 4 части*\n\n• *Part 1:* 8 диалогов — MCQ\n• *Part 2:* Монолог — заполни пропуски\n• *Part 3:* 5 говорящих — сопоставь\n• *Part 4:* Интервью — MCQ\n\n💡 Part 2: Пиши то что слышишь!\n💡 Part 3: Сначала слушай о чём говорит каждый.",
]

LESSONS = {
    "grammar": GRAMMAR_RULES,
    "vocab": VOCAB_RULES,
    "reading": READING_LESSONS,
    "writing": WRITING_LESSONS,
}

IDX_KEYS = {
    "grammar": "grammar_idx",
    "vocab": "vocab_idx",
    "reading": "reading_idx",
    "writing": "writing_idx",
}

user_store = {}

def init_user(user_id):
    if user_id not in user_store:
        user_store[user_id] = {
            "correct": 0,
            "wrong": 0,
            "grammar_idx": 0,
            "vocab_idx": 0,
            "reading_idx": 0,
            "writing_idx": 0,
            "speaking_idx": 0,
            "listening_idx": 0,
            "questions": [],
            "q_index": 0,
            "section": None,
            "lesson_hw": "",
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

def lesson_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Начать тест", callback_data="start_test")],
        [InlineKeyboardButton("🏠 Домашнее задание", callback_data="homework")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_user(user.id)
    s = user_store[user.id]
    s["questions"] = []
    s["q_index"] = 0
    s["section"] = None
    s["lesson_hw"] = ""
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"🎓 *FCE B2 English Trainer*\n\n"
        f"Здесь ты найдёшь:\n"
        f"• Объяснение правил\n"
        f"• Тесты для закрепления\n"
        f"• Домашние задания\n\n"
        f"Выбери раздел:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def send_question(query, user_id):
    store = user_store[user_id]
    questions = store["questions"]
    q_idx = store["q_index"]

    if not questions:
        await query.edit_message_text(
            "Сначала выбери раздел из меню!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]])
        )
        return

    if q_idx >= len(questions):
        await query.edit_message_text(
            "🎉 *Тест завершён! Отличная работа!*\n\nНе забудь выполнить домашнее задание!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Пройти снова", callback_data="start_test")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
            ])
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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    init_user(user_id)
    store = user_store[user_id]
    data = query.data

    if data == "menu":
        store["section"] = None
        store["questions"] = []
        store["q_index"] = 0
        store["lesson_hw"] = ""
        await query.edit_message_text("Выбери раздел:", reply_markup=get_main_menu())

    elif data in ("sec_grammar", "sec_vocab", "sec_reading", "sec_writing"):
        section = data.replace("sec_", "")
        lessons = LESSONS[section]
        idx_key = IDX_KEYS[section]
        idx = store[idx_key] % len(lessons)
        store[idx_key] += 1
        lesson = lessons[idx]
        store["section"] = section
        store["questions"] = list(lesson["questions"])
        store["q_index"] = 0
        store["lesson_hw"] = lesson["homework"]
        await query.edit_message_text(lesson["rule"], parse_mode="Markdown", reply_markup=lesson_keyboard())

    elif data == "sec_speaking":
        idx = store["speaking_idx"] % len(SPEAKING_TIPS)
        store["speaking_idx"] += 1
        await query.edit_message_text(
            SPEAKING_TIPS[idx],
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_speaking")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
            ])
        )

    elif data == "sec_listening":
        idx = store["listening_idx"] % len(LISTENING_TIPS)
        store["listening_idx"] += 1
        await query.edit_message_text(
            LISTENING_TIPS[idx],
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Следующий совет", callback_data="sec_listening")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
            ])
        )

    elif data == "homework":
        hw = store.get("lesson_hw", "")
        if not hw:
            hw = "Сначала выбери раздел из меню!"
        await query.edit_message_text(
            hw,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Начать тест", callback_data="start_test")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
            ])
        )

    elif data == "start_test":
        store["q_index"] = 0
        await send_question(query, user_id)

    elif data == "next_q":
        await send_question(query, user_id)

    elif data.startswith("ans_"):
        chosen = data[4:]
        questions = store["questions"]
        q_idx = store["q_index"] - 1

        if not questions or q_idx < 0 or q_idx >= len(questions):
            await query.edit_message_text(
                "Ошибка. Нажми /start и начни заново.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]])
            )
            return

        q = questions[q_idx]
        correct = q["a"]
        exp = q["exp"]

        if chosen == correct:
            store["correct"] += 1
            text = f"✅ *Правильно!*\n\n💡 {exp}"
        else:
            store["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct}*\n\n💡 {exp}"

        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next_q")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
            ])
        )

    elif data == "stats":
        total = store["correct"] + store["wrong"]
        percent = int(store["correct"] / total * 100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 *Твоя статистика:*\n\n"
            f"✅ Правильных: {store['correct']}\n"
            f"❌ Неправильных: {store['wrong']}\n"
            f"🎯 Точность: {percent}%\n\n"
            f"Продолжай заниматься! 💪",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]])
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Используй кнопки! 👇\nНажми /start чтобы начать.",
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
