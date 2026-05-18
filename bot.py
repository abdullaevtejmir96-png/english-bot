import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

# ============================================================
# ДАННЫЕ — все уроки
# ============================================================

DATA = {
    "grammar": [
        {
            "name": "Present Perfect vs Past Simple",
            "rule": (
                "📗 *Present Perfect vs Past Simple*\n\n"
                "✅ *Present Perfect* — связь с настоящим:\n"
                "• I have lost my keys. (всё ещё потеряны)\n"
                "• She has lived here for 5 years.\n\n"
                "✅ *Past Simple* — завершено в прошлом:\n"
                "• I lost my keys yesterday.\n"
                "• She lived in Paris in 2010.\n\n"
                "⚠️ PP: already, yet, just, ever, never, for, since\n"
                "⚠️ PS: yesterday, ago, last year, in 2010"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Напиши по 5 предложений:\n\n"
                "*Present Perfect:*\n"
                "Пример: I have never been to London.\n\n"
                "*Past Simple:*\n"
                "Пример: I visited Moscow last summer."
            ),
            "test": [
                {"q": "I ___ my homework already.", "a": "have done", "w": ["did", "do", "done"]},
                {"q": "She ___ to Paris in 2019.", "a": "went", "w": ["has gone", "goes", "have gone"]},
                {"q": "They ___ here for 10 years.", "a": "have lived", "w": ["lived", "live", "are living"]},
                {"q": "___ you ever tried sushi?", "a": "Have", "w": ["Did", "Do", "Are"]},
                {"q": "I ___ her since Monday.", "a": "haven't seen", "w": ["didn't see", "don't see", "wasn't seeing"]},
            ]
        },
        {
            "name": "Conditionals 1, 2, 3",
            "rule": (
                "📗 *Условные предложения*\n\n"
                "✅ *1st Conditional* — реальное будущее:\n"
                "If + Present Simple → will\n"
                "• If it rains, I will stay home.\n\n"
                "✅ *2nd Conditional* — нереальное настоящее:\n"
                "If + Past Simple → would\n"
                "• If I were rich, I would travel.\n\n"
                "✅ *3rd Conditional* — нереальное прошлое:\n"
                "If + Past Perfect → would have\n"
                "• If I had studied, I would have passed."
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Закончи предложения:\n\n"
                "1. If it rains tomorrow, I will...\n"
                "2. If I were a millionaire, I would...\n"
                "3. If I had studied harder, I would have..."
            ),
            "test": [
                {"q": "If it ___ tomorrow, we'll cancel.", "a": "rains", "w": ["rained", "will rain", "rain"]},
                {"q": "If I ___ you, I would apologise.", "a": "were", "w": ["am", "was", "be"]},
                {"q": "If she had studied, she ___ the exam.", "a": "would have passed", "w": ["passed", "would pass", "had passed"]},
                {"q": "If he ___ earlier, he'd have caught the train.", "a": "had left", "w": ["left", "leaves", "would leave"]},
                {"q": "If I have time, I ___ you.", "a": "will call", "w": ["would call", "called", "call"]},
            ]
        },
        {
            "name": "Passive Voice",
            "rule": (
                "📗 *Passive Voice*\n\n"
                "✅ Структура: *be + past participle*\n\n"
                "• Present: is/are + done\n"
                "• Past: was/were + done\n"
                "• Future: will be + done\n"
                "• Present Perfect: has/have been + done\n\n"
                "✅ Используй когда:\n"
                "• Не знаем кто сделал\n"
                "• Объект важнее субъекта\n"
                "• Формальный текст"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Переведи в Passive Voice:\n\n"
                "1. They build houses every year.\n"
                "2. Someone stole my bag.\n"
                "3. Scientists have discovered a new planet.\n"
                "4. They will deliver the package tomorrow."
            ),
            "test": [
                {"q": "The Mona Lisa ___ by da Vinci.", "a": "was painted", "w": ["painted", "has painted", "is painting"]},
                {"q": "English ___ all over the world.", "a": "is spoken", "w": ["speaks", "spoke", "has spoken"]},
                {"q": "The results ___ tomorrow.", "a": "will be announced", "w": ["will announce", "announce", "are announced"]},
                {"q": "The bridge ___ recently.", "a": "has been built", "w": ["is building", "has been building", "built"]},
                {"q": "The letter ___ yesterday.", "a": "was sent", "w": ["sent", "has sent", "is sent"]},
            ]
        },
    ],
    "uoe": [
        {
            "name": "Use of English — Коллокации",
            "rule": (
                "📙 *Use of English — Коллокации*\n\n"
                "Коллокации — слова которые всегда идут вместе!\n\n"
                "✅ *Make vs Do:*\n"
                "MAKE: a decision, an effort, a mistake, progress, friends\n"
                "DO: homework, research, damage, well, your best\n\n"
                "✅ *Have vs Take:*\n"
                "HAVE: a shower, a look, fun, a rest, a chat\n"
                "TAKE: a photo, part, a break, a risk, an exam\n\n"
                "✅ *Go vs Come:*\n"
                "GO: bankrupt, wrong, missing\n"
                "COME: true, first, into force"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Вставь make/do/have/take:\n\n"
                "1. ___ a decision\n"
                "2. ___ research\n"
                "3. ___ a photo\n"
                "4. ___ fun\n"
                "5. ___ a mistake\n"
                "6. ___ your best\n"
                "7. ___ part in"
            ),
            "test": [
                {"q": "She ___ a lot of progress this year.", "a": "made", "w": ["did", "had", "took"]},
                {"q": "Can you ___ a look at my essay?", "a": "have", "w": ["make", "do", "take"]},
                {"q": "He ___ part in the competition.", "a": "took", "w": ["made", "did", "had"]},
                {"q": "I need to ___ some research.", "a": "do", "w": ["make", "have", "take"]},
                {"q": "Don't ___ a risk — it's dangerous!", "a": "take", "w": ["make", "do", "have"]},
            ]
        },
        {
            "name": "Use of English — Предлоги",
            "rule": (
                "📙 *Use of English — Предлоги*\n\n"
                "✅ *Прилагательные + предлоги:*\n"
                "• good AT (sport)\n"
                "• interested IN (art)\n"
                "• afraid OF (spiders)\n"
                "• responsible FOR (results)\n"
                "• different FROM (others)\n"
                "• similar TO (mine)\n\n"
                "✅ *Глаголы + предлоги:*\n"
                "• depend ON\n"
                "• succeed IN\n"
                "• apologise FOR\n"
                "• insist ON\n"
                "• consist OF"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Вставь правильный предлог:\n\n"
                "1. She is very good ___ maths.\n"
                "2. He is afraid ___ dogs.\n"
                "3. This bag is similar ___ mine.\n"
                "4. It depends ___ the weather.\n"
                "5. She succeeded ___ passing the exam."
            ),
            "test": [
                {"q": "She is very good ___ mathematics.", "a": "at", "w": ["in", "on", "for"]},
                {"q": "He is afraid ___ spiders.", "a": "of", "w": ["from", "at", "about"]},
                {"q": "It depends ___ the weather.", "a": "on", "w": ["of", "from", "at"]},
                {"q": "She succeeded ___ passing the exam.", "a": "in", "w": ["at", "on", "for"]},
                {"q": "This is different ___ what I expected.", "a": "from", "w": ["to", "of", "than"]},
            ]
        },
    ],
    "vocabulary": [
        {
            "name": "Vocabulary — Описание людей",
            "rule": (
                "📘 *Vocabulary — Описание людей*\n\n"
                "✅ *Характер:*\n"
                "• ambitious — амбициозный\n"
                "• reliable — надёжный\n"
                "• stubborn — упрямый\n"
                "• generous — щедрый\n"
                "• arrogant — высокомерный\n"
                "• compassionate — сострадательный\n\n"
                "✅ *Внешность:*\n"
                "• slim — стройный\n"
                "• broad-shouldered — широкоплечий\n"
                "• well-built — спортивного телосложения\n\n"
                "✅ *Состояние:*\n"
                "• exhausted — измотанный\n"
                "• furious — в ярости\n"
                "• anxious — тревожный"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Опиши своего друга или известного человека используя минимум 6 слов из урока.\n\n"
                "Пример:\n"
                "My friend is very reliable and generous. He is slim and well-built..."
            ),
            "test": [
                {"q": "Надёжный = ?", "a": "reliable", "w": ["stubborn", "arrogant", "anxious"]},
                {"q": "Измотанный = ?", "a": "exhausted", "w": ["furious", "ambitious", "generous"]},
                {"q": "Высокомерный = ?", "a": "arrogant", "w": ["compassionate", "reliable", "slim"]},
                {"q": "She felt ___ before the exam — she couldn't sleep.", "a": "anxious", "w": ["furious", "generous", "stubborn"]},
                {"q": "He never gives up — he's very ___.", "a": "ambitious", "w": ["slim", "exhausted", "arrogant"]},
            ]
        },
        {
            "name": "Vocabulary — Технологии",
            "rule": (
                "📘 *Vocabulary — Технологии*\n\n"
                "✅ *Полезные слова:*\n"
                "• artificial intelligence — искусственный интеллект\n"
                "• data privacy — конфиденциальность данных\n"
                "• social media — социальные сети\n"
                "• misinformation — дезинформация\n"
                "• remote work — удалённая работа\n"
                "• cyberbullying — кибербуллинг\n\n"
                "✅ *Фразовые глаголы:*\n"
                "• log in/out — войти/выйти\n"
                "• set up — настроить\n"
                "• back up — сделать резервную копию\n"
                "• scroll through — листать"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Напиши 6 предложений о влиянии технологий на жизнь используя слова из урока.\n\n"
                "Пример:\n"
                "Social media can spread misinformation very quickly..."
            ),
            "test": [
                {"q": "Дезинформация = ?", "a": "misinformation", "w": ["data privacy", "cyberbullying", "remote work"]},
                {"q": "Войти в аккаунт = ?", "a": "log in", "w": ["set up", "back up", "scroll through"]},
                {"q": "The company stores your ___.", "a": "data privacy", "w": ["misinformation", "remote work", "log in"]},
                {"q": "Always ___ your files in case you lose them.", "a": "back up", "w": ["log in", "set up", "scroll through"]},
                {"q": "He ___ through his social media feed for hours.", "a": "scrolled", "w": ["backed", "logged", "set"]},
            ]
        },
    ],
    "suffixes": [
        {
            "name": "Суффиксы — Словообразование",
            "rule": (
                "🔤 *Суффиксы (Word Formation)*\n\n"
                "✅ *Существительные:*\n"
                "-tion/-sion: education, decision\n"
                "-ment: employment, achievement\n"
                "-ness: happiness, darkness\n"
                "-ity: creativity, curiosity\n"
                "-er/-or: teacher, actor\n\n"
                "✅ *Прилагательные:*\n"
                "-ful: beautiful, careful\n"
                "-less: careless, useless\n"
                "-able/-ible: reliable, possible\n"
                "-ive: creative, effective\n\n"
                "✅ *Наречия:*\n"
                "-ly: carefully, effectively\n\n"
                "✅ *Отрицательные префиксы:*\n"
                "un-, in-, im-, dis-: unhappy, incorrect"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Образуй слова:\n\n"
                "1. CREATE → ___ (noun)\n"
                "2. RELY → ___ (adjective)\n"
                "3. HAPPY → ___ (adverb)\n"
                "4. EMPLOY → ___ (noun)\n"
                "5. CARE → ___ (adjective, negative)\n"
                "6. DECIDE → ___ (noun)\n"
                "7. EFFECT → ___ (adjective)"
            ),
            "test": [
                {"q": "Her ___ (CREATIVE) was impressive.", "a": "creativity", "w": ["creation", "creative", "create"]},
                {"q": "He is a very ___ (RELY) person.", "a": "reliable", "w": ["relying", "reliance", "rely"]},
                {"q": "She spoke ___ (CAREFUL).", "a": "carefully", "w": ["careful", "carefulness", "careless"]},
                {"q": "The ___ (EMPLOY) rate is rising.", "a": "employment", "w": ["employer", "employee", "employ"]},
                {"q": "It's ___ (POSSIBLE) to finish by Friday — too much work.", "a": "impossible", "w": ["unpossible", "dispossible", "inpossible"]},
            ]
        },
    ],
    "reading": [
        {
            "name": "Reading — Стратегия FCE",
            "rule": (
                "📰 *Reading — Стратегия FCE*\n\n"
                "✅ *Part 5 — Multiple Choice:*\n"
                "1. Читай вопросы ДО текста\n"
                "2. Ищи нужный абзац\n"
                "3. Ищи ПЕРЕФРАЗ, не точные слова\n"
                "4. Исключай неверные варианты\n\n"
                "✅ *Part 6 — Gapped Text:*\n"
                "1. Читай весь текст сначала\n"
                "2. Следи за местоимениями (he/she/they)\n"
                "3. Ищи linking words\n\n"
                "✅ *Part 7 — Multiple Matching:*\n"
                "1. Подчёркивай ключевые слова в вопросах\n"
                "2. Сканируй каждый текст\n"
                "3. Ищи синонимы"
            ),
            "hw": (
                "📝 *Домашнее задание:*\n\n"
                "Прочитай любую статью на английском (BBC, The Guardian, CNN):\n\n"
                "1. Выпиши 10 незнакомых слов с переводом\n"
                "2. Определи главную мысль каждого абзаца\n"
                "3. Перескажи статью в 4-5 предложениях"
            ),
            "test": [
                {"q": "📄 'Social media enables connectivity but causes addiction and spreads misinformation.'\n\nWhat is a negative effect of social media?", "a": "Addiction", "w": ["Connectivity", "Speed", "Cost"]},
                {"q": "📄 'The Amazon produces 20% of the world's oxygen. Deforestation threatens this ecosystem.'\n\nWhat threatens the Amazon?", "a": "Deforestation", "w": ["Oxygen", "Animals", "Climate"]},
                {"q": "📄 'Scientists discovered that regular exercise improves mental health significantly.'\n\nWhat does exercise improve?", "a": "Mental health", "w": ["Physical strength", "Sleep quality", "Social skills"]},
                {"q": "В Part 5 нужно искать:", "a": "Перефраз идей", "w": ["Точные слова из текста", "Самый длинный абзац", "Первое предложение"]},
                {"q": "В Part 6 (Gapped text) важно следить за:", "a": "Местоимениями и linking words", "w": ["Длиной предложений", "Числом абзацев", "Заголовком текста"]},
            ]
        },
    ],
    "writing": [
        {
            "name": "Writing — Essay FCE",
            "rule": (
                "✏️ *Writing — Essay (FCE Part 1)*\n\n"
                "✅ *Структура (180-190 слов):*\n"
                "1. Introduction — тема + тезис\n"
                "2. Body para 1 — аргумент + пример\n"
                "3. Body para 2 — аргумент + пример\n"
                "4. Conclusion — вывод + мнение\n\n"
                "✅ *Полезные фразы:*\n"
                "Intro: Nowadays... / It is often argued...\n"
                "Adding: Furthermore, / Moreover, / In addition,\n"
                "Contrast: However, / Nevertheless, / On the other hand,\n"
                "Result: Therefore, / As a result, / Consequently,\n"
                "Conclusion: In conclusion, / To sum up,\n\n"
                "⚠️ *Правила формального стиля:*\n"
                "❌ don't → ✅ do not\n"
                "❌ can't → ✅ cannot\n"
                "❌ I think → ✅ It is believed that"
            ),
            "hw": (
                "📝 *Домашнее задание — Essay:*\n\n"
                "Напиши эссе (180-190 слов):\n\n"
                "📌 *Тема:* 'Technology has made our lives better. Discuss.'\n\n"
                "Структура:\n"
                "• Introduction: what is technology\n"
                "• Para 1: advantages (communication, information)\n"
                "• Para 2: disadvantages (addiction, privacy)\n"
                "• Conclusion: your opinion\n\n"
                "⚠️ Используй linking words из урока!"
            ),
            "test": [
                {"q": "Какая фраза подходит для введения эссе?", "a": "Nowadays, many people believe...", "w": ["Hey guys, today I wanna talk...", "So basically...", "I'm gonna discuss..."]},
                {"q": "Какое слово показывает КОНТРАСТ?", "a": "However", "w": ["Furthermore", "Moreover", "In addition"]},
                {"q": "Что НЕЛЬЗЯ в формальном эссе?", "a": "Сокращения (don't, can't)", "w": ["Passive voice", "Complex sentences", "Linking words"]},
                {"q": "Какое слово добавляет аргумент?", "a": "Furthermore", "w": ["However", "Nevertheless", "In conclusion"]},
                {"q": "Как формально написать 'I think'?", "a": "It is believed that", "w": ["I feel like", "In my mind", "Personally speaking"]},
            ]
        },
    ],
    "speaking": [
        {
            "name": "Speaking — FCE Parts 1-4",
            "rule": (
                "🗣 *Speaking — FCE*\n\n"
                "✅ *Part 1 — Interview (2 min):*\n"
                "Отвечай развёрнуто: Ответ + причина + пример\n"
                "❌ 'Yes' → ✅ 'Yes, I enjoy it because...'\n\n"
                "✅ *Part 2 — Long Turn (1 min):*\n"
                "Сравнивай фото:\n"
                "• In the first photo I can see...\n"
                "• In contrast, the second shows...\n"
                "• Both photos seem to be about...\n\n"
                "✅ *Part 3 — Discussion (3 min):*\n"
                "• What do you think about...?\n"
                "• I agree/disagree because...\n"
                "• That's a good point, but...\n\n"
                "✅ *Part 4 — Questions (4 min):*\n"
                "Расширяй ответы, давай примеры!"
            ),
            "hw": (
                "📝 *Домашнее задание — Speaking:*\n\n"
                "1. Запиши себя на 1 минуту отвечая на вопрос:\n"
                "   'What are the advantages of social media?'\n\n"
                "2. Используй минимум 5 фраз из урока\n\n"
                "3. Прослушай запись — есть ли паузы? Повторяй пока не будет плавно!\n\n"
                "💡 Полезные фразы:\n"
                "• As far as I'm concerned...\n"
                "• To be honest...\n"
                "• What I really think is..."
            ),
            "test": [
                {"q": "В Part 2 нужно:", "a": "Сравнивать два фото и отвечать на вопрос", "w": ["Читать текст вслух", "Отвечать только на вопросы экзаменатора", "Описывать только одно фото"]},
                {"q": "Как лучше ответить 'Do you like sport?'", "a": "Yes, I enjoy football because it keeps me fit.", "w": ["Yes.", "Yes I do.", "Sport is good."]},
                {"q": "Что делать если не знаешь слово во время Speaking?", "a": "Описать его: 'It's a kind of...' / 'It looks like...'", "w": ["Замолчать", "Сказать 'I don't know'", "Говорить по-русски"]},
                {"q": "Сколько минут длится Part 2?", "a": "1 минута", "w": ["2 минуты", "3 минуты", "30 секунд"]},
                {"q": "Какая фраза помогает выразить мнение?", "a": "As far as I'm concerned...", "w": ["In the first photo...", "Both photos show...", "Shall we move on?"]},
            ]
        },
    ],
    "listening": [
        {
            "name": "Listening — FCE Стратегия",
            "rule": (
                "🎧 *Listening — FCE*\n\n"
                "✅ *4 части экзамена:*\n"
                "• Part 1: 8 коротких диалогов — MCQ\n"
                "• Part 2: Монолог — заполни 10 пропусков\n"
                "• Part 3: 5 говорящих — сопоставь (8 вариантов)\n"
                "• Part 4: Интервью — MCQ (7 вопросов)\n\n"
                "✅ *Стратегия:*\n"
                "1. Читай вопросы ДО прослушивания\n"
                "2. Подчёркивай ключевые слова\n"
                "3. Слушай КОНТЕКСТ, не только слова\n\n"
                "⚠️ *Опасные слова:*\n"
                "• but, however, although → меняют смысл!\n"
                "• actually, in fact → исправление!\n"
                "• most importantly → главная идея!"
            ),
            "hw": (
                "📝 *Домашнее задание — Listening:*\n\n"
                "1. Найди на YouTube: 'BBC 6 Minute English'\n"
                "2. Послушай один выпуск\n"
                "3. Запиши 10 новых слов\n"
                "4. Послушай ещё раз с субтитрами\n"
                "5. Перескажи главную тему в 3-4 предложениях\n\n"
                "💡 Другие ресурсы:\n"
                "• TED Talks (с субтитрами)\n"
                "• Podcasts: 'All Ears English'"
            ),
            "test": [
                {"q": "Сколько частей в FCE Listening?", "a": "4", "w": ["3", "5", "6"]},
                {"q": "В Part 2 нужно:", "a": "Заполнить 10 пропусков", "w": ["Выбрать из 3 вариантов", "Сопоставить говорящих", "Ответить на вопросы"]},
                {"q": "Слово 'however' в тексте значит:", "a": "Сейчас будет контраст!", "w": ["Продолжение идеи", "Пример", "Вывод"]},
                {"q": "Что нужно делать ДО прослушивания?", "a": "Читать вопросы и подчёркивать ключевые слова", "w": ["Писать конспект", "Переводить слова", "Ничего — просто слушать"]},
                {"q": "В Part 3 нужно:", "a": "Сопоставить 5 говорящих с вариантами", "w": ["Заполнить пропуски", "Выбрать из 3 вариантов", "Написать эссе"]},
            ]
        },
    ],
}

SECTION_NAMES = {
    "grammar": "📗 Грамматика",
    "uoe": "📙 Use of English",
    "vocabulary": "📘 Словарный запас",
    "suffixes": "🔤 Суффиксы",
    "reading": "📰 Reading",
    "writing": "✏️ Writing",
    "speaking": "🗣 Speaking",
    "listening": "🎧 Listening",
}

user_stats = {}

def init_user(uid):
    if uid not in user_stats:
        user_stats[uid] = {"correct": 0, "wrong": 0}

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📗 Грамматика", callback_data="S|grammar|0"),
         InlineKeyboardButton("📙 Use of English", callback_data="S|uoe|0")],
        [InlineKeyboardButton("📘 Словарный запас", callback_data="S|vocabulary|0"),
         InlineKeyboardButton("🔤 Суффиксы", callback_data="S|suffixes|0")],
        [InlineKeyboardButton("📰 Reading", callback_data="S|reading|0"),
         InlineKeyboardButton("✏️ Writing", callback_data="S|writing|0")],
        [InlineKeyboardButton("🗣 Speaking", callback_data="S|speaking|0"),
         InlineKeyboardButton("🎧 Listening", callback_data="S|listening|0")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="STATS")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_user(update.effective_user.id)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\n\n"
        "🎓 *FCE B2 English Trainer*\n\n"
        "Выбери раздел для изучения:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    init_user(uid)
    data = query.data

    # Главное меню
    if data == "MENU":
        await query.edit_message_text(
            "Выбери раздел:",
            reply_markup=get_main_menu()
        )

    # Показать урок: S|section|lesson_index
    elif data.startswith("S|"):
        _, section, li = data.split("|")
        li = int(li)
        lessons = DATA[section]
        if li >= len(lessons):
            li = 0
        lesson = lessons[li]
        next_li = (li + 1) % len(lessons)

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"T|{section}|{li}|0")],
            [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"HW|{section}|{li}")],
            [InlineKeyboardButton("➡️ Следующий урок", callback_data=f"S|{section}|{next_li}")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")],
        ])
        await query.edit_message_text(
            lesson["rule"],
            parse_mode="Markdown",
            reply_markup=kb
        )

    # Домашнее задание: HW|section|lesson_index
    elif data.startswith("HW|"):
        _, section, li = data.split("|")
        li = int(li)
        lesson = DATA[section][li]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"T|{section}|{li}|0")],
            [InlineKeyboardButton("🔙 К уроку", callback_data=f"S|{section}|{li}")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")],
        ])
        await query.edit_message_text(
            lesson["hw"],
            parse_mode="Markdown",
            reply_markup=kb
        )

    # Вопрос теста: T|section|lesson_index|question_index
    elif data.startswith("T|"):
        _, section, li, qi = data.split("|")
        li = int(li)
        qi = int(qi)
        lesson = DATA[section][li]
        questions = lesson["test"]

        if qi >= len(questions):
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Пройти снова", callback_data=f"T|{section}|{li}|0")],
                [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"HW|{section}|{li}")],
                [InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")],
            ])
            await query.edit_message_text(
                "🎉 *Тест завершён! Молодец!*\n\nТеперь выполни домашнее задание для закрепления!",
                parse_mode="Markdown",
                reply_markup=kb
            )
            return

        q = questions[qi]
        options = [q["a"]] + q["w"]
        random.shuffle(options)

        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton(opt, callback_data=f"A|{section}|{li}|{qi}|{opt}")]
             for opt in options] +
            [[InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")]]
        )
        await query.edit_message_text(
            f"❓ *Вопрос {qi+1}/{len(questions)}*\n\n{q['q']}",
            parse_mode="Markdown",
            reply_markup=kb
        )

    # Ответ: A|section|lesson_index|question_index|chosen
    elif data.startswith("A|"):
        parts = data.split("|", 5)
        section = parts[1]
        li = int(parts[2])
        qi = int(parts[3])
        chosen = parts[4]

        q = DATA[section][li]["test"][qi]
        correct = q["a"]
        next_qi = qi + 1

        if chosen == correct:
            user_stats[uid]["correct"] += 1
            text = f"✅ *Правильно!*"
        else:
            user_stats[uid]["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct}*"

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"T|{section}|{li}|{next_qi}")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    # Статистика
    elif data == "STATS":
        s = user_stats[uid]
        total = s["correct"] + s["wrong"]
        percent = int(s["correct"] / total * 100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 *Твоя статистика:*\n\n"
            f"✅ Правильных: {s['correct']}\n"
            f"❌ Неправильных: {s['wrong']}\n"
            f"🎯 Точность: {percent}%\n\n"
            f"Продолжай заниматься! 💪",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Главное меню", callback_data="MENU")]])
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Нажми /start чтобы начать! 👇",
        reply_markup=get_main_menu()
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
