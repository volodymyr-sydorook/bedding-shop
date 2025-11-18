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

    # --- 1. Зв'язок з Користувачем ---
    # Якщо користувач зареєстрований, прив'язуємо замовлення до нього.
    # on_delete=models.SET_NULL: якщо видалити юзера, замовлення лишиться.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True, blank=True,  # Дозволяємо порожнє поле (для гостей)
                             related_name='orders',
                             verbose_name="Користувач")

    # --- 2. Дані для гостьового замовлення ---
    # Як ви й просили: якщо гість, він вказує ці дані.
    # Якщо зареєстрований, ми їх заповнимо автоматично.
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")

    # --- 3. Інформація про замовлення ---
    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='new',
                              verbose_name="Статус")

    # (Ми будемо розраховувати загальну суму пізніше,
    # але можна зберігати її тут)
    # total_price = models.DecimalField(...)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ('-created',)  # Найновіші замовлення зверху

    def __str__(self):
        return f"Замовлення №{self.id} ({self.status})"

    def get_total_cost(self):
        """Рахує загальну вартість всіх товарів у цьому замовленні."""
        return sum(item.get_cost() for item in self.items.all())


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
        return self.price * self.quantity
