import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

DATA = {
    "gr": [
        {
            "rule": "📗 *Present Perfect vs Past Simple*\n\n✅ *Present Perfect* — связь с настоящим:\n• I have lost my keys.\n• She has lived here for 5 years.\n\n✅ *Past Simple* — завершено в прошлом:\n• I lost my keys yesterday.\n• She lived in Paris in 2010.\n\n⚠️ PP: already, yet, just, ever, never, for, since\n⚠️ PS: yesterday, ago, last year, in 2010",
            "hw": "📝 *Домашнее задание:*\n\nНапиши по 5 предложений:\n\n*Present Perfect:*\nПример: I have never been to London.\n\n*Past Simple:*\nПример: I visited Moscow last summer.",
            "test": [
                {"q": "I ___ my homework already.", "a": "have done", "w": ["did", "do", "done"]},
                {"q": "She ___ to Paris in 2019.", "a": "went", "w": ["has gone", "goes", "have gone"]},
                {"q": "They ___ here for 10 years.", "a": "have lived", "w": ["lived", "live", "are living"]},
                {"q": "___ you ever tried sushi?", "a": "Have", "w": ["Did", "Do", "Are"]},
            ]
        },
        {
            "rule": "📗 *Conditionals*\n\n✅ *1st* — реальное будущее:\nIf + Present Simple → will\n• If it rains, I will stay home.\n\n✅ *2nd* — нереальное настоящее:\nIf + Past Simple → would\n• If I were rich, I would travel.\n\n✅ *3rd* — нереальное прошлое:\nIf + Past Perfect → would have\n• If I had studied, I would have passed.",
            "hw": "📝 *Домашнее задание:*\n\nЗакончи предложения:\n1. If it rains tomorrow, I will...\n2. If I were a millionaire, I would...\n3. If I had studied harder, I would have...",
            "test": [
                {"q": "If it ___ tomorrow, we'll cancel.", "a": "rains", "w": ["rained", "will rain", "rain"]},
                {"q": "If I ___ you, I would apologise.", "a": "were", "w": ["am", "was", "be"]},
                {"q": "If she had studied, she ___ the exam.", "a": "would have passed", "w": ["passed", "would pass", "had passed"]},
                {"q": "If he ___ earlier, he'd have caught the train.", "a": "had left", "w": ["left", "leaves", "would leave"]},
            ]
        },
        {
            "rule": "📗 *Passive Voice*\n\n✅ Структура: *be + past participle*\n\n• Present: is/are done\n• Past: was/were done\n• Future: will be done\n• Present Perfect: has/have been done\n\n✅ Используй когда:\n• Не знаем кто сделал\n• Формальный текст",
            "hw": "📝 *Домашнее задание:*\n\nПереведи в Passive Voice:\n1. They build houses every year.\n2. Someone stole my bag.\n3. Scientists have discovered a new planet.",
            "test": [
                {"q": "The Mona Lisa ___ by da Vinci.", "a": "was painted", "w": ["painted", "has painted", "is painting"]},
                {"q": "English ___ all over the world.", "a": "is spoken", "w": ["speaks", "spoke", "has spoken"]},
                {"q": "The results ___ tomorrow.", "a": "will be announced", "w": ["will announce", "announce", "are announced"]},
                {"q": "The letter ___ yesterday.", "a": "was sent", "w": ["sent", "has sent", "is sent"]},
            ]
        },
    ],
    "ue": [
        {
            "rule": "📙 *Use of English — Коллокации*\n\nКоллокации — слова которые всегда идут вместе!\n\n✅ *Make vs Do:*\nMAKE: a decision, an effort, a mistake, progress\nDO: homework, research, damage, well, your best\n\n✅ *Have vs Take:*\nHAVE: a shower, a look, fun, a rest, a chat\nTAKE: a photo, part, a break, a risk, an exam",
            "hw": "📝 *Домашнее задание:*\n\nВставь make/do/have/take:\n1. ___ a decision\n2. ___ research\n3. ___ a photo\n4. ___ fun\n5. ___ a mistake\n6. ___ your best",
            "test": [
                {"q": "She ___ a lot of progress this year.", "a": "made", "w": ["did", "had", "took"]},
                {"q": "Can you ___ a look at my essay?", "a": "have", "w": ["make", "do", "take"]},
                {"q": "He ___ part in the competition.", "a": "took", "w": ["made", "did", "had"]},
                {"q": "I need to ___ some research.", "a": "do", "w": ["make", "have", "take"]},
            ]
        },
        {
            "rule": "📙 *Use of English — Предлоги*\n\n✅ *Прилагательные + предлоги:*\n• good AT sport\n• interested IN art\n• afraid OF spiders\n• responsible FOR results\n• different FROM others\n• similar TO mine\n\n✅ *Глаголы + предлоги:*\n• depend ON\n• succeed IN\n• apologise FOR\n• consist OF",
            "hw": "📝 *Домашнее задание:*\n\nВставь правильный предлог:\n1. She is very good ___ maths.\n2. He is afraid ___ dogs.\n3. It depends ___ the weather.\n4. She succeeded ___ passing the exam.",
            "test": [
                {"q": "She is very good ___ mathematics.", "a": "at", "w": ["in", "on", "for"]},
                {"q": "He is afraid ___ spiders.", "a": "of", "w": ["from", "at", "about"]},
                {"q": "It depends ___ the weather.", "a": "on", "w": ["of", "from", "at"]},
                {"q": "She succeeded ___ passing the exam.", "a": "in", "w": ["at", "on", "for"]},
            ]
        },
    ],
    "vo": [
        {
            "rule": "📘 *Vocabulary — Описание людей*\n\n✅ *Характер:*\n• ambitious — амбициозный\n• reliable — надёжный\n• stubborn — упрямый\n• generous — щедрый\n• arrogant — высокомерный\n\n✅ *Состояние:*\n• exhausted — измотанный\n• furious — в ярости\n• anxious — тревожный",
            "hw": "📝 *Домашнее задание:*\n\nОпиши своего друга используя минимум 6 слов из урока.\n\nПример:\nMy friend is very reliable and generous...",
            "test": [
                {"q": "Надёжный = ?", "a": "reliable", "w": ["stubborn", "arrogant", "anxious"]},
                {"q": "Измотанный = ?", "a": "exhausted", "w": ["furious", "ambitious", "generous"]},
                {"q": "She felt ___ before the exam.", "a": "anxious", "w": ["furious", "generous", "stubborn"]},
                {"q": "He never gives up — he's very ___.", "a": "ambitious", "w": ["slim", "exhausted", "arrogant"]},
            ]
        },
        {
            "rule": "📘 *Vocabulary — Технологии*\n\n✅ *Полезные слова:*\n• artificial intelligence — ИИ\n• data privacy — конфиденциальность\n• misinformation — дезинформация\n• remote work — удалённая работа\n• cyberbullying — кибербуллинг\n\n✅ *Фразовые глаголы:*\n• log in/out — войти/выйти\n• back up — резервная копия\n• scroll through — листать",
            "hw": "📝 *Домашнее задание:*\n\nНапиши 6 предложений о влиянии технологий используя слова из урока.",
            "test": [
                {"q": "Дезинформация = ?", "a": "misinformation", "w": ["data privacy", "cyberbullying", "remote work"]},
                {"q": "Войти в аккаунт = ?", "a": "log in", "w": ["back up", "scroll through", "set up"]},
                {"q": "Always ___ your files!", "a": "back up", "w": ["log in", "set up", "scroll through"]},
                {"q": "He ___ through social media for hours.", "a": "scrolled", "w": ["backed", "logged", "set"]},
            ]
        },
    ],
    "su": [
        {
            "rule": "🔤 *Суффиксы*\n\n✅ *Существительные:*\n-tion: education, decision\n-ment: employment, achievement\n-ness: happiness, darkness\n-ity: creativity, curiosity\n\n✅ *Прилагательные:*\n-ful: beautiful, careful\n-less: careless, useless\n-able: reliable, possible\n\n✅ *Наречия:*\n-ly: carefully, effectively\n\n✅ *Отрицательные префиксы:*\nun-, in-, im-, dis-",
            "hw": "📝 *Домашнее задание:*\n\nОбразуй слова:\n1. CREATE → ___ (noun)\n2. RELY → ___ (adjective)\n3. HAPPY → ___ (adverb)\n4. EMPLOY → ___ (noun)\n5. CARE → ___ (adjective, negative)",
            "test": [
                {"q": "Her ___ (CREATIVE) was impressive.", "a": "creativity", "w": ["creation", "creative", "create"]},
                {"q": "He is a very ___ (RELY) person.", "a": "reliable", "w": ["relying", "reliance", "rely"]},
                {"q": "She spoke ___ (CAREFUL).", "a": "carefully", "w": ["careful", "carefulness", "careless"]},
                {"q": "The ___ (EMPLOY) rate is rising.", "a": "employment", "w": ["employer", "employee", "employ"]},
            ]
        },
    ],
    "re": [
        {
            "rule": "📰 *Reading — Стратегия FCE*\n\n✅ *Part 5 — Multiple Choice:*\n1. Читай вопросы ДО текста\n2. Ищи ПЕРЕФРАЗ, не точные слова\n3. Исключай неверные варианты\n\n✅ *Part 6 — Gapped Text:*\n1. Читай весь текст сначала\n2. Следи за местоимениями\n3. Ищи linking words\n\n✅ *Part 7 — Multiple Matching:*\n1. Подчёркивай ключевые слова\n2. Сканируй каждый текст",
            "hw": "📝 *Домашнее задание:*\n\nПрочитай статью на BBC или CNN:\n1. Выпиши 10 новых слов\n2. Определи главную мысль каждого абзаца\n3. Перескажи в 4-5 предложениях",
            "test": [
                {"q": "'Social media causes addiction and spreads misinformation.'\n\nWhat is a negative effect?", "a": "Addiction", "w": ["Connectivity", "Speed", "Cost"]},
                {"q": "'The Amazon produces 20% of world's oxygen. Deforestation threatens it.'\n\nWhat threatens the Amazon?", "a": "Deforestation", "w": ["Oxygen", "Animals", "Climate"]},
                {"q": "В Part 5 нужно искать:", "a": "Перефраз идей", "w": ["Точные слова", "Длинный абзац", "Первое предложение"]},
                {"q": "В Part 6 важно следить за:", "a": "Местоимениями и linking words", "w": ["Длиной предложений", "Числом абзацев", "Заголовком"]},
            ]
        },
    ],
    "wr": [
        {
            "rule": "✏️ *Writing — Essay FCE*\n\n✅ *Структура (180-190 слов):*\n1. Introduction\n2. Body paragraph 1\n3. Body paragraph 2\n4. Conclusion\n\n✅ *Полезные фразы:*\nIntro: Nowadays... / It is argued that...\nAdding: Furthermore, / Moreover,\nContrast: However, / Nevertheless,\nConclusion: In conclusion, / To sum up,\n\n⚠️ Только формальный стиль!\n❌ don't → ✅ do not",
            "hw": "📝 *Домашнее задание:*\n\nНапиши эссе (180-190 слов):\n📌 'Technology has made our lives better.'\n\n• Introduction\n• Para 1: плюсы\n• Para 2: минусы\n• Conclusion",
            "test": [
                {"q": "Какая фраза для введения эссе?", "a": "Nowadays, many people believe...", "w": ["Hey guys...", "So basically...", "I wanna discuss..."]},
                {"q": "Какое слово показывает КОНТРАСТ?", "a": "However", "w": ["Furthermore", "Moreover", "In addition"]},
                {"q": "Что НЕЛЬЗЯ в формальном эссе?", "a": "Сокращения (don't)", "w": ["Passive voice", "Linking words", "Сложные предложения"]},
                {"q": "Как формально написать 'I think'?", "a": "It is believed that", "w": ["I feel like", "In my mind", "Personally"]},
            ]
        },
    ],
    "sp": [
        {
            "rule": "🗣 *Speaking — FCE*\n\n✅ *Part 1 — Interview (2 min):*\nОтвечай: Ответ + причина + пример\n❌ 'Yes' → ✅ 'Yes, I enjoy it because...'\n\n✅ *Part 2 — Long Turn (1 min):*\n• In the first photo I can see...\n• In contrast, the second shows...\n• Both photos seem to be about...\n\n✅ *Part 3 — Discussion (3 min):*\n• What do you think about...?\n• I agree because...\n• That's a good point, but...",
            "hw": "📝 *Домашнее задание:*\n\nЗапиши себя на 1 минуту:\n'What are the advantages of social media?'\n\nИспользуй минимум 5 фраз из урока.\nПрослушай — есть ли паузы? Повторяй!",
            "test": [
                {"q": "В Part 2 нужно:", "a": "Сравнивать два фото", "w": ["Читать текст вслух", "Только отвечать на вопросы", "Описывать одно фото"]},
                {"q": "Как лучше ответить 'Do you like sport?'", "a": "Yes, I enjoy football because it keeps me fit.", "w": ["Yes.", "Yes I do.", "Sport is good."]},
                {"q": "Если не знаешь слово — что делать?", "a": "It's a kind of... / It looks like...", "w": ["Замолчать", "Сказать I don't know", "Говорить по-русски"]},
                {"q": "Сколько минут длится Part 2?", "a": "1 минута", "w": ["2 минуты", "3 минуты", "30 секунд"]},
            ]
        },
    ],
    "li": [
        {
            "rule": "🎧 *Listening — FCE*\n\n✅ *4 части:*\n• Part 1: 8 диалогов — MCQ\n• Part 2: Монолог — 10 пропусков\n• Part 3: 5 говорящих — сопоставь\n• Part 4: Интервью — MCQ\n\n✅ *Стратегия:*\n1. Читай вопросы ДО прослушивания\n2. Подчёркивай ключевые слова\n3. Слушай КОНТЕКСТ\n\n⚠️ *Опасные слова:*\n• but, however → меняют смысл!\n• actually → исправление!\n• most importantly → главная идея!",
            "hw": "📝 *Домашнее задание:*\n\n1. Найди на YouTube: 'BBC 6 Minute English'\n2. Послушай один выпуск\n3. Запиши 10 новых слов\n4. Послушай с субтитрами\n5. Перескажи тему в 3-4 предложениях",
            "test": [
                {"q": "Сколько частей в FCE Listening?", "a": "4", "w": ["3", "5", "6"]},
                {"q": "В Part 2 нужно:", "a": "Заполнить 10 пропусков", "w": ["Выбрать из 3 вариантов", "Сопоставить говорящих", "Ответить письменно"]},
                {"q": "Слово 'however' значит:", "a": "Сейчас будет контраст!", "w": ["Продолжение идеи", "Пример", "Вывод"]},
                {"q": "Что делать ДО прослушивания?", "a": "Читать вопросы и подчёркивать ключевые слова", "w": ["Писать конспект", "Переводить слова", "Ничего"]},
            ]
        },
    ],
}

SECTIONS = [
    ("gr", "📗 Грамматика"),
    ("ue", "📙 Use of English"),
    ("vo", "📘 Словарный запас"),
    ("su", "🔤 Суффиксы"),
    ("re", "📰 Reading"),
    ("wr", "✏️ Writing"),
    ("sp", "🗣 Speaking"),
    ("li", "🎧 Listening"),
]

user_stats = {}

def init_user(uid):
    if uid not in user_stats:
        user_stats[uid] = {"correct": 0, "wrong": 0}

def get_main_menu():
    rows = []
    for i in range(0, len(SECTIONS), 2):
        row = []
        for code, name in SECTIONS[i:i+2]:
            row.append(InlineKeyboardButton(name, callback_data=f"S{code}0"))
        rows.append(row)
    rows.append([InlineKeyboardButton("📊 Моя статистика", callback_data="ST")])
    return InlineKeyboardMarkup(rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_user(update.effective_user.id)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\n\n"
        "🎓 *FCE B2 English Trainer*\n\n"
        "Выбери раздел:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    init_user(uid)
    data = query.data

    if data == "MN":
        await query.edit_message_text("Выбери раздел:", reply_markup=get_main_menu())
        return

    if data == "ST":
        s = user_stats[uid]
        total = s["correct"] + s["wrong"]
        pct = int(s["correct"] / total * 100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 *Статистика:*\n\n✅ Правильных: {s['correct']}\n❌ Неправильных: {s['wrong']}\n🎯 Точность: {pct}%\n\n💪 Продолжай!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="MN")]])
        )
        return

    # S{sec}{li} — показать урок
    if data[0] == "S" and len(data) >= 4:
        sec = data[1:3]
        li = int(data[3:])
        lessons = DATA[sec]
        li = li % len(lessons)
        lesson = lessons[li]
        next_li = (li + 1) % len(lessons)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"T{sec}{li}q0")],
            [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"H{sec}{li}")],
            [InlineKeyboardButton("➡️ Следующий урок", callback_data=f"S{sec}{next_li}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="MN")],
        ])
        await query.edit_message_text(lesson["rule"], parse_mode="Markdown", reply_markup=kb)
        return

    # H{sec}{li} — домашнее задание
    if data[0] == "H" and len(data) >= 4:
        sec = data[1:3]
        li = int(data[3:])
        lesson = DATA[sec][li]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"T{sec}{li}q0")],
            [InlineKeyboardButton("🔙 К уроку", callback_data=f"S{sec}{li}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="MN")],
        ])
        await query.edit_message_text(lesson["hw"], parse_mode="Markdown", reply_markup=kb)
        return

    # T{sec}{li}q{qi} — вопрос теста
    if data[0] == "T" and "q" in data:
        sec = data[1:3]
        rest = data[3:]
        li, qi = rest.split("q")
        li = int(li)
        qi = int(qi)
        questions = DATA[sec][li]["test"]
        if qi >= len(questions):
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Пройти снова", callback_data=f"T{sec}{li}q0")],
                [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"H{sec}{li}")],
                [InlineKeyboardButton("🔙 Меню", callback_data="MN")],
            ])
            await query.edit_message_text(
                "🎉 *Тест завершён! Молодец!*\n\nВыполни домашнее задание для закрепления!",
                parse_mode="Markdown", reply_markup=kb
            )
            return

        q = questions[qi]
        opts = [q["a"]] + q["w"]
        random.shuffle(opts)
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton(o, callback_data=f"A{sec}{li}q{qi}|{o}")] for o in opts] +
            [[InlineKeyboardButton("🔙 Меню", callback_data="MN")]]
        )
        await query.edit_message_text(
            f"❓ *Вопрос {qi+1}/{len(questions)}*\n\n{q['q']}",
            parse_mode="Markdown", reply_markup=kb
        )
        return

    # A{sec}{li}q{qi}|{chosen} — ответ
    if data[0] == "A" and "q" in data and "|" in data:
        main, chosen = data.rsplit("|", 1)
        sec = main[1:3]
        rest = main[3:]
        li, qi = rest.split("q")
        li = int(li)
        qi = int(qi)
        q = DATA[sec][li]["test"][qi]
        correct = q["a"]

        if chosen == correct:
            user_stats[uid]["correct"] += 1
            text = "✅ *Правильно!*"
        else:
            user_stats[uid]["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct}*"

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"T{sec}{li}q{qi+1}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="MN")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нажми /start! 👇")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main() 
