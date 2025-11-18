# cart/cart.py (новий файл)
from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    def __init__(self, request):
        """
        Ініціалізуємо кошик.
        Ми отримуємо 'request', щоб отримати доступ до 'request.session'.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Якщо кошика в сесії немає, створюємо порожній
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Додати товар в кошик або оновити його кількість.
        """
        product_id = str(product.id)  # Використовуємо рядок, бо JSON (сесії) вимагає рядкових ключів

        if product_id not in self.cart:
            # Якщо товару ще немає, додаємо його
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            # Логіка для лічильника (+1/-1): просто встановити нову кількість
            self.cart[product_id]['quantity'] = quantity
        else:
            # Логіка для кнопки "Додати": додати +1 до існуючої
            self.cart[product_id]['quantity'] += quantity

        self.save()  # Зберегти зміни в сесії

    def save(self):
        # Позначити сесію як "змінену"
        self.session.modified = True

    def remove(self, product):
        """
        Видалити товар з кошика.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебір товарів у кошику для відображення в шаблонах.
        Ми також дістанемо повні об'єкти Product з бази.
        """
        product_ids = self.cart.keys()
        # Дістаємо об'єкти товарів з бази даних
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product  # Додаємо сам об'єкт товару

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item  # 'yield' робить цей метод генератором

    def __len__(self):
        """
        Підрахунок кількості товарів у кошику.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Підрахунок загальної вартості кошика.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Видалити кошик з сесії
        del self.session[settings.CART_SESSION_ID]
        self.save()
