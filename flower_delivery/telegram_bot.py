import os
import sys
import django
import logging
from datetime import datetime

# Добавляем путь к корневой папке проекта, чтобы Python мог найти настройки Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackContext, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)
from core.models import Product, Order, OrderItem, UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot_logs.log")
    ]
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
# (ASKING_FULL_NAME, ASKING_PHONE, ASKING_ADDRESS0) = range(3)
# (SELECT_PRODUCT, SELECT_QUANTITY, ASKING_CUSTOM_QUANTITY, ASKING_ADDRESS, ORDER_CONFIRMATION) = range(5)
(ASKING_FULL_NAME, ASKING_PHONE, ASKING_ADDRESS0, INFO_CONFIRMATION, SELECT_PRODUCT, SELECT_QUANTITY, ASKING_CUSTOM_QUANTITY, ASKING_ADDRESS, ORDER_CONFIRMATION) = range(9)

# Рабочее время
WORKING_HOURS_START = 9
WORKING_HOURS_END = 23

# Загружаем токен из переменных окружения через настройки Django
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_TELEGRAM_CHAT_ID = os.getenv("ADMIN_TELEGRAM_CHAT_ID")
application = Application.builder().token(TELEGRAM_BOT_TOKEN).read_timeout(5).write_timeout(5).build()

# Функция проверки рабочего времени
def is_within_working_hours() -> bool:
    now = datetime.now().time()
    return WORKING_HOURS_START <= now.hour < WORKING_HOURS_END

# Унифицированная функция отправки сообщений с клавиатурой
async def send_message_with_keyboard(chat_id, text, keyboard, context):
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

# Функция запуска бота
async def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"Команда /start выполнена пользователем: {update.message.from_user.username}")
    keyboard = [
        [
            InlineKeyboardButton("ℹ️ Помощь", callback_data='help'),
            InlineKeyboardButton("📝 Регистрация", callback_data='register')
        ],
        [
            InlineKeyboardButton("🌹 Каталог", callback_data='catalog'),
            InlineKeyboardButton("📦 Статус заказа", callback_data='status')
        ],
        [InlineKeyboardButton("🛍 Заказать", callback_data='order')]
    ]
    if update.message.chat_id == int(ADMIN_TELEGRAM_CHAT_ID):
        keyboard.append([InlineKeyboardButton("🛠 Управление заказами", callback_data='manage_orders')])
    await send_message_with_keyboard(
        update.message.chat_id,
        "   Добро пожаловать\nв `Flower Delivery Bot`!\nВыберите один из вариантов ниже:",
        keyboard,
        context,
    )

# async def handle_catalog(update: Update, context: CallbackContext) -> None:
#     """Redirect user to the catalog page."""
#     query = update.callback_query
#     await query.answer()
#     await query.message.reply_text("Перейдите по ссылке для просмотра каталога: http://127.0.0.1:8000")

async def handle_catalog(update: Update, context: CallbackContext) -> None:
    """Redirect user to the catalog page."""
    query = update.callback_query
    await query.answer()
    try:
        await query.message.reply_text("Перейдите по ссылке для просмотра каталога: http://127.0.0.1:8000")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения о каталоге: {e}")
        await query.message.reply_text("Произошла ошибка при попытке перейти к каталогу. Пожалуйста, попробуйте позже.")


async def handle_status(update: Update, context: CallbackContext) -> None:
    """Redirect user to the order status page."""
    query = update.callback_query
    await query.answer()
    try:
        await query.message.reply_text("Перейдите по ссылке для проверки "
                                       "статуса заказа: http://127.0.0.1:8000/profile")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения о cтатусе заказа: {e}")
        await query.message.reply_text("Произошла ошибка при попытке проверки статуса заказа. "
                                       "Пожалуйста, попробуйте позже.")


async def handle_help(update: Update, context: CallbackContext) -> None:
    """Provide help instructions for the user."""
    query = update.callback_query
    await query.answer()
    help_message = (
        "*Инструкция по заказу цветов:*\n"
        "0. Нажмите '*📝 Регистрация*' до процедуры заказа `цветов🌹`.\n"
        "1. Нажмите '*🛍 Заказать*' для просмотра доступных `цветов🌹`.\n"
        "2. *Выберите* `товар(букет,цветок🌹)` и количество.\n"
        "3. Укажите *адрес доставки*.\n"
        "4. *Подтвердите* Ваш заказ.\n"
        "5. *Проверьте статус* заказа с помощью '*📦 Статус заказа*'.\n\n"
        "*Если у Вас возникли вопросы, обратитесь в службу поддержки*."
    )
    await query.message.reply_text(help_message, parse_mode='Markdown')

async def handle_register(update: Update, context: CallbackContext) -> int:
    user_chat_id = update.effective_chat.id
    username = update.effective_user.username

    if not username:
        await update.effective_message.reply_text("Ошибка: имя пользователя не найдено. \nПожалуйста, введите его в своём профиле Телеграм.")
        return ConversationHandler.END

    user, created = await sync_to_async(User.objects.get_or_create)(
        username=username,
        defaults={
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name,
            'email': f"{username}@example.com"
        }
    )

    # Сохраняем объект user в контексте
    context.user_data['user'] = user

    # Проверяем, существует ли профиль пользователя
    user_profile, created_profile = await sync_to_async(UserProfile.objects.get_or_create)(
        user=user,
        defaults={
            'telegram_chat_id': user_chat_id,
            'full_name': None,
            'phone': None,
            'delivery_address': None,
        }
    )

    # Проверяем, заполнен ли профиль пользователя
    if created_profile:
        await update.effective_message.reply_text(f"{update.effective_user.first_name}, Вы успешно *зарегистрированы*!\n Пожалуйста, введите *Ваше полное имя (ФИО)*:", parse_mode="Markdown")
        return ASKING_FULL_NAME  # Переход к следующему состоянию для ввода полного имени
    else:
        # Проверяем, заполнены ли поля профиля
        if user_profile.full_name is None:
            await update.effective_message.reply_text(f"{update.effective_user.first_name}, Вы *уже зарегистрированы* в системе!\n Пожалуйста, введите *Ваше полное имя (ФИО)*:", parse_mode="Markdown")
            return ASKING_FULL_NAME  # Переход к следующему состоянию для ввода полного имени
        else:
            await update.effective_message.reply_text(f"{update.effective_user.first_name}, Вы *уже зарегистрированы* в системе, и Ваш профиль заполнен!\n"
                                                      "Если Вам *нужно обновить* информацию о себе, пожалуйста, обратитесь"
                                                  " к администратору или откорректируйте ее в своем личном кабинете "
                                                  "на нашем сайте.", parse_mode="Markdown")
        return ConversationHandler.END  # Завершить разговор, если профиль заполнен


async def ask_full_name(update: Update, context: CallbackContext) -> int:
    full_name = update.message.text
    context.user_data['full_name'] = full_name  # Сохраняем полное имя в контексте

    await update.message.reply_text(f"{update.effective_user.first_name}, пожалуйста, введите Ваш *номер телефона*:", parse_mode="Markdown")
    return ASKING_PHONE  # Переход к следующему состоянию для ввода номера телефона

async def ask_phone(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    context.user_data['phone'] = phone  # Сохраняем номер телефона в контексте

    await update.message.reply_text(f"{update.effective_user.first_name}, пожалуйста, введите *Ваш адрес доставки*:", parse_mode="Markdown")
    return ASKING_ADDRESS0  # Переход к следующему состоянию для ввода адреса доставки


async def ask_address(update: Update, context: CallbackContext) -> int:
    try:
        delivery_address = update.message.text
        context.user_data['delivery_address'] = delivery_address  # Сохраняем адрес в контексте
        phone = context.user_data.get('phone')
        full_name = context.user_data.get('full_name')
        user_chat_id = update.effective_chat.id

        # Логируем полученные данные
        logger.info(f"Получен адрес доставки: {delivery_address}")
        logger.info(f"ФИО: {full_name}, Телефон: {phone}, Chat ID: {user_chat_id}")

        # Проверка на наличие необходимых данных
        if not all([full_name, phone, delivery_address]):
            await update.message.reply_text(f"{update.effective_user.first_name}, пожалуйста, убедитесь, "
                                            f"что все данные собраны.", parse_mode="Markdown")
            return ConversationHandler.END

        # Экранирование специальных символов
        info_summary = (
            f"Ваши данные для регистрации на сайте:\n"
            f"ФИО: {full_name};\n"
            f"Телефон: {phone};\n"
            f"Ваш chat_id в Телеграме: {user_chat_id};\n"
            f"Адрес доставки: {delivery_address}\n\n"
            f"Подтвердите Ваши данные, если верны:"
        )
        keyboard1 = [
            [InlineKeyboardButton("✅ Подтвердить", callback_data='confirm_info')],
            [InlineKeyboardButton("❌ Отменить", callback_data='cancel_info')]
        ]

        await update.message.reply_text(info_summary, reply_markup=InlineKeyboardMarkup(keyboard1))
        return INFO_CONFIRMATION
    except Exception as e:
        logger.error(f"Ошибка при обработке адреса: {e}")
        await update.message.reply_text(f"{update.effective_user.first_name}, произошла ошибка. \n"
                                        f"Пожалуйста, попробуйте снова.", parse_mode="Markdown")
        return ConversationHandler.END

async def confirm_info(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    telegram_chat_id = str(update.effective_user.id)
    full_name = context.user_data.get('full_name')
    phone = context.user_data.get('phone')
    delivery_address = context.user_data.get('delivery_address')

    if not all([full_name, phone, delivery_address]):
        await query.message.reply_text("Пожалуйста, убедитесь, что все данные собраны.")
        return ConversationHandler.END
    try:
        user = context.user_data.get('user')
        if user is None:
            await query.message.reply_text("Ошибка: пользователь не найден. Пожалуйста, зарегистрируйтесь заново.")
            return ConversationHandler.END
        # Отладочное сообщение
        await query.message.reply_text(f"Данные для сохранения: {full_name}, {phone}, {delivery_address}")
        user_profile, created = await sync_to_async(UserProfile.objects.update_or_create)(
            user=user,
            defaults={
                'telegram_chat_id': telegram_chat_id,
                'full_name': full_name,
                'phone': phone,
                'delivery_address': delivery_address
            }
        )
        if created:
            await query.message.reply_text("Профиль успешно создан.")
        else:
            await query.message.reply_text("Профиль успешно обновлен.")
        return ConversationHandler.END
    except IntegrityError as e:
        await sync_to_async(logger.error)(f"Ошибка при сохранении профиля пользователя: {e}")
        await query.message.reply_text("Произошла ошибка при сохранении ваших данных. Пожалуйста, попробуйте снова.")
    except Exception as e:
        await sync_to_async(logger.error)(f"Ошибка: {e}")
        await query.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")
    return ConversationHandler.END


async def cancel_info(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("Пользователь отменил регистрацию своих данных из-за ошибки.")
    await query.edit_message_text(text=f"{update.effective_user.first_name}, регистрация в системе Ваших данных отменена *.", parse_mode="Markdown")
    return ConversationHandler.END


# async def handle_register(update: Update, context: CallbackContext) -> None:
#     """Redirect user to the registration page."""
#     query = update.callback_query
#     await query.answer()
#     await query.message.reply_text("Перейдите по ссылке для регистрации: http://127.0.0.1:8000/register")


async def handle_manage_orders(update: Update, context: CallbackContext) -> None:
    """Manage orders to the Admin panel."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"{update.effective_user.first_name}, перейдите по ссылке для управления заказами: *http://127.0.0.1:8000/admin*", parse_mode="Markdown")


async def start_order(update: Update, context: CallbackContext) -> int:
    """Начало процесса заказа с проверкой рабочего времени."""
    logger.info("Начало процесса заказа.")
    query = update.callback_query
    await query.answer()

    if not is_within_working_hours():
        await query.message.reply_text(
            "Заказы принимаются только *в рабочее время (с 9:00 до 18:00)*.\n"
            "Заказы, присланные *в нерабочее время*, будут обработаны *на следующий рабочий день*.", parse_mode="Markdown"
        )

    products = await sync_to_async(list)(Product.objects.all())
    if products:
        keyboard = [
            [InlineKeyboardButton(f" {product.name}   `{product.price} рублей`", callback_data=f"product_{product.id}")]
        # keyboard = [
        #     [InlineKeyboardButton(f"{product.name} ({product.price}) руб.", callback_data=f"product_{product.id}")]
            for product in products
        ]
        await query.message.reply_text(f"{update.effective_user.first_name}, *выберите товар для заказа:*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return SELECT_PRODUCT
    else:
        await query.message.reply_text(f"{update.effective_user.first_name}, к сожалению, в данный момент *товары не доступны*.", parse_mode="Markdown")
        return ConversationHandler.END

# Обработчик для выбора продукта
async def handle_product_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    try:
        await query.answer()
        product_id = int(query.data.split("_")[1])
        product = await sync_to_async(Product.objects.get)(id=product_id)
        context.user_data['product'] = product

        keyboard = [
            [InlineKeyboardButton("1", callback_data="quantity_1"),
             InlineKeyboardButton("2", callback_data="quantity_2"),
             InlineKeyboardButton("3", callback_data="quantity_3")],
            [InlineKeyboardButton("4", callback_data="quantity_4"),
             InlineKeyboardButton("5", callback_data="quantity_5")],
            [InlineKeyboardButton("Ввести количество товара вручную", callback_data="custom_quantity")]
        ]
        await query.edit_message_text(
            text=f"{update.effective_user.first_name}, Вы выбрали товар: *{product.name}*. Выберите *количество товара*:",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
        return SELECT_QUANTITY
    except Exception as e:
        logger.error(f"Ошибка при выборе продукта: {e}")
        await query.message.reply_text("*Произошла ошибка*. Пожалуйста, попробуйте *еще раз*.", parse_mode="Markdown")
        return ConversationHandler.END

# Обработчик для выбора количества
async def handle_quantity_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    quantity = int(query.data.split("_")[1])
    context.user_data['quantity'] = quantity

    product = context.user_data.get('product')
    logger.info(f"Пользователь выбрал количество товара: {quantity}")

    await query.message.reply_text(
        f"{update.effective_user.first_name}, Вы выбрали товар: \n*{product.name}*\nКоличество товара: *{quantity}*\n"
        "Пожалуйста, укажите *адрес для доставки*:", parse_mode="Markdown"
    )
    return ASKING_ADDRESS

# Обработчик для ручного ввода количества
async def handle_custom_quantity(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Пожалуйста, введите *желаемое количество товара*:", parse_mode="Markdown")
    return ASKING_CUSTOM_QUANTITY

async def ask_custom_quantity(update: Update, context: CallbackContext) -> int:
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным числом.")
        context.user_data['quantity'] = quantity

        product = context.user_data.get('product')
        await update.message.reply_text(
            f"{update.effective_user.first_name}, Вы выбрали: *{product.name}*\nКоличество: *{quantity}*\n"
            "Пожалуйста, укажите *адрес для доставки*:", parse_mode="Markdown"
        )
        return ASKING_ADDRESS
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите *корректное положительное число* для количества.", parse_mode="Markdown")
        return ASKING_CUSTOM_QUANTITY

async def process_address_input(update: Update, context: CallbackContext) -> int:
    address = update.message.text
    context.user_data['address'] = address
    product = context.user_data.get('product')
    quantity = context.user_data.get('quantity')

    order_summary = (
        f"{update.effective_user.first_name}, Вы собираетесь заказать товар\n*{product.name}* \n(в количестве *{quantity}* шт.).\n"
        f"Адрес доставки: *{address}*\n\n*Подтвердите Ваш заказ:*"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data='confirm_order')],
        [InlineKeyboardButton("❌ Отменить", callback_data='cancel_order')]
    ]
    await update.message.reply_text(order_summary, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return ORDER_CONFIRMATION

async def confirm_order(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    product = context.user_data.get('product')
    quantity = context.user_data.get('quantity')
    address = context.user_data.get('address')

    user, _ = await sync_to_async(User.objects.get_or_create)(username=query.from_user.username)
    order = await sync_to_async(Order.objects.create)(user=user, address=address)
    await sync_to_async(OrderItem.objects.create)(order=order, product=product, quantity=quantity)

    await query.edit_message_text(text=f"{update.effective_user.first_name}, Ваш заказ на товар *'{product.name}'* \nв количестве *{quantity}* шт. успешно *создан*!", parse_mode="Markdown")
    return ConversationHandler.END

async def cancel_order(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("Пользователь отменил заказ.")
    await query.edit_message_text(text="{update.effective_user.first_name}, Ваш заказ был *отменен*.", parse_mode="Markdown")
    return ConversationHandler.END

def setup_bot(button_handler=None):
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_order, pattern='^order$')],
        states={
            SELECT_PRODUCT: [CallbackQueryHandler(handle_product_selection, pattern='^product_')],
            SELECT_QUANTITY: [
                CallbackQueryHandler(handle_quantity_selection, pattern='^quantity_'),
                CallbackQueryHandler(handle_custom_quantity, pattern='^custom_quantity$')
            ],
            ASKING_CUSTOM_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_custom_quantity)],
            ASKING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_address_input)],
            ORDER_CONFIRMATION: [
                CallbackQueryHandler(confirm_order, pattern='^confirm_order$'),
                CallbackQueryHandler(cancel_order, pattern='^cancel_order$')
            ]
        },
        fallbacks=[CallbackQueryHandler(cancel_order, pattern='^cancel_order$')],
        per_chat=True
    )

    # Определяем ConversationHandler с состояниями и обработчиками
    conversation_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handle_register, pattern='register'),
        ],
        states={
            ASKING_FULL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_full_name)
            ],
            ASKING_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)
            ],
            ASKING_ADDRESS0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)
            ],
            INFO_CONFIRMATION: [
                CallbackQueryHandler(confirm_info, pattern='^confirm_info$'),
                CallbackQueryHandler(cancel_info, pattern='^cancel_info$')
            ]
        },
        fallbacks=[
            CallbackQueryHandler(cancel_info, pattern='^cancel_info$')
        ],
        allow_reentry=True  # Позволяет пользователю повторно входить в разговор
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    # Добавляем ConversationHandler в приложение
    application.add_handler(conversation_handler)
    # Add these handlers to the application in the main function or where you initialize your handlers
    application.add_handler(CallbackQueryHandler(handle_catalog, pattern='^catalog$'))
    application.add_handler(CallbackQueryHandler(handle_status, pattern='^status$'))
    application.add_handler(CallbackQueryHandler(handle_help, pattern='^help$'))
    # application.add_handler(CallbackQueryHandler(handle_register, pattern='^register$'))
    application.add_handler(CallbackQueryHandler(handle_manage_orders, pattern='^manage_orders$'))
    application.add_handler(CallbackQueryHandler(button_handler))
    # Выводим сообщение о том, что бот успешно запущен
    print('Telegram бот успешно запущен!')
    application.run_polling()

if __name__ == "__main__":
    setup_bot()
