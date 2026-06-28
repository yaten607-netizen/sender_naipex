import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Импортируем инициализацию базы данных из нашего файла database.py
from database import init_db

BOT_TOKEN = "8973718655:AAEJLZCO4z1SIRnBAiudnZ8EZrj5D-D8SqI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ (Кнопки внизу экрана) ---

# Выбор языка (Reply-кнопки внизу)
def get_language_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🇷🇺 Русский"))
    builder.add(types.KeyboardButton(text="🇬🇧 English"))
    builder.adjust(1) # Кнопки будут одна под другой
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Главное меню (в два столбца)
def get_main_menu(lang: str):
    builder = ReplyKeyboardBuilder()
    
    if lang == "rus":
        builder.add(types.KeyboardButton(text="🚀 Авто рассылка"))
        builder.add(types.KeyboardButton(text="📝 Текст сообщения"))
        builder.add(types.KeyboardButton(text="⏱ Интервал"))
        builder.add(types.KeyboardButton(text="💬 Настройка групп"))
        builder.add(types.KeyboardButton(text="👤 Профили"))
        builder.add(types.KeyboardButton(text="👑 Про тариф"))
        builder.add(types.KeyboardButton(text="🆔 Кабинет"))
        builder.add(types.KeyboardButton(text="⚙️ Настройки"))
    else:
        builder.add(types.KeyboardButton(text="🚀 Auto Spammer"))
        builder.add(types.KeyboardButton(text="📝 Message Text"))
        builder.add(types.KeyboardButton(text="⏱ Delay/Interval"))
        builder.add(types.KeyboardButton(text="💬 Group Settings"))
        builder.add(types.KeyboardButton(text="👤 Profiles"))
        builder.add(types.KeyboardButton(text="👑 Pro Tariff"))
        builder.add(types.KeyboardButton(text="🆔 Cabinet"))
        builder.add(types.KeyboardButton(text="⚙️ Settings"))
        
    builder.adjust(2) # Строго по 2 кнопки в ряд
    return builder.as_markup(resize_keyboard=True)


# --- ХЭНДЛЕРЫ ---

# Старт бота (Русский язык сверху, Английский снизу)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Добро пожаловать в ApexSend!**\n"
        "Прогрессивная мультиязычная платформа для автоматизации рассылок и масштабирования трафика.\n\n"
        "Пожалуйста, выберите язык ниже на кнопках:\n"
        "-------------------------------------\n"
        "🚀 **Welcome to ApexSend!**\n"
        "The ultimate multi-language platform for automated Telegram outreach and traffic growth.\n\n"
        "Please choose your language using the buttons below:",
        reply_markup=get_language_keyboard(),
        parse_mode="Markdown"
    )

# Обработка нажатия на кнопку "Русский"
@dp.message(F.text == "🇷🇺 Русский")
async def process_rus_lang(message: types.Message):
    await message.answer(
        "🤖 **Главное меню ApexSend**\n\n"
        "Платформа успешно запущена и готова к работе. Выберите нужное действие на панели внизу:",
        reply_markup=get_main_menu("rus"),
        parse_mode="Markdown"
    )

# Обработка нажатия на кнопку "English"
@dp.message(F.text == "🇬🇧 English")
async def process_eng_lang(message: types.Message):
    await message.answer(
        "🤖 **ApexSend Main Menu**\n\n"
        "The platform is successfully launched and ready. Choose an action on the panel below:",
        reply_markup=get_main_menu("eng"),
        parse_mode="Markdown"
    )

# Отлов всех остальных кнопок меню, чтобы бот реагировал текстом
@dp.message()
async def process_menu_clicks(message: types.Message):
    if message.text not in ["/start", "🇷🇺 Русский", "🇬🇧 English"]:
        await message.answer("Эта функция сейчас находится в процессе разработки! 😉")


# --- ЗАПУСК ---
async def main():
    # Запускаем создание папки и таблиц базы данных перед стартом самого бота
    init_db() 
    
    print("[+] Панель управления ApexSend успешно запущена на Railway!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
