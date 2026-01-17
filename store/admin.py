from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # Ця магія автоматично заповнює поле 'slug'
    # на основі поля 'name' (транслітом, якщо налаштовано)
    prepopulated_fields = {'slug': ('name',)}


# --- Тепер зробимо зручний інтерфейс для Товарів ---

class ProductImageInline(admin.TabularInline):
    """
    Це "вбудована" форма для додавання фотографій
    прямо на сторінці товару.
    """
    model = ProductImage
    extra = 1  # Кількість порожніх форм для завантаження нових фото


class ProductVariantInline(admin.TabularInline):
    """
    "Вбудована" форма для додавання варіацій (розмірів, кольорів).
    """
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created']

    # Фільтри, які будуть збоку
    list_filter = ['available', 'category', 'created']

    # Поля, які можна редагувати прямо зі списку (дуже зручно!)
    list_editable = ['price', 'stock', 'available']

    # Додаємо пошук
    search_fields = ['name', 'description']

    # Автозаповнення slug
    prepopulated_fields = {'slug': ('name',)}  # Так, у товарів теж має бути slug для гарних URL

    # !!! Підключаємо наші "вбудовані" форми !!!
    inlines = [ProductVariantInline, ProductImageInline]

# Можна також зареєструвати моделі окремо, але це не так зручно
# admin.site.register(ProductImage)
# admin.site.register(ProductVariant)
