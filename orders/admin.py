from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Це "вбудована" форма, яка дозволяє показувати
    та редагувати OrderItem прямо на сторінці Order.
    """
    model = OrderItem
    raw_id_fields = ['product']  # Зручний віджет для вибору товару, якщо треба додати
    extra = 0  # Не показувати порожні форми для додавання
    readonly_fields = ['price', 'quantity']  # Забороняємо міняти ціну/кількість з адмінки замовлення


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone_number', 'status', 'created']
    list_filter = ['status', 'created', 'updated']  # Фільтри збоку
    search_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

    # ВАЖЛИВО: Підключаємо наші товари
    inlines = [OrderItemInline]
