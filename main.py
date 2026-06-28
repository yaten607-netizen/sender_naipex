import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Твой токен вшит напрямую для удобства запуска на хостинге
BOT_TOKEN = "8973718655:AAEJLZCO4z1SIRnBAiudnZ8EZrj5D-D8SqI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

# 1. Выбор языка при старте
def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ukr"))
    builder.add(types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_rus"))
    builder.add(types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_eng"))
    builder.add(types.InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_chn"))
    builder.adjust(2)
    return builder.as_markup()

# 2. Главное меню (генерируется в зависимости от выбранного языка)
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

# Стартовая команда (исправленная разметка Markdown)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Welcome to ApexSend!**\n"
        "The ultimate multi-language platform for automated Telegram outreach and traffic growth.\n\n"
        "Please choose your language below to access the control panel:\n"
        "-------------------------------------\n"
        "🚀 **Добро пожаловать в ApexSend!**\n"
        "Прогрессивная мультиязычная платформа для автоматизации рассылок и масштабирования трафика.\n\n"
        "Пожалуйста, выберите язык ниже для доступа к панели управления:",
        reply_markup=get_language_keyboard(),
        parse_mode="Markdown"
    )

# Обработка выбора языка и показ Главного Меню
@dp.callback_query(F.data.startswith("lang_"))
async def process_language_select(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    
    if lang == "ukr":
        text = (
            "🤖 **Головне меню ApexSend**\n\n"
            "Платформа готова до роботи. Оберіть потрібну дію на кнопках нижче:"
        )
    elif lang == "rus":
        text = (
            "🤖 **Главное меню ApexSend**\n\n"
            "Платформа готова к работе. Выберите нужное действие на кнопках ниже:"
        )
    else:
        text = (
            "🤖 **ApexSend Main Menu**\n\n"
            "The platform is ready. Choose an action using the buttons below:"
        )
        
    await callback.message.edit_text(
        text=text,
        reply_markup=get_main_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()

# Возврат к выбору языка из меню
@dp.callback_query(F.data == "menu_change_lang")
async def process_change_lang(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🚀 Выберите язык / Оберіть мову / Choose language:",
        reply_markup=get_language_keyboard()
    )
    await callback.answer()

# Заглушки для остальных кнопок меню
@dp.callback_query(F.data.startswith("menu_"))
async def process_menu_buttons(callback: types.CallbackQuery):
    await callback.answer("Эта функция сейчас разрабатывается нами! 😉", show_alert=True)


# --- ЗАПУСК ---
async def main():
    print("[+] Панель управления ApexSend успешно запущена!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
