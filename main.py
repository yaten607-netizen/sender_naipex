import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ukr"))
    builder.add(types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_rus"))
    builder.add(types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_eng"))
    builder.add(types.InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_chn"))
    builder.adjust(2)
    return builder.as_markup()

def get_main_menu(lang: str):
    builder = InlineKeyboardBuilder()
    if lang == "ukr":
        builder.add(types.InlineKeyboardButton(text="👥 Керування акаунтами", callback_data="menu_accounts"))
        builder.add(types.InlineKeyboardButton(text="✉️ Створити розсилку", callback_data="menu_start_spam"))
        builder.add(types.InlineKeyboardButton(text="⚙️ Налаштування", callback_data="menu_settings"))
        builder.add(types.InlineKeyboardButton(text="🌐 Змінити мову", callback_data="menu_change_lang"))
    elif lang == "rus":
        builder.add(types.InlineKeyboardButton(text="👥 Управление аккаунтами", callback_data="menu_accounts"))
        builder.add(types.InlineKeyboardButton(text="✉️ Создать рассылку", callback_data="menu_start_spam"))
        builder.add(types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="menu_settings"))
        builder.add(types.InlineKeyboardButton(text="🌐 Изменить язык", callback_data="menu_change_lang"))
    else:
        builder.add(types.InlineKeyboardButton(text="👥 Manage Accounts", callback_data="menu_accounts"))
        builder.add(types.InlineKeyboardButton(text="✉️ New Campaign", callback_data="menu_start_spam"))
        builder.add(types.InlineKeyboardButton(text="⚙️ Settings", callback_data="menu_settings"))
        builder.add(types.InlineKeyboardButton(text="🌐 Change Language", callback_data="menu_change_lang"))
    builder.adjust(1)
    return builder.as_markup()

# --- ХЭНДЛЕРЫ ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Welcome to ApexSend!**\n"
        "The ultimate multi-language platform for automated Telegram outreach and traffic growth.\n\n"
        "Please choose your language below to access the control panel:\n"
        "_____________________________________\n\n"
        "🚀 **Добро пожаловать в ApexSend!**\n"
        "Прогрессивная мультиязычная платформа для автоматизации рассылок и масштабирования трафика.\n\n"
        "Пожалуйста, выберите язык ниже для доступа к панели управления:",
        reply_markup=get_language_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("lang_"))
async def process_language_select(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    text = "🤖 **Головне меню ApexSend**\n\nОберіть потрібну дію:" if lang == "ukr" else "🤖 **Главное меню ApexSend**\n\nВыберите нужное действие:"
    await callback.message.edit_text(text=text, reply_markup=get_main_menu(lang), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_change_lang")
async def process_change_lang(callback: types.CallbackQuery):
    await callback.message.edit_text("🚀 Выберите язык / Оберіть мову / Choose language:", reply_markup=get_language_keyboard())
    await callback.answer()

@dp.callback_query(F.data.startswith("menu_"))
async def process_menu_buttons(callback: types.CallbackQuery):
    await callback.answer("Эта функция сейчас разрабатывается нами! 😉", show_alert=True)

async def main():
    print("[+] Панель управления ApexSend успешно запущена!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())