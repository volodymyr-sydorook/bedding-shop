# orders/views.py
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart  # Нам потрібен наш кошик!
from django.contrib import messages
from .models import Order  # <-- Переконайтеся, що Order імпортовано
from .utils import send_telegram_notification


def order_create(request):
    """
    Обробляє оформлення замовлення, зберігає дані і безумовно перенаправляє на сторінку "Дякуємо"
    (замовлення приймається в обробку менеджером).
    """
    cart = Cart(request)

    if not cart:
        messages.error(request, "Ваш кошик порожній.")
        return redirect('store:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            # 1. Зареєстрований користувач
            if request.user.is_authenticated:
                order.user = request.user

            # 2. Зберігаємо замовлення
            order.save()

            # 2. Виклик сповіщення
            try:
                # 🟢 Переконайтеся, що функція викликається
                send_telegram_notification(order)
            except Exception as e:
                # Це critical, але не повинно ламати клієнтський досвід
                print(f"Критична помилка при відправці Telegram: {e}")
                # 🟢 Додатково виводимо повідомлення для debug
                messages.warning(request, "Помилка при відправці повідомлення в Telegram!")

            # 3. Створення Order Items (знімок кошика)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # 4. Очищення кошика
            cart.clear()

            # 5. ФІНАЛ: Безумовне перенаправлення на сторінку "Дякуємо!"
            # (Це означає, що замовлення прийнято в обробку менеджером)
            return render(request,
                          'orders/order_created.html',
                          {'order': order})

    else:
        # GET: Початкове завантаження сторінки
        form = OrderCreateForm()

        # Заповнення форми даними зареєстрованого користувача
        if request.user.is_authenticated:
            form.initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': request.user.phone_number
            }

    # Рендеринг сторінки
    return render(request,
                  'orders/checkout.html',
                  {'cart': cart, 'form': form})
