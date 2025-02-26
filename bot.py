import logging
import pandas as pd
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция для загрузки CSV-файлов
def load_csv(filename):
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename, encoding="latin1", delimiter=";")
            df.columns = df.columns.str.lower().str.strip()  # Приведение колонок к нижнему регистру
            logger.info(f"Файл {filename} успешно загружен.")
            return df
        else:
            logger.warning(f"Файл {filename} не найден.")
            return pd.DataFrame()  # Возвращает пустой DataFrame при отсутствии файла
    except Exception as e:
        logger.error(f"Ошибка при загрузке {filename}: {e}")
        return pd.DataFrame()

# Загрузка данных из CSV
data = load_csv("data.csv")
product_data = load_csv("products.csv")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Сурогаи склад роҳ 🚚", "Нархнома 💲"],
        ["Молҳои манъшуда ❌", "Контакт 👤"],
        ["Тафтиши трек-код 🔍", "Дарси ройгон!"],
        ["Борҳои қабулшуда 🔍"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Хуш омадед ба Telegram боти Сомон Сугд Карго! 📦", reply_markup=reply_markup
    )

# Функция для обработки кнопок и поиска товаров
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    responses = {
        "Сурогаи склад роҳ 🚚": "📍 Сурогаи склад:\n1) AL-KH\n2)13711652794\n3) 广州市荔湾区环市西路黑山三街20号宇宙鞋城E区113-119档8 Al-Kh /Шахр/Ном ва номери телефон",
        "Нархнома 💲": "💲 Нархнома:\n• Аз 1кг то 40кг - 3$\n• Аз 40кг зиёд - 2.8$\n• Аз 1куб - 300$\n\n✈️ АВИА (7-13 дней) - 9$/кг",
        "Молҳои манъшуда ❌": "🚫 Запрещенные товары:\n• Лекарства\n• Жидкости (парфюм, ароматизаторы)\n• Оружие, электронные сигареты\n• Телефоны, ноутбуки\n• 18+ товары",
        "Контакт 👤": "📞 Контакт:\nInstagram: @somon_sugd_cargo\nWhatsApp/Telegram: +992990050500",
        "Тафтиши трек-код 🔍": "📦 Введите ваш трек-код:",
        "Дарси ройгон!": "📚 Бесплатные уроки: https://t.me/somon_sugd_cargo/31",
        "Борҳои қабулшуда 🔍": "📲 Введите ваш номер телефона:"
    }

    if text in responses:
        await update.message.reply_text(responses[text])
        return

    # Поиск товаров по номеру телефона
    if product_data.empty:
        await update.message.reply_text("❌ База данных товаров недоступна.")
        return

    phone_result = product_data[product_data['phone'].astype(str) == text]

    if not phone_result.empty:
        response = f"📲 Товары для номера {text}:\n"
        for _, row in phone_result.iterrows():
            response += (
                f"\n📦 Код товара: {row['code']}\n"
                f"👤 Имя: {row['name']}\n"
                f"📦 Шт: {row['quantity']}\n"
                f"⚖️ Кг: {row['weight']}\n"
                f"📏 Куб: {row['volume']}\n"
                f"💰 Сумма (TJS): {row['amount']}\n"
                f"📅 Дата прибытия: {row['arrival_date']}\n"
                "----------------------"
            )
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Маълумот ёфт нашуд! Лутфан рақами дурустро ворид кунед.")

# Функция для проверки трек-кода
async def track_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if data.empty:
        await update.message.reply_text("❌ База данных трек-кодов недоступна.")
        return

    track_code = update.message.text.strip()
    if len(track_code) < 10:
        await update.message.reply_text("❌ Лутфан трек-код ворид кунед, на телефон рақам!")
        return

    result = data[data['code'].astype(str) == track_code]

    if not result.empty:
        await update.message.reply_text(f"📦 Маълумот ёфт шуд! Статус: {result.iloc[0]['status']}")
    else:
        await update.message.reply_text("❌ Маълумот ёфт нашуд! Лутфан рақами дурустро ворид кунед.")

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("ℹ️ Команды:\n/start - Запуск бота\n/help - Помощь")



# Главная функция
def main():
    # Вставьте сюда токен, который вы получили от @BotFather
    TOKEN = '8174740222:AAFXj35riRMhfGf8ATDXMcOAJ9KlJ9ZoBlY'

    # Создаем объект Application и передаем ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик сообщений с кнопок и трек-кодов
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main() 
