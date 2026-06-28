import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# Токены и доступы
BOT_TOKEN = "8973718655:AAEJLZCO4z1SIRnBAiudnZ8EZrj5D-D8SqI"
API_ID = 38973104
API_HASH = "2edbb6059c7cba62860eb638e0508793"

bot = Bot(token=BOT_TOKEN)
# Используем MemoryStorage для хранения состояний (номеров/кодов) в памяти
dp = Dispatcher(storage=MemoryStorage())

# Временное хранилище запущенных клиентов Pyrogram, чтобы передавать их между шагами
active_clients = {}

# Описываем состояния для пошагового ввода данных
class AddAccountState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()
    waiting_for_password = State()

# --- КЛАВИАТУРЫ ---

# 1. Выбор языка
def get_language_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🇷🇺 Русский"))
    builder.add(types.KeyboardButton(text="🇬🇧 English"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# 2. Главное меню
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
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# 3. Инлайн-кнопка для добавления аккаунта в разделе Профили
def get_profiles_inline():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="add_tg_account"))
    return builder.as_markup()


# --- ХЭНДЛЕРЫ ---

# Старт бота
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

# Выбор языка
@dp.message(F.text == "🇷🇺 Русский")
async def process_rus_lang(message: types.Message):
    await message.answer("🤖 **Главное меню ApexSend**\n\nВыберите нужное действие на панели ниже:", reply_markup=get_main_menu("rus"), parse_mode="Markdown")

@dp.message(F.text == "🇬🇧 English")
async def process_eng_lang(message: types.Message):
    await message.answer("🤖 **ApexSend Main Menu**\n\nChoose an action on the panel below:", reply_markup=get_main_menu("eng"), parse_mode="Markdown")

# Нажатие на кнопку "👤 Профили" или "👤 Profiles"
@dp.message(F.text.in_(["👤 Профили", "👤 Profiles"]))
async def process_profiles_menu(message: types.Message):
    await message.answer(
        "🗂 **Управление рабочими аккаунтами**\n\n"
        "Здесь отображаются добавленные профили, с которых будет идти рассылка.\n"
        "Чтобы привязать новый аккаунт, нажмите на кнопку ниже:",
        reply_markup=get_profiles_inline(),
        parse_mode="Markdown"
    )

# Клик по инлайн-кнопке "Добавить аккаунт" -> Переход в FSM состояние
@dp.callback_query(F.data == "add_tg_account")
async def start_add_account(callback: types.CallbackQuery, state: FSMContext):
    await callback.message
