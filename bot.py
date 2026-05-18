import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

LESSONS = [
    {"sec":"Грамматика","rule":"📗 *Present Perfect vs Past Simple*\n\n✅ PP — связь с настоящим:\n• I have lost my keys.\n• She has lived here for 5 years.\n\n✅ PS — завершено в прошлом:\n• I lost my keys yesterday.\n\n⚠️ PP: already, yet, ever, never, for, since\n⚠️ PS: yesterday, ago, last year","hw":"📝 Напиши по 5 предложений PP и PS.\n\nПример PP: I have never been to London.\nПример PS: I visited Moscow last summer.","test":[{"q":"I ___ my homework already.","a":0,"opts":["have done","did","do","done"]},{"q":"She ___ to Paris in 2019.","a":0,"opts":["went","has gone","goes","have gone"]},{"q":"They ___ here for 10 years.","a":0,"opts":["have lived","lived","live","are living"]},{"q":"___ you ever tried sushi?","a":0,"opts":["Have","Did","Do","Are"]}]},
    {"sec":"Грамматика","rule":"📗 *Conditionals*\n\n✅ 1st — реальное будущее:\nIf + Present Simple → will\n• If it rains, I will stay home.\n\n✅ 2nd — нереальное настоящее:\nIf + Past Simple → would\n• If I were rich, I would travel.\n\n✅ 3rd — нереальное прошлое:\nIf + Past Perfect → would have\n• If I had studied, I would have passed.","hw":"📝 Закончи предложения:\n1. If it rains tomorrow, I will...\n2. If I were a millionaire, I would...\n3. If I had studied harder, I would have...","test":[{"q":"If it ___ tomorrow, we'll cancel.","a":0,"opts":["rains","rained","will rain","rain"]},{"q":"If I ___ you, I would apologise.","a":0,"opts":["were","am","was","be"]},{"q":"If she had studied, she ___ the exam.","a":0,"opts":["would have passed","passed","would pass","had passed"]},{"q":"If he ___ earlier, he'd have caught the train.","a":0,"opts":["had left","left","leaves","would leave"]}]},
    {"sec":"Грамматика","rule":"📗 *Passive Voice*\n\n✅ be + past participle\n\n• Present: is done\n• Past: was done\n• Future: will be done\n• Perfect: has been done\n\n✅ Используй когда не знаем кто сделал.","hw":"📝 Переведи в Passive:\n1. They build houses every year.\n2. Someone stole my bag.\n3. Scientists have discovered a new planet.","test":[{"q":"The Mona Lisa ___ by da Vinci.","a":0,"opts":["was painted","painted","has painted","is painting"]},{"q":"English ___ all over the world.","a":0,"opts":["is spoken","speaks","spoke","has spoken"]},{"q":"The results ___ tomorrow.","a":0,"opts":["will be announced","will announce","announce","are announced"]},{"q":"The letter ___ yesterday.","a":0,"opts":["was sent","sent","has sent","is sent"]}]},
    {"sec":"Use of English","rule":"📙 *Коллокации*\n\n✅ Make vs Do:\nMAKE: a decision, an effort, a mistake, progress\nDO: homework, research, damage, well\n\n✅ Have vs Take:\nHAVE: a shower, a look, fun, a rest\nTAKE: a photo, part, a break, a risk","hw":"📝 Вставь make/do/have/take:\n1. ___ a decision\n2. ___ research\n3. ___ a photo\n4. ___ fun\n5. ___ a mistake","test":[{"q":"She ___ a lot of progress this year.","a":0,"opts":["made","did","had","took"]},{"q":"Can you ___ a look at my essay?","a":0,"opts":["have","make","do","take"]},{"q":"He ___ part in the competition.","a":0,"opts":["took","made","did","had"]},{"q":"I need to ___ some research.","a":0,"opts":["do","make","have","take"]}]},
    {"sec":"Use of English","rule":"📙 *Предлоги*\n\n✅ Прилагательные + предлоги:\n• good AT sport\n• interested IN art\n• afraid OF spiders\n• responsible FOR results\n• different FROM others\n\n✅ Глаголы + предлоги:\n• depend ON\n• succeed IN\n• apologise FOR","hw":"📝 Вставь предлог:\n1. She is good ___ maths.\n2. He is afraid ___ dogs.\n3. It depends ___ weather.\n4. She succeeded ___ passing.","test":[{"q":"She is very good ___ mathematics.","a":0,"opts":["at","in","on","for"]},{"q":"He is afraid ___ spiders.","a":0,"opts":["of","from","at","about"]},{"q":"It depends ___ the weather.","a":0,"opts":["on","of","from","at"]},{"q":"She succeeded ___ passing the exam.","a":0,"opts":["in","at","on","for"]}]},
    {"sec":"Словарный запас","rule":"📘 *Описание людей*\n\n✅ Характер:\n• ambitious — амбициозный\n• reliable — надёжный\n• stubborn — упрямый\n• generous — щедрый\n• arrogant — высокомерный\n\n✅ Состояние:\n• exhausted — измотанный\n• furious — в ярости\n• anxious — тревожный","hw":"📝 Опиши своего друга используя 6 слов из урока.\n\nПример: My friend is very reliable and generous...","test":[{"q":"Надёжный = ?","a":0,"opts":["reliable","stubborn","arrogant","anxious"]},{"q":"Измотанный = ?","a":0,"opts":["exhausted","furious","ambitious","generous"]},{"q":"She felt ___ before the exam.","a":0,"opts":["anxious","furious","generous","stubborn"]},{"q":"He never gives up — he's very ___.","a":0,"opts":["ambitious","slim","exhausted","arrogant"]}]},
    {"sec":"Суффиксы","rule":"🔤 *Суффиксы*\n\n✅ Существительные:\n-tion: education\n-ment: employment\n-ness: happiness\n-ity: creativity\n\n✅ Прилагательные:\n-ful: beautiful\n-less: careless\n-able: reliable\n\n✅ Наречия:\n-ly: carefully\n\n✅ Отрицание: un-, in-, im-, dis-","hw":"📝 Образуй слова:\n1. CREATE → (noun)\n2. RELY → (adjective)\n3. HAPPY → (adverb)\n4. EMPLOY → (noun)\n5. CARE → (adjective, negative)","test":[{"q":"Her ___ (CREATIVE) was impressive.","a":0,"opts":["creativity","creation","creative","create"]},{"q":"He is a very ___ (RELY) person.","a":0,"opts":["reliable","relying","reliance","rely"]},{"q":"She spoke ___ (CAREFUL).","a":0,"opts":["carefully","careful","carefulness","careless"]},{"q":"The ___ (EMPLOY) rate is rising.","a":0,"opts":["employment","employer","employee","employ"]}]},
    {"sec":"Reading","rule":"📰 *Reading FCE*\n\n✅ Part 5 — Multiple Choice:\n1. Читай вопросы ДО текста\n2. Ищи ПЕРЕФРАЗ\n3. Исключай неверные варианты\n\n✅ Part 6 — Gapped Text:\n1. Читай весь текст\n2. Следи за местоимениями\n3. Ищи linking words\n\n✅ Part 7 — Multiple Matching:\n1. Подчёркивай ключевые слова\n2. Сканируй каждый текст","hw":"📝 Прочитай статью на BBC:\n1. Выпиши 10 новых слов\n2. Определи главную мысль каждого абзаца\n3. Перескажи в 4-5 предложениях","test":[{"q":"'Social media causes addiction and misinformation.'\n\nНегативный эффект:","a":0,"opts":["Addiction","Connectivity","Speed","Cost"]},{"q":"'The Amazon produces 20% of world oxygen. Deforestation threatens it.'\n\nЧто угрожает Амазонке?","a":0,"opts":["Deforestation","Oxygen","Animals","Climate"]},{"q":"В Part 5 нужно искать:","a":0,"opts":["Перефраз идей","Точные слова","Длинный абзац","Первое предложение"]},{"q":"В Part 6 важно следить за:","a":0,"opts":["Местоимениями и linking words","Длиной предложений","Числом абзацев","Заголовком"]}]},
    {"sec":"Writing","rule":"✏️ *Essay FCE*\n\n✅ Структура (180-190 слов):\n1. Introduction\n2. Body paragraph 1\n3. Body paragraph 2\n4. Conclusion\n\n✅ Полезные фразы:\nIntro: Nowadays...\nAdding: Furthermore,\nContrast: However,\nConclusion: In conclusion,\n\n⚠️ Формальный стиль!\n❌ don't → ✅ do not","hw":"📝 Напиши эссе (180-190 слов):\n'Technology has made our lives better.'\n\n• Introduction\n• Para 1: плюсы\n• Para 2: минусы\n• Conclusion","test":[{"q":"Какая фраза для введения?","a":0,"opts":["Nowadays, many people believe...","Hey guys...","So basically...","I wanna discuss..."]},{"q":"Слово для КОНТРАСТА:","a":0,"opts":["However","Furthermore","Moreover","In addition"]},{"q":"Что нельзя в формальном эссе?","a":0,"opts":["Сокращения (don't)","Passive voice","Linking words","Сложные предложения"]},{"q":"Как формально написать 'I think'?","a":0,"opts":["It is believed that","I feel like","In my mind","Personally"]}]},
    {"sec":"Speaking","rule":"🗣 *Speaking FCE*\n\n✅ Part 1 — Interview (2 min):\nОтвет + причина + пример\n❌ 'Yes' → ✅ 'Yes, because...'\n\n✅ Part 2 — Long Turn (1 min):\n• In the first photo I can see...\n• In contrast, the second shows...\n• Both photos seem to be about...\n\n✅ Part 3 — Discussion (3 min):\n• What do you think about...?\n• I agree because...\n• That's a good point, but...","hw":"📝 Запиши себя на 1 минуту:\n'What are advantages of social media?'\n\nИспользуй 5 фраз из урока.\nПрослушай — есть паузы? Повторяй!","test":[{"q":"В Part 2 нужно:","a":0,"opts":["Сравнивать два фото","Читать текст","Только отвечать на вопросы","Описывать одно фото"]},{"q":"Лучший ответ на 'Do you like sport?'","a":0,"opts":["Yes, I enjoy football because it keeps me fit.","Yes.","Yes I do.","Sport is good."]},{"q":"Если не знаешь слово:","a":0,"opts":["It's a kind of... / It looks like...","Замолчать","Сказать I don't know","Говорить по-русски"]},{"q":"Сколько минут Part 2?","a":0,"opts":["1 минута","2 минуты","3 минуты","30 секунд"]}]},
    {"sec":"Listening","rule":"🎧 *Listening FCE*\n\n✅ 4 части:\n• Part 1: 8 диалогов — MCQ\n• Part 2: Монолог — 10 пропусков\n• Part 3: 5 говорящих — сопоставь\n• Part 4: Интервью — MCQ\n\n✅ Стратегия:\n1. Читай вопросы ДО прослушивания\n2. Подчёркивай ключевые слова\n3. Слушай КОНТЕКСТ\n\n⚠️ but, however → меняют смысл!","hw":"📝 Найди на YouTube: 'BBC 6 Minute English'\n1. Послушай выпуск\n2. Запиши 10 новых слов\n3. Послушай с субтитрами\n4. Перескажи тему в 3-4 предложениях","test":[{"q":"Сколько частей в FCE Listening?","a":0,"opts":["4","3","5","6"]},{"q":"В Part 2 нужно:","a":0,"opts":["Заполнить 10 пропусков","Выбрать из 3 вариантов","Сопоставить говорящих","Ответить письменно"]},{"q":"Слово 'however' значит:","a":0,"opts":["Сейчас будет контраст!","Продолжение идеи","Пример","Вывод"]},{"q":"Что делать ДО прослушивания?","a":0,"opts":["Читать вопросы и ключевые слова","Писать конспект","Переводить слова","Ничего"]}]},
]

MENU_SECTIONS = ["Грамматика","Use of English","Словарный запас","Суффиксы","Reading","Writing","Speaking","Listening"]
MENU_ICONS = {"Грамматика":"📗","Use of English":"📙","Словарный запас":"📘","Суффиксы":"🔤","Reading":"📰","Writing":"✏️","Speaking":"🗣","Listening":"🎧"}

user_stats = {}

def init_user(uid):
    if uid not in user_stats:
        user_stats[uid] = {"correct": 0, "wrong": 0}

def get_lessons_by_section(sec):
    return [i for i, l in enumerate(LESSONS) if l["sec"] == sec]

def get_main_menu():
    rows = []
    for i in range(0, len(MENU_SECTIONS), 2):
        row = []
        for sec in MENU_SECTIONS[i:i+2]:
            icon = MENU_ICONS[sec]
            row.append(InlineKeyboardButton(f"{icon} {sec}", callback_data=f"M:{sec}"))
        rows.append(row)
    rows.append([InlineKeyboardButton("📊 Статистика", callback_data="STAT")])
    return InlineKeyboardMarkup(rows)

async def show_lesson(query, lesson_idx):
    lesson = LESSONS[lesson_idx]
    sec = lesson["sec"]
    idxs = get_lessons_by_section(sec)
    pos = idxs.index(lesson_idx)
    next_idx = idxs[(pos + 1) % len(idxs)]
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Начать тест", callback_data=f"Q:{lesson_idx}:0")],
        [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"HW:{lesson_idx}")],
        [InlineKeyboardButton("➡️ Следующий урок", callback_data=f"L:{next_idx}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="HOME")],
    ])
    await query.edit_message_text(lesson["rule"], parse_mode="Markdown", reply_markup=kb)

async def show_question(query, lesson_idx, qi):
    questions = LESSONS[lesson_idx]["test"]
    if qi >= len(questions):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Пройти снова", callback_data=f"Q:{lesson_idx}:0")],
            [InlineKeyboardButton("🏠 Домашнее задание", callback_data=f"HW:{lesson_idx}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="HOME")],
        ])
        await query.edit_message_text(
            "🎉 *Тест завершён! Молодец!*\n\nВыполни домашнее задание!",
            parse_mode="Markdown", reply_markup=kb
        )
        return

    q = questions[qi]
    opts = list(q["opts"])
    correct_answer = opts[q["a"]]
    random.shuffle(opts)
    new_correct_idx = opts.index(correct_answer)

    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton(o, callback_data=f"A:{lesson_idx}:{qi}:{opts.index(o)}")] for o in opts] +
        [[InlineKeyboardButton("🔙 Меню", callback_data="HOME")]]
    )
    await query.edit_message_text(
        f"❓ *Вопрос {qi+1}/{len(questions)}*\n\n{q['q']}",
        parse_mode="Markdown", reply_markup=kb
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    init_user(uid)
    data = query.data

    if data == "HOME":
        await query.edit_message_text("Выбери раздел:", reply_markup=get_main_menu())

    elif data == "STAT":
        s = user_stats[uid]
        total = s["correct"] + s["wrong"]
        pct = int(s["correct"] / total * 100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 *Статистика:*\n\n✅ Правильных: {s['correct']}\n❌ Неправильных: {s['wrong']}\n🎯 Точность: {pct}%\n\n💪 Продолжай!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="HOME")]])
        )

    elif data.startswith("M:"):
        sec = data[2:]
        idxs = get_lessons_by_section(sec)
        if idxs:
            await show_lesson(query, idxs[0])

    elif data.startswith("L:"):
        await show_lesson(query, int(data[2:]))

    elif data.startswith("HW:"):
        lesson_idx = int(data[3:])
        lesson = LESSONS[lesson_idx]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Начать тест", callback_data=f"Q:{lesson_idx}:0")],
            [InlineKeyboardButton("🔙 К уроку", callback_data=f"L:{lesson_idx}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="HOME")],
        ])
        await query.edit_message_text(lesson["hw"], parse_mode="Markdown", reply_markup=kb)

    elif data.startswith("Q:"):
        parts = data.split(":")
        await show_question(query, int(parts[1]), int(parts[2]))

    elif data.startswith("A:"):
        parts = data.split(":")
        lesson_idx = int(parts[1])
        qi = int(parts[2])
        chosen_idx = int(parts[3])
        q = LESSONS[lesson_idx]["test"][qi]
        correct_idx = q["a"]

        if chosen_idx == correct_idx:
            user_stats[uid]["correct"] += 1
            text = "✅ *Правильно!*"
        else:
            correct_answer = q["opts"][correct_idx]
            user_stats[uid]["wrong"] += 1
            text = f"❌ *Неправильно!*\n\nПравильный ответ: *{correct_answer}*"

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"Q:{lesson_idx}:{qi+1}")],
            [InlineKeyboardButton("🔙 Меню", callback_data="HOME")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_user(update.effective_user.id)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\n\n🎓 *FCE B2 English Trainer*\n\nВыбери раздел:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

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
