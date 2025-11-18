# cart/context_processors.py (новий файл)
from .cart import Cart


def cart(request):
    """
    Робить об'єкт 'cart' доступним у всіх шаблонах.
    """
    return {'cart': Cart(request)}
