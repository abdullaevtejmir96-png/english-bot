import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"

# ===== GRAMMAR =====
GRAMMAR = [
    {"q": "She ___ to school every day.", "options": ["go", "goes", "going", "gone"], "a": "goes", "exp": "Third person singular: he/she/it + goes"},
    {"q": "By the time he arrived, she ___ already left.", "options": ["has", "had", "have", "was"], "a": "had", "exp": "Past Perfect: had + past participle"},
    {"q": "I wish I ___ more time to study.", "options": ["have", "had", "has", "having"], "a": "had", "exp": "Wish + Past Simple для нереального желания"},
    {"q": "If I ___ you, I would apologise.", "options": ["am", "was", "were", "be"], "a": "were", "exp": "Second conditional: If I were you..."},
    {"q": "She suggested ___ to the cinema.", "options": ["go", "to go", "going", "went"], "a": "going", "exp": "suggest + verb-ing"},
    {"q": "He made me ___ the dishes.", "options": ["wash", "to wash", "washing", "washed"], "a": "wash", "exp": "make someone do (без to)"},
    {"q": "The book ___ by Tolkien.", "options": ["write", "wrote", "was written", "has write"], "a": "was written", "exp": "Passive voice: was/were + past participle"},
    {"q": "I haven't seen her ___ Monday.", "options": ["for", "since", "ago", "during"], "a": "since", "exp": "since — с конкретного момента времени"},
    {"q": "They ___ in London for 5 years.", "options": ["live", "lived", "have lived", "are living"], "a": "have lived", "exp": "Present Perfect с for для незавершённого действия"},
    {"q": "Despite ___ tired, she continued working.", "options": ["be", "been", "being", "was"], "a": "being", "exp": "Despite + verb-ing"},
]

# ===== VOCABULARY =====
VOCABULARY = [
    {"q": "Choose the correct word: The politician gave a ___ speech.", "options": ["persuasive", "persuading", "persuaded", "persuasion"], "a": "persuasive", "exp": "persuasive = убедительный (прилагательное)"},
    {"q": "She has a ___ for languages.", "options": ["talent", "talented", "talently", "talenting"], "a": "talent", "exp": "talent = талант (существительное)"},
    {"q": "The new law will ___ next month.", "options": ["come into force", "come to force", "go into force", "put into force"], "a": "come into force", "exp": "come into force = вступить в силу"},
    {"q": "He was ___ for the mistake.", "options": ["blamed", "fault", "guilty of", "responsible"], "a": "blamed", "exp": "be blamed for = быть обвинённым в чём-то"},
    {"q": "The company went ___.", "options": ["bankrupt", "bankruptcy", "bankrupted", "bankruptly"], "a": "bankrupt", "exp": "go bankrupt = обанкротиться"},
    {"q": "She ___ a living as a teacher.", "options": ["makes", "earns", "does", "gets"], "a": "earns", "exp": "earn a living = зарабатывать на жизнь"},
    {"q": "The film had a ___ effect on me.", "options": ["profound", "profoundly", "profoundness", "profounder"], "a": "profound", "exp": "profound = глубокий, сильный (прилагательное)"},
    {"q": "He ___ up his mind to quit.", "options": ["made", "did", "took", "set"], "a": "made", "exp": "make up your mind = принять решение"},
]

# ===== USE OF ENGLISH =====
USE_OF_ENGLISH = [
    {"q": "Complete: She is ___ interested in art.", "options": ["deeply", "deeply", "high", "strongly"], "a": "deeply", "exp": "deeply interested — коллокация"},
    {"q": "Word formation: The ___ (decide) was difficult.", "options": ["decide", "decision", "decisive", "decided"], "a": "decision", "exp": "decision = существительное от decide"},
    {"q": "Key word transformation: 'I started learning English 5 years ago.' → 'I ___ English for 5 years.'", "options": ["have been learning", "learned", "was learning", "am learning"], "a": "have been learning", "exp": "Present Perfect Continuous для действия, начавшегося в прошлом"},
    {"q": "Choose the correct collocation: ___ a decision", "options": ["make", "do", "take", "have"], "a": "make", "exp": "make a decision — устойчивое словосочетание"},
    {"q": "Fill in: He succeeded ___ passing the exam.", "options": ["in", "at", "on", "for"], "a": "in", "exp": "succeed in + verb-ing"},
    {"q": "Choose: She is very good ___ mathematics.", "options": ["in", "at", "on", "for"], "a": "at", "exp": "good at — коллокация с предлогом"},
]

# ===== SUFFIXES =====
SUFFIXES = [
    {"q": "Form a noun from: EMPLOY", "options": ["employment", "employful", "employness", "employing"], "a": "employment", "exp": "-ment: employment = занятость"},
    {"q": "Form an adjective from: RELY", "options": ["relyful", "reliable", "relying", "reliance"], "a": "reliable", "exp": "-able: reliable = надёжный"},
    {"q": "Form a noun from: HAPPY", "options": ["happiness", "happily", "happiful", "happiment"], "a": "happiness", "exp": "-ness: happiness = счастье"},
    {"q": "Form an adverb from: CAREFUL", "options": ["carefully", "carefulness", "carefulment", "caring"], "a": "carefully", "exp": "-ly: carefully = осторожно"},
    {"q": "Form a noun from: CURIOUS", "options": ["curiousness", "curiosity", "curiously", "curiousful"], "a": "curiosity", "exp": "-ity: curiosity = любопытство"},
    {"q": "Form an adjective from: BEAUTY", "options": ["beautious", "beautiful", "beautify", "beautifully"], "a": "beautiful", "exp": "-ful: beautiful = красивый"},
    {"q": "Form a noun from: ACHIEVE", "options": ["achievement", "achievable", "achieving", "achieveness"], "a": "achievement", "exp": "-ment: achievement = достижение"},
]

# ===== READING =====
READING = [
    {
        "text": "Climate change is one of the most pressing issues of our time. Scientists agree that human activities, particularly the burning of fossil fuels, have significantly increased greenhouse gas emissions. This has led to rising temperatures, melting ice caps, and more frequent extreme weather events.",
        "q": "According to the text, what is the main cause of climate change?",
        "options": ["Natural disasters", "Human activities", "Ice caps melting", "Weather changes"],
        "a": "Human activities",
        "exp": "Текст говорит: 'human activities, particularly the burning of fossil fuels'"
    },
    {
        "text": "Social media has transformed the way people communicate. While it offers many benefits such as instant communication and global connectivity, it also has drawbacks including addiction, privacy concerns, and the spread of misinformation.",
        "q": "Which of these is NOT mentioned as a drawback of social media?",
        "options": ["Addiction", "High cost", "Privacy concerns", "Misinformation"],
        "a": "High cost",
        "exp": "В тексте упоминаются addiction, privacy concerns, misinformation — но не высокая стоимость"
    },
    {
        "text": "The Renaissance was a period of great cultural and intellectual activity in Europe, roughly from the 14th to the 17th century. It began in Italy and spread throughout Europe, leading to revolutionary changes in art, science, and philosophy.",
        "q": "Where did the Renaissance begin?",
        "options": ["France", "England", "Italy", "Germany"],
        "a": "Italy",
        "exp": "Текст: 'It began in Italy'"
    },
]

# ===== WRITING TIPS =====
WRITING_TIPS = [
    "📝 *Essay structure:*\n\nIntroduction → 2-3 Body paragraphs → Conclusion\n\nВсегда начинай с чёткого тезиса!",
    "📝 *Linking words:*\n\nAddition: Furthermore, Moreover, In addition\nContrast: However, Nevertheless, On the other hand\nResult: Therefore, Consequently, As a result",
    "📝 *Formal email:*\n\nDear Sir/Madam,\nI am writing to...\nI would be grateful if...\nYours faithfully,",
    "📝 *Opinion essay:*\n\nIn my opinion...\nI strongly believe that...\nIt seems to me that...\nFrom my perspective...",
    "📝 *Избегай в formal writing:*\n\n❌ contractions (don't → do not)\n❌ slang\n❌ short sentences\n✅ Используй passive voice\n✅ Академическая лексика",
]

# ===== SPEAKING TIPS =====
SPEAKING_TIPS = [
    "🗣 *Part 1 — Interview:*\n\nОтвечай развёрнуто! Не просто 'Yes' или 'No'.\n\nПример: 'Do you like sport?'\n❌ 'Yes'\n✅ 'Yes, I really enjoy playing football. I play twice a week because it keeps me fit.'",
    "🗣 *Part 2 — Long turn:*\n\nУ тебя 1 минута. Структура:\n1. Describe what you see\n2. Compare the photos\n3. Answer the question\n\nПолезные фразы:\n• In the first photo I can see...\n• Compared to the first photo...\n• Both photos show...",
    "🗣 *Part 3 — Discussion:*\n\nОбсуждай с партнёром! Полезные фразы:\n• What do you think about...?\n• I agree with you because...\n• That's a good point, but...\n• Shall we move on to...?",
    "🗣 *Полезные фразы для FCE Speaking:*\n\n• What I mean is...\n• As far as I know...\n• It depends on...\n• On the whole...\n• To be honest...",
]

# ===== LISTENING TIPS =====
LISTENING_TIPS = [
    "🎧 *FCE Listening советы:*\n\n1. Читай вопросы ДО прослушивания\n2. Подчёркивай ключевые слова\n3. Слушай контекст, не только отдельные слова\n4. Не паникуй если пропустил — слушай дальше",
    "🎧 *Типы заданий Listening:*\n\n• Part 1: 8 коротких диалогов (MCQ)\n• Part 2: Monologue — заполни пропуски\n• Part 3: 5 говорящих — сопоставь\n• Part 4: Interview — MCQ",
    "🎧 *Ключевые слова для listening:*\n\nОбращай внимание на:\n• however, but, although (контраст!)\n• actually, in fact (исправление!)\n• most importantly (главное!)",
]

user_stats = {}

def init_user(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {
            "correct": 0, "wrong": 0,
            "grammar_q": list(range(len(GRAMMAR))),
            "vocab_q": list(range(len(VOCABULARY))),
            "uoe_q": list(range(len(USE_OF_ENGLISH))),
            "suffix_q": list(range(len(SUFFIXES))),
            "reading_q": list(range(len(READING))),
        }
        random.shuffle(user_stats[user_id]["grammar_q"])
        random.shuffle(user_stats[user_id]["vocab_q"])
        random.shuffle(user_stats[user_id]["uoe_q"])
        random.shuffle(user_stats[user_id]["suffix_q"])
        random.shuffle(user_stats[user_id]["reading_q"])

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Grammar", callback_data="grammar"),
         InlineKeyboardButton("📖 Vocabulary", callback_data="vocabulary")],
        [InlineKeyboardButton("✍️ Use of English", callback_data="uoe"),
         InlineKeyboardButton("🔤 Suffixes", callback_data="suffixes")],
        [InlineKeyboardButton("📰 Reading", callback_data="reading")],
        [InlineKeyboardButton("🎧 Listening tips", callback_data="listening"),
         InlineKeyboardButton("🗣 Speaking tips", callback_data="speaking")],
        [InlineKeyboardButton("✏️ Writing tips", callback_data="writing")],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    init_user(user.id)
    await update.message.reply_text(
        f"Hello, {user.first_name}! 👋\n\n"
        f"Welcome to your *FCE B2 English Trainer*! 🎓\n\n"
        f"Choose a section to practise:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def send_question(query, context, section, data_list, key):
    user_id = query.from_user.id
    init_user(user_id)

    queue_key = f"{key}_q"
    if not user_stats[user_id][queue_key]:
        user_stats[user_id][queue_key] = list(range(len(data_list)))
        random.shuffle(user_stats[user_id][queue_key])
        await query.edit_message_text(
            "🎉 You've completed all questions in this section! Starting over...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Continue ▶️", callback_data=section)]])
        )
        return

    idx = user_stats[user_id][queue_key].pop(0)
    item = data_list[idx]
    context.user_data["current_section"] = section
    context.user_data["current_answer"] = item["a"]
    context.user_data["current_exp"] = item["exp"]

    options = item["options"][:]
    random.shuffle(options)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(opt, callback_data=f"ans_{opt}")] for opt in options] +
        [[InlineKeyboardButton("🔙 Main Menu", callback_data="menu")]]
    )

    text = f"*{section.upper()}*\n\n{item['q']}"
    if "text" in item:
        text = f"*{section.upper()} — Reading*\n\n📄 {item['text']}\n\n❓ {item['q']}"

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    init_user(user_id)
    data = query.data

    if data == "menu":
        context.user_data["current_section"] = None
        await query.edit_message_text("Choose a section:", reply_markup=get_main_menu())

    elif data == "grammar":
        await send_question(query, context, "grammar", GRAMMAR, "grammar")

    elif data == "vocabulary":
        await send_question(query, context, "vocabulary", VOCABULARY, "vocab")

    elif data == "uoe":
        await send_question(query, context, "uoe", USE_OF_ENGLISH, "uoe")

    elif data == "suffixes":
        await send_question(query, context, "suffixes", SUFFIXES, "suffix")

    elif data == "reading":
        await send_question(query, context, "reading", READING, "reading")

    elif data == "listening":
        tip = random.choice(LISTENING_TIPS)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Another tip", callback_data="listening")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")],
        ])
        await query.edit_message_text(tip, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "speaking":
        tip = random.choice(SPEAKING_TIPS)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Another tip", callback_data="speaking")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")],
        ])
        await query.edit_message_text(tip, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "writing":
        tip = random.choice(WRITING_TIPS)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Another tip", callback_data="writing")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")],
        ])
        await query.edit_message_text(tip, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "stats":
        s = user_stats[user_id]
        total = s["correct"] + s["wrong"]
        percent = int(s["correct"] / total * 100) if total > 0 else 0
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Main Menu", callback_data="menu")]])
        await query.edit_message_text(
            f"📊 *Your FCE Statistics:*\n\n"
            f"✅ Correct: {s['correct']}\n"
            f"❌ Wrong: {s['wrong']}\n"
            f"🎯 Accuracy: {percent}%\n\n"
            f"Keep practising! 💪",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    elif data.startswith("ans_"):
        chosen = data.replace("ans_", "")
        correct = context.user_data.get("current_answer", "")
        exp = context.user_data.get("current_exp", "")
        section = context.user_data.get("current_section", "grammar")

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Next question", callback_data=section)],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")],
        ])

        if chosen == correct:
            user_stats[user_id]["correct"] += 1
            text = f"✅ *Correct!*\n\n💡 {exp}"
        else:
            user_stats[user_id]["wrong"] += 1
            text = f"❌ *Wrong!*\n\nCorrect answer: *{correct}*\n\n💡 {exp}"

        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use the buttons to navigate! 👇\nPress /start to begin.",
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
