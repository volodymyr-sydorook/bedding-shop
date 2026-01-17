# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    fields = ('product', 'price', 'quantity')
    readonly_fields = ['price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # 🟢 1. МЕТОД ДЛЯ СУМИ (Залишаємо, як було)
    def get_total_cost(self, obj):
        return f"{obj.get_total_cost()} UAH"

    get_total_cost.short_description = 'Сума (UAH)'

    # 🟢 2. МЕТОД ДЛЯ ВИВЕДЕННЯ СПИСКУ ТОВАРІВ У ЗАГАЛЬНУ ТАБЛИЦЮ
    def get_item_summary(self, obj):
        """Форматує назви товарів та кількість у зручний рядок."""
        # Обмежуємо до перших 2-3 позицій для таблиці
        items = obj.items.all()[:3]
        summary = [f"{item.product} ({item.quantity} шт.)" for item in items]
        if obj.items.count() > 3:
            summary.append(f"... та ще {obj.items.count() - 3}")
        return " | ".join(summary)

    get_item_summary.short_description = 'Товари (Коротко)'  # Назва колонки

    # 3. СПИСОК ВІДОБРАЖЕННЯ (list_display)
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'city',
        'delivery_method',
        'status',
        'get_total_cost',
        'get_item_summary',  # <-- ДОДАНО: Короткий список товарів
        'created'
    ]
    list_filter = ['status', 'created', 'delivery_method']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'city']
    inlines = [OrderItemInline]
