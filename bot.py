import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ====================================
# TOKEN
# ====================================

TOKEN = "8850167918:AAF0a6ubRqC7oAsWpt-0oCvzGBfOlwjqDCs"


bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====================================
# MENU
# ====================================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📘 Grammar"),
            KeyboardButton(text="📚 Vocabulary")
        ],
        [
            KeyboardButton(text="🧠 Use of English"),
            KeyboardButton(text="📝 Writing")
        ],
        [
            KeyboardButton(text="🎧 Listening"),
            KeyboardButton(text="🗣 Speaking")
        ],
        [
            KeyboardButton(text="📖 Reading"),
            KeyboardButton(text="🔤 Suffixes")
        ],
        [
            KeyboardButton(text="🏠 Homework"),
            KeyboardButton(text="✅ Tests")
        ]
    ],
    resize_keyboard=True
)

# ====================================
# START
# ====================================

@dp.message(CommandStart())
async def start(message: Message):

    text = f"""
🇬🇧 Welcome, {message.from_user.first_name}!

English Learning Bot
Level: B1+ / B2

Choose a section 👇
"""

    await message.answer(text, reply_markup=main_menu)

# ====================================
# GRAMMAR
# ====================================

@dp.message(F.text == "📘 Grammar")
async def grammar(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Start Grammar Test",
                    callback_data="grammar_test"
                )
            ]
        ]
    )

    text = """
📘 PRESENT PERFECT

RULE:
have/has + V3

EXAMPLES:
• I have finished my homework.
• She has visited London.

USE:
1. Experience
2. Result
3. Unfinished time

WORDS:
already, just, yet, ever, never
"""

    await message.answer(text, reply_markup=keyboard)

# ====================================
# VOCABULARY
# ====================================

@dp.message(F.text == "📚 Vocabulary")
async def vocabulary(message: Message):

    text = """
📚 TRAVEL VOCABULARY

1. Journey — путешествие
2. Destination — место назначения
3. Accommodation — жильё
4. Departure — отправление
5. Sightseeing — осмотр города

TASK:
Make 3 sentences using these words.
"""

    await message.answer(text)

# ====================================
# USE OF ENGLISH
# ====================================

@dp.message(F.text == "🧠 Use of English")
async def use_english(message: Message):

    text = """
🧠 USE OF ENGLISH

Choose the correct answer:

She ____ to Paris last year.

A) go
B) went
C) gone
"""

    await message.answer(text)

# ====================================
# WRITING
# ====================================

@dp.message(F.text == "📝 Writing")
async def writing(message: Message):

    text = """
📝 WRITING TASK

Topic:
Should students study online?

Write:
• introduction
• arguments
• conclusion

120–180 words
"""

    await message.answer(text)

# ====================================
# LISTENING
# ====================================

@dp.message(F.text == "🎧 Listening")
async def listening(message: Message):

    text = """
🎧 LISTENING

Watch:
https://youtu.be/H14bBuluwB8

QUESTIONS:
1. What is the topic?
2. What words did you hear?
3. Summarize the video.
"""

    await message.answer(text)

# ====================================
# SPEAKING
# ====================================

@dp.message(F.text == "🗣 Speaking")
async def speaking(message: Message):

    text = """
🗣 SPEAKING TASK

Describe your dream holiday.

Speak for 1–2 minutes.

Use:
• past experiences
• future plans
• opinions
"""

    await message.answer(text)

# ====================================
# READING
# ====================================

@dp.message(F.text == "📖 Reading")
async def reading(message: Message):

    text = """
📖 READING

Tom had always dreamed of visiting Canada.
One day he finally bought a ticket...

QUESTIONS:
1. What was Tom's dream?
2. Where did he go?
3. Why was he excited?
"""

    await message.answer(text)

# ====================================
# SUFFIXES
# ====================================

@dp.message(F.text == "🔤 Suffixes")
async def suffixes(message: Message):

    text = """
🔤 SUFFIXES

-ful
care → careful

-less
hope → hopeless

-ment
develop → development

TASK:
Create 5 new words.
"""

    await message.answer(text)

# ====================================
# HOMEWORK
# ====================================

@dp.message(F.text == "🏠 Homework")
async def homework(message: Message):

    text = """
🏠 HOMEWORK

1. Learn 10 words
2. Write an essay
3. Complete grammar exercises
4. Practice speaking
"""

    await message.answer(text)

# ====================================
# TESTS
# ====================================

@dp.message(F.text == "✅ Tests")
async def tests(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Answer: B",
                    callback_data="correct"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Answer: A",
                    callback_data="wrong"
                )
            ]
        ]
    )

    text = """
✅ TEST

If I ____ more money, I would travel more.

A) have
B) had
C) will have
"""

    await message.answer(text, reply_markup=keyboard)

# ====================================
# CALLBACKS
# ====================================

@dp.callback_query(F.data == "grammar_test")
async def grammar_test(callback):

    await callback.message.answer(
        """
📘 MINI TEST

She ____ already eaten.

A) have
B) has
C) had
"""
    )

    await callback.answer()

@dp.callback_query(F.data == "correct")
async def correct(callback):

    await callback.message.answer(
        "✅ Correct!"
    )

    await callback.answer()

@dp.callback_query(F.data == "wrong")
async def wrong(callback):

    await callback.message.answer(
        "❌ Wrong answer!"
    )

    await callback.answer()

# ====================================
# RUN BOT
# ====================================

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
