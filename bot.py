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

# Загрузка данных из CSV
try:
    data = pd.read_csv('data.csv', encoding='latin1', delimiter=';')
    logger.info("Данные успешно загружены из data.csv")
except Exception as e:
    logger.error(f"Ошибка при загрузке data.csv: {e}")
    data = pd.DataFrame()


def load_product_data():
    try:
        product_data = pd.read_csv('products.csv', encoding='latin1', delimiter=';')
        logger.info("Данные о товарах загружены из products.csv")
        return product_data
    except Exception as e:
        logger.error(f"Ошибка при загрузке products.csv: {e}")
        return pd.DataFrame()


# Функция команды /start
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


# Функция команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "Вы также можете использовать кнопки для навигации."
    )
    await update.message.reply_text(help_text)


# Функция обработки кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

     if text == "Сурогаи склад роҳ  🚚":
        response = "1) AL-KH \n2)13711652794\n3) 广州市荔湾区环市西路黑山三街20号宇宙鞋城E区113-119档8 Al-Kh /Шахр/Ном ва номери телефон"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/photo_2024-10-08_19-49-26.jpg")

    if text == "Сурогаи склад авиа✈️":
        response = "Avia / Ном ВА номери шумо \n19068507113\n浙江省 金华市 义乌市\n桥东二区34栋8号 1 avia Al-Kh / Шахр Ном ВА немери шумо"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/photo_5406973989118667037_y.jpg")


    elif text == "Нархнома 💲":
        response = "РОҲ\n> Аз 1кг то 40кг  - 3$ \n> Аз 40кг зиёд  - 2,8$\n> Аз 100кг зиёд алохида нарх дода мешавад\n> Аз 1куб 300$\n\nАВИА\n\nСрок доставки: 7-13 дней 🚀\n• 10$\кг\n• До 31.12.2024 — всего 9$\кг 🎉"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/Нарх2.png")

    elif text == "Молҳои манъшуда ❌":
        response = "ЗАПРЕЩЕННЫЕ ТОВАРЫ\nНЕЛЬЗЯ 🚫 ЗАКАЗАТЬ ИЗ КИТАЯ , ДАННЫЙ МОМЕНТ ПРОВЕРКА ИДЕТ ТЩАТЕЛЬНО ‼️\nЗапрещенные товары \n🚫 Лекарственное средство (порошок, таблетки, жидкие лекарства)\n🚫 Все виды жидких веществ (парфюм, ароматизаторы и тд)\n🚫 Все виды холодного оружия (ножи, электрошокеры , биты и т.д)\n 🚫 Не принимаем электронные сигареты, кальяны и т.д\n🚫 ТОВАРЫ С ПРИЗНАКАМИ 18+ \n🚫 Смартфон ( телефоны ) и ноутбук\n\nЗапрещенные вещи для перевозки в АВИАции, пожалуйста, соблюдайте правила.\nЗапрещенные вещи 🚫\nХолодное оружие 🗡️\nХимические вещества 🧪\nБаллон с дихлофосом (газ) 🧴\nВещи 18+ 🔞\nЛюбые опасные предметы ⚠️\nС аккумуляторами 🔋\nВсе эти вещи запрещены ❌"
        await update.message.reply_text(response)

    elif text == "Контакт 👤":
        response = "Контакт : www.instagram.com/somon_sugd_cargo \n Телефон +992990050500 Whatsapp, Telegram "
        await update.message.reply_text(response)

    elif text == "Тафтиши трек-код 🔍":
        response = "Трек-коди худро ворид намоед:"
        await update.message.reply_text(response)

    elif text == "Дарси ройгон!":
        response = " Дарсхои ройгонро аз инчо дастрас кунед: https://t.me/somon_sugd_cargo/31"
        await update.message.reply_text(response)
    elif text == "Борҳои қабулшуда 🔍":
        await update.message.reply_text("Рақами телефони худро ворид кунед:")
        return
    else:
        response = None  # Если нет совпадения, ничего не отправляем

    if response:
        await update.message.reply_text(response)


# Функция проверки трек-кода
async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text.strip()
    logger.info(f"Получен трек-код: {track_code}")

    if data.empty:
        await update.message.reply_text("⚠️ База данных пустая или не загружена.")
        return

    result = data[data['code'].astype(str) == track_code]

    if not result.empty:
        status_china = result.iloc[0]['china']
        status_khujand = result.iloc[0]['khujand']
        arrival_date = result.iloc[0]['arrival_date']

        if status_khujand:
            response = f"📦 Бори шумо бо трек-коди {track_code} ба Хучанд омадааст."
        elif status_china:
            response = f"📦 Бори Шумо бо трек-коди {track_code} ба склади Хитой санаи {arrival_date} кабул шудааст ва рузхои наздик ба Хучанд омада мерасад."
    else:
        response = f"📦 Бори шумо ҳоло бо трек-коди {track_code} ба склади Хитой кабул нашудааст."

    await update.message.reply_text(response)


# Обработка кнопки "Борҳои қабулшуда 🔍"
async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Рақами телефони худро ворид кунед:")
    context.user_data['waiting_for_phone'] = True  # Ожидаем ввод номера телефона


# Проверка товаров по номеру телефона
async def check_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('waiting_for_phone'):  # Если не ждем телефон, проверяем как трек-код
        await check_track_code(update, context)
        return

    phone_number = update.message.text.strip()
    logger.info(f"Проверка товаров по номеру: {phone_number}")

    product_data = load_product_data()
    phone_result = product_data[product_data['phone'].astype(str) == phone_number]

    if not phone_result.empty:
        response = f"📲 Информация о товарах для номера {phone_number}:\n"
        for _, row in phone_result.iterrows():
            response += (
                f"👤 Имя: {row['name']}\n"
                f"📦 Шт: {row['quantity']}\n"
                f"⚖️ Кг: {row['weight']}\n"
                f"📏 Куб: {row['volume']}\n"
                f"💰 Сумма (TJS): {row['amount']}\n"
                f"📅 Дата прибытия: {row['arrival_date']}\n"
                "----------------------\n"
            )
    else:
        response = "❌ Бори Шумо бо ин раками телефон кабул нашудааст."

    await update.message.reply_text(response)
    context.user_data['waiting_for_phone'] = False  # Сбрасываем ожидание номера телефона


# Общий обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    # Если ожидается ввод номера телефона
    if context.user_data.get('waiting_for_phone'):
        await check_phone(update, context)
        return

    # Если текст похож на трек-код (например, состоит из цифр и имеет определенную длину)
    if text.isdigit() and len(text) == 10:  # Пример: трек-код длиной 10 цифр
        await check_track_code(update, context)
        return

    # Если текст не является трек-кодом, обрабатываем как кнопку
    await handle_buttons(update, context)


# Главная функция
def main():
    TOKEN = '8174740222:AAFXj35riRMhfGf8ATDXMcOAJ9KlJ9ZoBlY'

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик для кнопки "Борҳои қабулшуда 🔍"
    application.add_handler(MessageHandler(filters.Regex("Борҳои қабулшуда 🔍"), request_phone))

    # Общий обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()


if __name__ == '__main__':
    main()
