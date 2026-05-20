import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ⚠️ ВСТАВЬ СЮДА СВОЙ ТОКЕН ИЗ BOTFATHER
API_TOKEN = 'ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обновленная база данных (без домашних заданий)
COURSE_DATA = {
    1: {
        "title": "Unit 1: Noun Suffixes & State Verbs",
        "grammar": (
            "📚 **UNIT 1: Grammar & Suffixes**\n\n"
            "🟢 **Noun Suffixes (Суффиксы существительных):**\n"
            "На уровне B2 важно не просто знать слова, а уметь их преобразовывать:\n"
            "• `-ment`: Словесный эквивалент действия/процесса. *develop* (развивать) ➡️ *development* (развитие), *appoint* (назначать) ➡️ *appointment* (встреча/назначение).\n"
            "• `-tion / -sion`: Часто образует абстрактные понятия от глаголов. *produce* (производить) ➡️ *production* (производство), *decide* (решать) ➡️ *decision* (решение).\n"
            "• `-ness`: Показывает состояние или качество (от прилагательных). *weak* (слабый) ➡️ *weakness* (слабость), *polite* (вежливый) ➡️ *politeness* (вежливость).\n"
            "• `-ity`: Означает свойство или характеристика. *creative* (творческий) ➡️ *creativity* (творчество/креативность).\n\n"
            "🔵 **State Verbs (Глаголы состояния):**\n"
            "Глаголы, описывающие мыслительные процессы, чувства, владение чем-то, **не живут в временах Continuous** (никаких -ing!).\n"
            "Основные группы:\n"
            "1. Thoughts: *know, realize, understand, believe, remember, forget*\n"
            "2. Feelings: *love, hate, prefer, like, depend*\n"
            "3. Possession: *belong, own, possess, have* (в значении иметь)\n\n"
            "💡 **Сдвиг значения B1+/B2:**\n"
            "• I *have* a car (У меня есть машина — состояние/Simple).\n"
            "• I *am having* lunch (Я обедаю — процесс/Continuous).\n"
            "• I *think* you are right (Я считаю/это мое мнение — Simple).\n"
            "• Quiet! I *am thinking* about the answer (Я размышляю/процесс в голове — Continuous)."
        ),
        "use_of_english": (
            "✍️ **UNIT 1: Use of English & Writing**\n\n"
            "**Word Formation Guide:**\n"
            "В экзаменах (например, FCE/IELTS) вам дается текст с пропусками. На полях стоит базовое слово. Вам нужно понять, какая часть речи пропущена. Если перед пропуском стоит артикль *the* или притяжательное местоимение (*my, his*), а после нет существительного — значит, нужно образовать существительное!\n\n"
            "**Writing Part: Formal vs Informal**\n"
            "На уровне B2 в написании эссе или официальных писем ЗАПРЕЩЕНО использовать сокращения (*don't, can't, I'm*). Вместо этого пишите полностью: *do not, cannot, I am*.\n"
            "Вместо простых связок используйте продвинутые вводные слова:\n"
            "• *In addition to this...* (В дополнение к этому)\n"
            "• *Furthermore...* (Более того)\n"
            "• *On the one hand / On the other hand* (С одной стороны / С другой стороны)"
        ),
        "skills": (
            "📖 **UNIT 1: Reading & Listening**\n\n"
            "📰 **Reading Practice (B2 Text):**\n"
            "«The rapid *development* of artificial intelligence has sparked intense debates among tech experts. Many *believe* that AI will replace millions of jobs, while others argue it will enhance human *creativity*. For now, tech companies are *having* a lot of success implementing new tools, but long-term consequences remain unknown.»\n\n"
            "🔍 **Разбор текста:**\n"
            "1. *development* — существительное от глагола *develop* с помощью суффикса `-ment`.\n"
            "2. *believe* — глагол состояния (мысль), стоит в Present Simple.\n"
            "3. *creativity* — существительное от прилагательного *creative* с помощью суффикса `-ity`.\n"
            "4. *are having success* — здесь *have* означает не владение, а динамическое действие (добиваются успеха), поэтому Continuous уместен."
        ),
        "vocabulary": (
            "🧠 **UNIT 1: Vocabulary & Speaking**\n\n"
            "🔥 **Phrasal Verbs (Topic: Education & Study):**\n"
            "1. **Bring up** — поднимать вопрос / воспитывать. *Example: She brought up an interesting point during the lesson.*\n"
            "2. **Fall behind** — отставать (в учебе/графике). *Example: If you miss lessons, you will fall behind the rest of the class.*\n"
            "3. **Look into** — исследовать, изучать детали. *Example: The police are looking into the cause of the accident.*\n"
            "4. **Turn out** — оказаться в итоге. *Example: The test turned out to be much easier than I expected.*\n\n"
            "🗣️ **Speaking Practice Topic:**\n"
            "Describe an intellectual challenge you faced. You should say:\n"
            "— what the challenge was\n"
            "— how you prepared for it\n"
            "— and explain why it *turned out* to be difficult or easy for you."
        ),
        "questions": [
            {
                "q": "1/5: He looked at the painting in absolute ______.\n(Образуй существительное от глагола amaze)",
                "options": ["amazement", "amazation", "amazeness"],
                "correct": 0,
                "expl": "Суффикс -ment используется с глаголом amaze для образования существительного amazement (изумление)."
            },
            {
                "q": "2/5: Choose the grammatically CORRECT option:",
                "options": ["I am wanting to buy a new laptop.", "I want to buy a new laptop.", "I am want to buy a new laptop."],
                "correct": 1,
                "expl": "Want — глагол состояния (желание), он не употребляется во временах Continuous."
            },
            {
                "q": "3/5: What does the phrasal verb 'fall behind' mean?",
                "options": ["To drop something on the floor", "To progress slower than others", "To drop out of school entirely"],
                "correct": 1,
                "expl": "Fall behind переводится как 'отставать' от группы, графика или прогресса других людей."
            },
            {
                "q": "4/5: 'Why are you smelling the milk?' - Why is Present Continuous used here?",
                "options": ["Because it is a regular habit.", "Because smell represents an active physical action here.", "It is incorrect, smell cannot be used in Continuous."],
                "correct": 1,
                "expl": "Здесь smell — это physical action (человек намеренно нюхает молоко), а не пассивное ощущение запаха, поэтому Continuous правилен."
            },
            {
                "q": "5/5: Regular exercise can improve your overall ______.\n(Образуй слово от прилагательного fit)",
                "options": ["fittity", "fitment", "fitness"],
                "correct": 2,
                "expl": "Суффикс -ness добавляется к прилагательному fit для получения существительного fitness (хорошая физическая форма)."
            }
        ]
    },
    2: {
        "title": "Unit 2: Narrative Tenses & Adjective Suffixes",
        "grammar": (
            "📚 **UNIT 2: Grammar & Suffixes**\n\n"
            "🟢 **Adjective Suffixes (Суффиксы прилагательных):**\n"
            "• `-ive`: Образует прилагательные со значением активного свойства. *act* (действовать) ➡️ *active* (активный), *create* (творить) ➡️ *creative* (творческий).\n"
            "• `-able / -ible`: Означает возможность выполнения действия или пригодность к чему-то. *rely* (полагаться) ➡️ *reliable* (надежный), *suit* (подходить) ➡️ *suitable* (подходящий).\n"
            "• `-ful` (наличие качества) vs `-less` (отсутствие качества): *care* (забота) ➡️ *careful* (осторожный) / *careless* (беззаботный/небрежный).\n\n"
            "🔵 **Narrative Tenses (Прошедшие времена для историй):**\n"
            "Когда мы рассказываем историю или анекдот, мы красиво комбинируем 3 времени:\n"
            "1. **Past Simple** (Действия по цепочке): *He jumped out of bed, grabbed his keys and ran out.*\n"
            "2. **Past Continuous** (Длинное фоновое действие/атмосфера): *The wind was blowing, the birds were singing...*\n"
            "3. **Past Perfect** (Действие-предыстория, которое произошло ДО всей цепочки событий): *When I reached the station, the train had already left.* (Поезд уехал раньше, чем я пришел)."
        ),
        "use_of_english": (
            "✍️ **UNIT 2: Use of English & Writing**\n\n"
            "**Key Word Transformations (Задания на перефразирование):**\n"
            "Вам дано предложение и одно опорное слово крупными буквами. С его помощью нужно переписать предложение так, чтобы смысл остался прежним. На это дается от 2 до 5 слов.\n\n"
            "*Пример:* \n"
            "«We ate dinner before Mark arrived.» (HAD)\n"
            "➡️ *Ответ:* We **had already eaten** dinner when Mark arrived.\n\n"
            "**Writing Practice: Informal Letter / Email**\n"
            "В отличие от эссе, в неофициальном письме другу сокрщения ИСПОЛЬЗУЮТСЯ (*I'm, can't, don't*). Используйте разговорные связки:\n"
            "• *By the way...* (Кстати)\n"
            "• *Anyway...* (В любом случае / Короче говоря)\n"
            "• *Drop me a line soon!* (Чиркани мне пару строк!)"
        ),
        "skills": (
            "📖 **UNIT 2: Reading & Listening**\n\n"
            "📰 **Reading Text (Narrative Style B2):**\n"
            "«It was a dark, stormy night. The rain *was pouring* down outside, and Jessica *was trying* to finish her article. Suddenly, she heard a strange noise from the basement. She remembered that she *had forgotten* to lock the back door. Heart pounding, she walked down the stairs, but it *turned out* to be just her cat.»\n\n"
            "🔍 **Разбор времен в тексте:**\n"
            "• *was pouring / was trying* — фоновые процессы в момент истории (Past Continuous).\n"
            "• *heard / remembered / walked / turned out* — последовательные основные действия (Past Simple).\n"
            "• *had forgotten* — она забыла закрыть дверь еще до того, как услышала звук (Past Perfect)."
        ),
        "vocabulary": (
            "🧠 **UNIT 2: Vocabulary & Speaking**\n\n"
            "🔥 **B2 Idioms (Идиомы для яркой речи):**\n"
            "1. **See eye to eye** — полностью соглашаться. *Example: I don't see eye to eye with my boss on this strategy.*\n"
            "2. **Once in a blue moon** — безумно редко. *Example: My brother lives abroad, so he visits us once in a blue moon.*\n"
            "3. **Piece of cake** — проще простого (пустяковое дело). *Example: Don't worry about the exam, it's going to be a piece of cake.*\n"
            "4. **Cost an arm and a leg** — стоить целое состояние. *Example: This new smartphone costs an arm and a leg.*\n\n"
            "🗣 **Speaking Task:**\n"
            "Tell a story about a time when you bought something that *cost an arm and a leg*, but later you realized it wasn't *suitable* or *reliable* for you."
        ),
        "questions": [
            {
                "q": "1/5: When I arrived at the party, Sarah ______ home.",
                "options": ["already went", "had already gone", "was already going"],
                "correct": 1,
                "expl": "Сара ушла ДО того, как я пришел. Для действия, случившегося раньше другого в прошлом, нужен Past Perfect (had gone)."
            },
            {
                "q": "2/5: He is a very ______ person. You can always trust him.\n(Образуй слово от глагола rely)",
                "options": ["relyful", "reliable", "reliant"],
                "correct": 1,
                "expl": "Суффикс -able образует прилагательное reliable — надежный, тот, на кого можно положиться."
            },
            {
                "q": "3/5: What does it mean if something 'costs an arm and a leg'?",
                "options": ["It is dangerous.", "It is extremely expensive.", "It requires physical labor."],
                "correct": 1,
                "expl": "Идиома 'costs an arm and a leg' означает, что вещь стоит очень дорого (целое состояние)."
            },
            {
                "q": "4/5: While my mother ______ dinner, the lights suddenly went out.",
                "options": ["cooked", "was cooking", "had cooked"],
                "correct": 1,
                "expl": "Готовка ужина — это длительное фоновое действие в прошлом, которое прервалось коротким (went out). Нужен Past Continuous."
            },
            {
                "q": "5/5: She was so careless that she made a lot of mistakes. What does 'careless' mean?",
                "options": ["Very attentive", "Without care / negligent", "Full of worry"],
                "correct": 1,
                "expl": "Суффикс -less означает отсутствие качества. Careless — невнимательный, небрежный (без заботы)."
            }
        ]
    },
    3: {
        "title": "Unit 3: Passive Voice & Verb Suffixes",
        "grammar": (
            "📚 **UNIT 3: Grammar & Suffixes**\n\n"
            "🟢 **Verb Suffixes (Суффиксы глаголов):**\n"
            "Служат для создания глаголов от существительных и прилагательных:\n"
            "• `-ify`: Означает делать каким-то или превращать. *clear* (ясный) ➡️ *clarify* (прояснять/делать ясным), *simple* (простой) ➡️ *simplify* (упрощать).\n"
            "• `-ize / -ise`: Придавать форму, преобразовывать в состояние. *memory* (память) ➡️ *memorize* (запоминать), *social* (общественный) ➡️ *socialize* (общаться/социализироваться).\n"
            "• `-en`: Означает становиться или делать более... *short* (короткий) ➡️ *shorten* (укорачивать), *wide* (широкий) ➡️ *widen* (расширять).\n\n"
            "🔵 **Passive Voice (Пассивный залог уровня B2):**\n"
            "Мы используем пассив, когда совершающий действие объект нам неизвестен, неважен, или мы хотим звучать официально. Формула: **BE (в нужном времени) + глагол в 3-й форме (V3)**.\n\n"
            "Продвинутые формы пассива для B2:\n"
            "• **Continuous Passive** (действие происходит прямо сейчас): *The car is being repaired right now.* (Машину сейчас ремонтируют).\n"
            "• **Perfect Passive** (действие уже завершилось к текущему моменту): *The report has been sent.* (Отчет уже отправлен).\n"
            "• **Modal Passive** (с модальными глаголами): *The rules must be followed.* (Правила необходимо соблюдать)."
        ),
        "use_of_english": (
            "✍️ **UNIT 3: Use of English & Writing**\n\n"
            "**Passive Sentence Transformation:**\n"
            "На экзаменах часто просят переделать активный залог в пассивный, сохраняя видовременную форму.\n"
            "• *Active:* They are examining the project. (Present Continuous)\n"
            "• *Passive:* The project **is being examined**. (Present Continuous Passive)\n\n"
            "• *Active:* They have canceled the match. (Present Perfect)\n"
            "• *Passive:* The match **has been canceled**. (Present Perfect Passive)\n\n"
            "**Writing Tip: Formal Reports**\n"
            "В официальных отчетах пассивный залог является основным стилем повествования, так как он убирает личные местоимения *I, We*. Вместо «We discovered that...» пишите: «It was discovered that...»."
        ),
        "skills": (
            "📖 **UNIT 3: Reading & Listening**\n\n"
            "📰 **Reading Text (Official News B2):**\n"
            "«New security measures *have been introduced* at the airport today. Passports *are being checked* by automated scanners to *shorten* waiting lines. Officials state that all luggage *must be scanned* before boarding. These changes *were finalized* last week after a brief review.»\n\n"
            "🔍 **Анализ пассива:**\n"
            "• *have been introduced* — Present Perfect Passive (уже ввели, важен результат).\n"
            "• *are being checked* — Present Continuous Passive (прямо сейчас проверяются в данный период времени).\n"
            "• *must be scanned* — Modal Passive (должны быть отсканированы).\n"
            "• *were finalized* — Past Simple Passive (были утверждены на прошлой неделе)."
        ),
        "vocabulary": (
            "🧠 **UNIT 3: Vocabulary & Speaking**\n\n"
            "🔥 **Advanced Collocations (Устойчивые словосочетания B2):**\n"
            "1. **Make an effort** — приложить усилия. *Example: You need to make an effort if you want to pass B2.*\n"
            "2. **Take advantage of** — воспользоваться моментом/преимуществом. *Example: You should take advantage of this free course.*\n"
            "3. **Do your best** — сделать всё возможное. *Example: Don't panic, just do your best in the test.*\n"
            "4. **Change your mind** — передумать, поменять решение. *Example: I was going to stay home, but I changed my mind.*\n\n"
            "🗣 **Speaking Practice:**\n"
            "Talk about an important decision you made. Did you *change your mind* later? Did you *take advantage of* someone's advice? Speak for 1.5 minutes."
        ),
        "questions": [
            {
                "q": "1/5: Active: 'They are building a school.' -> Passive:",
                "options": ["A school is built.", "A school is being built.", "A school has been built."],
                "correct": 1,
                "expl": "В оригинале Present Continuous (are building), значит в пассиве будет форма 'is/are being + V3'."
            },
            {
                "q": "2/5: Could you please ______ your answer? It's not quite clear.\n(Образуй глагол от прилагательного clear)",
                "options": ["clearize", "clearen", "clarify"],
                "correct": 2,
                "expl": "Суффикс -ify используется для образования глагола clarify — прояснить, внести ясность."
            },
            {
                "q": "3/5: All homework assignments ______ before Friday.",
                "options": ["must check", "must be checked", "must being checked"],
                "correct": 1,
                "expl": "После модальных глаголов пассив строится по формуле modal + be + V3 (must be checked)."
            },
            {
                "q": "4/5: I was going to move out, but at the last moment I ______ my mind.",
                "options": ["made", "took", "changed"],
                "correct": 2,
                "expl": "Устойчивое выражение 'change your mind' переводится как 'передумать, изменить решение'."
            },
            {
                "q": "5/5: We need to ______ the old wooden door so the car can pass.\n(Образуй глагол от прилагательного wide - широкий)",
                "options": ["widen", "widify", "wideize"],
                "correct": 0,
                "expl": "Суффикс -en добавляется к некоторым прилагательным для значения 'делать шире/больше' -> widen (расширять)."
            }
        ]
    }
}

# Сессии пользователей
user_units = {}         # Текущий юнит юзера {user_id: unit_number}
user_test_progress = {} # На каком вопросе теста сейчас юзер {user_id: question_index}
user_test_score = {}    # Счет правильных ответов {user_id: correct_count}

def get_user_unit(user_id):
    return user_units.get(user_id, 1)

# Главное меню (КНОПКА ДЗ ПОЛНОСТЬЮ УБРАНА)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Изучать Теорию (Grammar & Suffixes)")],
        [KeyboardButton(text="🧠 Use of English & Vocabulary"), KeyboardButton(text="🎧 Reading & Listening")],
        [KeyboardButton(text="📝 Пройти Тест из 5 вопросов")],
        [KeyboardButton(text="🔄 Сменить / Выбрать Урок")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_units[user_id] = 1
    user_test_progress[user_id] = -1 
    
    await message.answer(
        f"Hi {message.from_user.first_name}! 👋\n"
        "Добро пожаловать в мега-курс английского языка уровня B1+/B2.\n\n"
        "Меню обновлено, лишние кнопки убраны. Приятного обучения!\n\n"
        "Текущий класс: **Unit 1**.",
        reply_markup=main_menu
    )

# Кнопка: Выбор урока
@dp.message(lambda message: message.text == "🔄 Сменить / Выбрать Урок")
async def choose_unit(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Unit 1: Noun Suffixes & States", callback_data="set_unit_1")],
        [InlineKeyboardButton(text="Unit 2: Narrative & Adjectives", callback_data="set_unit_2")],
        [InlineKeyboardButton(text="Unit 3: Passive Voice & Verbs", callback_data="set_unit_3")]
    ])
    await message.answer("Выбери интересующий тебя урок из списка ниже:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('set_unit_'))
async def process_unit_change(callback_query: types.CallbackQuery):
    unit_num = int(callback_query.data.split('_')[-1])
    user_id = callback_query.from_user.id
    user_units[user_id] = unit_num
    user_test_progress[user_id] = -1 
    
    await bot.answer_callback_query(callback_query.id)
    
    # Кнопка перехода на следующий юнит в конце теста
    if unit_num < 3:
        next_unit_btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Открыть Unit {unit_num+1} 🔓", callback_data=f"set_unit_{unit_num+1}")]
        ])
    else:
        next_unit_btn = None

    await bot.send_message(
        user_id,
        f"✅ Успешно переключено на **{COURSE_DATA[unit_num]['title']}**!\n"
        "Материалы и тесты обновлены. Можешь приступать!",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )

# Блок: Грамматика
@dp.message(lambda message: message.text == "📖 Изучать Теорию (Grammar & Suffixes)")
async def show_grammar(message: types.Message):
    unit = get_user_unit(message.from_user.id)
    text = COURSE_DATA[unit]["grammar"]
    next_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к Use of English ➡️", callback_data="go_use_of_english")]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=next_btn)

# Блок: Use of English & Лексика
@dp.message(lambda message: message.text == "🧠 Use of English & Vocabulary")
async def show_vocab(message: types.Message):
    unit = get_user_unit(message.from_user.id)
    text = f"{COURSE_DATA[unit]['use_of_english']}\n\n---\n\n{COURSE_DATA[unit]['vocabulary']}"
    next_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к Reading & Listening ➡️", callback_data="go_skills")]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=next_btn)

# Блок: Чтение и аудирование
@dp.message(lambda message: message.text == "🎧 Reading & Listening")
async def show_skills(message: types.Message):
    unit = get_user_unit(message.from_user.id)
    text = COURSE_DATA[unit]["skills"]
    next_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Начать тест из 5 вопросов ➡️", callback_data="go_test")]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=next_btn)

# --- ЛОГИКА ТЕСТА ИЗ 5 ВОПРОСОВ ---
@dp.message(lambda message: message.text == "📝 Пройти Тест из 5 вопросов")
async def start_test_command(message: types.Message):
    user_id = message.from_user.id
    user_test_progress[user_id] = 0 
    user_test_score[user_id] = 0    
    await send_next_question(user_id, message.chat.id)

async def send_next_question(user_id, chat_id):
    unit = get_user_unit(user_id)
    q_index = user_test_progress[user_id]
    questions = COURSE_DATA[unit]["questions"]
    
    if q_index < len(questions):
        q_data = questions[q_index]
        buttons = []
        for i, option in enumerate(q_data["options"]):
            buttons.append([InlineKeyboardButton(text=option, callback_data=f"ans_{i}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await bot.send_message(chat_id, f"❓ **Вопрос {q_data['q']}**", reply_markup=keyboard, parse_mode="Markdown")
    else:
        score = user_test_score[user_id]
        
        # Вместо ДЗ теперь предлагаем сразу открыть следующий юнит, если он есть
        if unit < 3:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"Открыть Unit {unit+1} 🔓", callback_data=f"set_unit_{unit+1}")]
            ])
        else:
            keyboard = None
            
        await bot.send_message(
            chat_id, 
            f"🎉 **Тест по Unit {unit} завершен!**\n"
            f"Твой результат: **{score} из 5** правильных ответов.\n\n"
            "Отличная работа!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        user_test_progress[user_id] = -1

@dp.callback_query(lambda c: c.data.startswith('ans_'))
async def handle_answer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    q_index = user_test_progress.get(user_id, -1)
    
    if q_index == -1:
        await bot.answer_callback_query(callback_query.id, "Тест еще не запущен или уже пройден.")
        return
        
    unit = get_user_unit(user_id)
    questions = COURSE_DATA[unit]["questions"]
    q_data = questions[q_index]
    
    selected_ans = int(callback_query.data.split('_')[-1])
    
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=callback_query.message.message_id, reply_markup=None)
    
    if selected_ans == q_data["correct"]:
        user_test_score[user_id] += 1
        await bot.send_message(chat_id, f"🟢 **Правильно!**\n💡 {q_data['expl']}", parse_mode="Markdown")
    else:
        correct_text = q_data["options"][q_data["correct"]]
        await bot.send_message(chat_id, f"🔴 **Ошибка!**\nПравильный ответ: *{correct_text}*\n\n💡 {q_data['expl']}", parse_mode="Markdown")
    
    user_test_progress[user_id] += 1
    await asyncio.sleep(1)
    await send_next_question(user_id, chat_id)
    await bot.answer_callback_query(callback_query.id)

# Навигация внутри inline-ссылок (связка разделов)
@dp.callback_query(lambda c: c.data.startswith('go_'))
async def process_navigation(callback_query: types.CallbackQuery):
    action = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    
    if action == "go_use_of_english":
        await show_vocab(callback_query.message)
    elif action == "go_skills":
        await show_skills(callback_query.message)
    elif action == "go_test":
        await start_test_command(callback_query.message)

async def main():
    print("Бот успешно обновлен на Railway (версия без ДЗ)!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
