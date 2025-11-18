# orders/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart  # Нам потрібен наш кошик!


def order_create(request):
    """
    View для створення замовлення.
    """
    cart = Cart(request)  # Отримуємо кошик з сесії

    if request.method == 'POST':
        # --- 1. Якщо форма відправлена (POST) ---
        form = OrderCreateForm(request.POST)

        # Перевіряємо, чи дані коректні
        if form.is_valid():
            order = form.save(commit=False)  # Створюємо об'єкт 'Order', але не зберігаємо в базу

            # --- Ваша логіка з зареєстрованим юзером ---
            if request.user.is_authenticated:
                # Якщо юзер залогінений, прив'язуємо замовлення до нього
                order.user = request.user
            # -----------------------------------------------

            order.save()  # Тепер зберігаємо замовлення в базу

            # --- 2. Створюємо OrderItem для кожного товару ---
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

                # (Додатково: відняти 'stock' у товару)
                # product = item['product']
                # product.stock -= item['quantity']
                # product.save()

            # --- 3. Очищуємо кошик ---
            cart.clear()

            # --- 4. Перекидаємо на сторінку "Дякуємо" ---
            # Ми передаємо ID замовлення на сторінку успіху
            return render(request,
                          'orders/order_created.html',
                          {'order': order})

    else:
        # --- 5. Якщо це GET-запит (просто завантажили сторінку) ---
        form = OrderCreateForm()

        # --- Ваша логіка: заповнити поля, якщо юзер залогінений ---
        if request.user.is_authenticated:
            form.initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': request.user.phone_number
            }
        # --------------------------------------------------------

    # Рендеримо сторінку з формою
    return render(request,
                  'orders/checkout.html',
                  {'cart': cart, 'form': form})
