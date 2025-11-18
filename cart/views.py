# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart  # Наш клас


@require_POST  # Дозволяємо тільки POST-запити (бо ми змінюємо дані)
def cart_add(request, product_id):
    """
    View для додавання товару в кошик.
    """
    cart = Cart(request)  # Ініціалізуємо кошик
    product = get_object_or_404(Product, id=product_id)

    # Отримуємо дані з форми (кількість)
    quantity = int(request.POST.get('quantity', 1))
    # (Тут треба додати валідацію, щоб кількість не перевищувала 'stock')

    cart.add(product=product, quantity=quantity)

    # Повертаємо користувача на сторінку, з якої він прийшов
    # (або на сторінку кошика)
    return redirect('cart:cart_detail')  # Перекидаємо на сторінку кошика


def cart_remove(request, product_id):
    """
    View для видалення товару.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    View для сторінки самого кошика (де список товарів).
    """
    cart = Cart(request)
    # Ми передаємо 'cart' напряму, бо в ньому є __iter__
    return render(request, 'cart/cart_detail.html', {'cart': cart})
