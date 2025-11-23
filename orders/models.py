from decimal import Decimal

from django.db import models
from django.conf import settings
from store.models import Product  # Нам потрібна модель Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('completed', 'Виконано'),
        ('canceled', 'Скасовано'),
    ]

    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова Пошта'),
        ('ukr_poshta', 'Укрпошта'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Накладений платіж (Оплата при отриманні)'),
        ('card', 'Оплата карткою'),  # Це тепер лише індикація для менеджера
    ]
    # ---

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='orders', verbose_name="Користувач")

    # Основні дані
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")

    # Дані доставки
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='nova_poshta',
                                       verbose_name="Спосіб доставки")
    city = models.CharField(max_length=100, verbose_name="Місто / Населений пункт", default="")
    warehouse = models.CharField(max_length=100, verbose_name="Відділення / Поштомат", default="")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod',
                                      verbose_name="Спосіб оплати")  # Зберігаємо для менеджера
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар до замовлення")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ('-created',)

    def __str__(self):
        return f"Замовлення №{self.id}"

    def get_total_cost(self):
        # 🟢 ВИПРАВЛЕНО: Додаємо Decimal(0) як початкове значення для sum().
        # Це гарантує, що тип результату завжди буде Decimal.
        return sum((item.get_cost() for item in self.items.all()), Decimal(0))


class OrderItem(models.Model):
    """
    Конкретний товар в конкретному замовленні.
    """
    order = models.ForeignKey(Order,
                              related_name='items',  # Дозволяє з Order отримати .items.all()
                              on_delete=models.CASCADE)  # Видалити товар, якщо видалили замовлення

    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.SET_NULL,  # Якщо товар видалять з каталогу,
                                null=True)  # він лишиться в історії замовлень

    # ВАЖЛИВО: Ми зберігаємо ціну на момент покупки!
    # Якщо адмін змінить ціну на товар, в старих замовленнях вона не зміниться.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна на момент покупки")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    class Meta:
        verbose_name = "Товар у замовленні"
        verbose_name_plural = "Товари у замовленні"

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Рахує вартість позиції (ціна * кількість)"""
        # 🟢 ВИПРАВЛЕНО: Явно приводимо результат до Decimal, хоча Django має це робити сам.
        return self.price * self.quantity