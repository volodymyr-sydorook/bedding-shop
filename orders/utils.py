# orders/utils.py
import requests
from django.conf import settings
from decimal import Decimal


def send_telegram_notification(order):
    """Надсилає деталі замовлення менеджеру."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_MANAGER_CHAT_ID

    # Захист від відправлення порожніх токенів
    if not token or chat_id == 'ВСТАВТЕ_ЧИСЛОВИЙ_ID_ЧАТУ':
        print("ПОМИЛКА: Телеграм токен або Chat ID не налаштовані!")
        return

    # --- Формування повідомлення ---
    total_cost = order.get_total_cost()

    message_text = (
        f"🚨 *НОВЕ ЗАМОВЛЕННЯ* №{order.id}\n"
        f"_______________________________________\n"
        f"💰 *Сума:* {total_cost} UAH\n"
        f"🚚 *Доставка:* {order.get_delivery_method_display()}\n"
        f"💳 *Оплата:* {order.get_payment_method_display()}\n"
        f"📍 *Куди:* {order.city}, {order.warehouse}\n"
        f"_______________________________________\n"
        f"👤 *Клієнт:* {order.first_name} {order.last_name}\n"
        f"📞 *Телефон:* {order.phone_number}\n"
        f"📧 *Email:* {order.email}\n"
    )

    if order.comment:
        message_text += f"\n💬 *Коментар:* {order.comment}"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'  # Використовуємо Markdown для жирного тексту
    }

    try:
        # Відправка запиту до Telegram API
        response = requests.post(url, data=payload, timeout=5)  # Обмеження часу, щоб не гальмувати сайт
        response.raise_for_status()  # Викликає помилку для поганих статусів (4xx або 5xx)
        print(f"Telegram Notification sent for Order {order.id}")
    except requests.exceptions.RequestException as e:
        # Логуємо помилку, але дозволяємо замовленню завершитися
        print(f"Telegram notification FAILED for Order {order.id}: {e}")
