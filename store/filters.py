# store/filters.py (новий файл)
import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    # Фільтр за ціною "від" і "до"
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label="Ціна від")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label="Ціна до")

    # Фільтр за категорією (випадаючий список)
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Категорія")

    class Meta:
        model = Product
        fields = ['category']  # Поля моделі, які ми використовуємо
