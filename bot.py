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

# Функция для загрузки данных о товарах из products.csv
def load_product_data():
    try:
        product_data = pd.read_csv('products.csv', encoding='latin1', delimiter=';')
        logger.info("Данные о товарах успешно загружены из products.csv")
        return product_data
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных о товарах из products.csv: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame при ошибке


# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Сурогаи склад роҳ  🚚", "Нархнома 💲"],
        ["Молҳои манъшуда ❌", "Контакт 👤"],
        ["Тафтиши трек-код 🔍", "Дарси ройгон!"],
        ["Борҳои қабулшуда 🔍"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Хуш омадед ба Telegram боти  Сомон Сугд Карго. Ман ба шумо дар ёфтани суроғаҳои анбор, санҷидани трек код ва бо нархҳо шинос шудан кӯмак мекунам', reply_markup=reply_markup)

# Функция для обработки сообщений с кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Сурогаи склад роҳ  🚚":
        response = "1) AL-KH \n2)13711652794\n3) 广州市荔湾区环市西路黑山三街20号宇宙鞋城E区113-119档8 Al-Kh /Шахр/Ном ва номери телефон"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/photo_2024-10-08_19-49-26.jpg")


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
        # Предлагаем ввести код из products.csv
        await update.message.reply_text("Рамзи худро ворид кунед:")
    else:
        # Здесь обрабатываем введённый текст, который может быть:
        # - трек-кодом (data.csv)
        # - кодом товара (products.csv)

        # Попробуем сначала поискать в products.csv
        product_data = load_product_data()
        product_result = product_data[product_data['phone'] == text]

        if not product_result.empty:
            # Если нашли запись в products.csv, формируем ответ
            product_info = product_result.iloc[0]
            response = (
                f"Информация о товаре с кодом {text}:\n"
                f"Имя: {product_info['name']}\n"
                f"Телефон: {product_info['phone']}\n"
                f"Шт: {product_info['quantity']}\n"
                f"Кг: {product_info['weight']}\n"
                f"Куб: {product_info['volume']}\n"
                f"Сумма (TJS): {product_info['amount']}\n"
                f"Дата прибытия: {product_info['arrival_date']}"
            )
            await update.message.reply_text(response)
        else:
            # Если не нашли в products.csv, проверяем data.csv (трекинг)
            await check_track_code(update, context)



# Функция для проверки трек-кода
# Функция для проверки трек-кода
async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text
    logger.info(f"Получен трек-код: {track_code}")

    # Выполняем поиск трек-кода
    result = data[data['code'] == track_code]
    logger.info(f"Результат поиска: {result}")

    if not result.empty:
        status_china = result['china'].values[0]
        status_khujand = result['khujand'].values[0]
        arrival_date = result['arrival_date'].values[0]  # Извлекаем дату прибытия на склад

        if status_khujand:
            response = f"Бори Шумо бо трек-коди {track_code} ба Хучанд омадааст, мунтазири занг шавед."
        elif status_china:
            response = (f"Бори Шумо бо трек-коди {track_code} ба склади Хитой санаи {arrival_date} кабул шудааст ва рузхои наздик ба Хучанд омада мерасад.")
        else:
            response = f"Бори Шумо бо трек-коди {track_code} холо ба склади Хитой кабул нашуааст."
    else:
        response = f"Бори Шумо бо трек-коди {track_code} холо ба склади Хитой кабул нашуааст."

    logger.info(f"Ответ: {response}")
    await update.message.reply_text(response)



# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Напишите /start для начала общения со мной.')


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
