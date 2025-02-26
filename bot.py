import logging
import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка данных из CSV с указанием кодировки и разделителя
try:
    data = pd.read_csv('data.csv', encoding='latin1', delimiter=';')
    logger.info("Данные успешно загружены из data.csv")
except Exception as e:
    logger.error(f"Ошибка при загрузке данных из data.csv: {e}")
    data = pd.DataFrame()

# Функция для загрузки данных о товарах из products.csv
def load_product_data():
    try:
        product_data = pd.read_csv('products.csv', encoding='latin1', delimiter=';')
        logger.info("Данные о товарах успешно загружены из products.csv")
        return product_data
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных о товарах из products.csv: {e}")
        return pd.DataFrame()

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Сурогаи склад роҳ  🚚", "Нархнома 💲"],
        ["Молҳои манъшуда ❌", "Контакт 👤"],
        ["Тафтиши трек-код 🔍", "Дарси ройгон!"],
        ["Борҳои қабулшуда 🔍"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        'Хуш омадед ба Telegram боти Сомон Сугд Карго. Ман ба шумо дар ёфтани суроғаҳои анбор, '
        'санҷидани трек код ва бо нархҳо шинос шудан кӯмак мекунам', 
        reply_markup=reply_markup
    )

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с описанием команд."""
    help_text = (
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "Вы также можете использовать кнопки для навигации."
    )
    await update.message.reply_text(help_text)

# Функция для обработки сообщений с кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Сурогаи склад роҳ  🚚":
        response = "1) AL-KH \n2)13711652794\n3) 广州市荔湾区环市西路黑山三街20号宇宙鞋城E区113-119档8 Al-Kh /Шахр/Ном ва номери телефон"
        await update.message.reply_text(response)

    elif text == "Нархнома 💲":
        response = "РОҲ\n> Аз 1кг то 40кг  - 3$ \n> Аз 40кг зиёд  - 2,8$\n> Аз 100кг зиёд алохида нарх дода мешавад\n> Аз 1куб 300$"
        await update.message.reply_text(response)

    elif text == "Молҳои манъшуда ❌":
        response = "🚫 Лекарства, жидкости, ножи, электронные сигареты, телефоны, ноутбуки и т.д. запрещены для перевозки."
        await update.message.reply_text(response)

    elif text == "Контакт 👤":
        response = "📲 Instagram: www.instagram.com/somon_sugd_cargo \n📞 Телефон: +992990050500 (Whatsapp, Telegram)"
        await update.message.reply_text(response)

    elif text == "Тафтиши трек-код 🔍":
        await update.message.reply_text("Трек-коди худро ворид намоед:")

    elif text == "Дарси ройгон!":
        await update.message.reply_text("Дарсхои ройгонро аз инчо дастрас кунед: https://t.me/somon_sugd_cargo/31")

    elif text == "Борҳои қабулшуда 🔍":
        await update.message.reply_text("Рақами телефони худро ворид кунед:")

    else:
        product_data = load_product_data()
        phone_result = product_data[product_data['phone'].astype(str) == text]

        if not phone_result.empty:
            response = f"📲 Информация о товарах для номера {text}:\n"
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
async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text.strip()
    logger.info(f"Получен трек-код: {track_code}")

    # Проверяем, загружены ли данные
    if data.empty:
        await update.message.reply_text("⚠️ Ошибка: База данных пустая или не загружена.")
        return

    # Ищем трек-код в data.csv
    result = data[data['code'].astype(str) == track_code]

    if not result.empty:
        status_china = result.iloc[0]['china']
        status_khujand = result.iloc[0]['khujand']
        arrival_date = result.iloc[0]['arrival_date']

        if status_khujand:
            response = f"📦 Бори шумо бо трек-коди {track_code} ба Хучанд омадааст."
        elif status_china:
            response = f"📦 Бори шумо ба склади Хитой санаи {arrival_date} кабул шудааст."
        else:
            response = f"📦 Бори шумо ҳоло ба склади Хитой кабул нашудааст."
    else:
        response = f"📦 Бори шумо бо трек-коди {track_code} ёфт нашуд."

    await update.message.reply_text(response)


# Главная функция
def main():
    # Вставьте сюда токен, который вы получили от @BotFather
    TOKEN = '8174740222:AAFXj35riRMhfGf8ATDXMcOAJ9KlJ9ZoBlY'

    # Создаем объект Application и передаем ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик для кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Обработчик для ввода трек-кода
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_track_code))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main() 
