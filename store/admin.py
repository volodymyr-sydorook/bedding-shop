from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant

import requests
from django.contrib import admin
from django.utils.html import strip_tags
from urllib.parse import quote
from django.http import HttpResponseRedirect  # Щоб перенаправити вас у Viber
from django.conf import settings
from .models import Product
import requests  # Для Telegram залишаємо


# --- ВАРІАНТ: ВІДПРАВКА ВІД ВАШОГО ІМЕНІ (Клік-шеринг) ---
@admin.action(description="👤 Відкрити в Telegram (від мого імені)")
def share_to_telegram_user(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "⚠️ Оберіть лише ОДИН товар для ручного постингу.", level='ERROR')
        return

    product = queryset.first()

    # 1. Формуємо посилання на товар
    product_link = f"https://beddingshop.shop/product/{product.slug}/"

    # 2. Формуємо красивий текст
    text = (
        f"*{product.name}*\n\n"  # Жирний шрифт у Markdown
        f"{strip_tags(product.description)[:200]}...\n\n"
        f"💰 *Ціна: {product.price} грн*\n"
    )

    # 3. Кодуємо текст для URL
    # Telegram Share Link приймає два параметри: url (посилання на товар) і text (опис)
    encoded_text = quote(text)
    encoded_url = quote(product_link)

    # 4. Створюємо посилання t.me/share
    # Воно відкриє додаток Telegram на телефоні або ПК
    telegram_link = f"https://t.me/share/url?url={encoded_url}&text={encoded_text}"

    # 5. Перенаправляємо вас туди
    return HttpResponseRedirect(telegram_link)


# 👇 1. ДОДАЙТЕ ЦЕЙ КЛАС (Він дозволяє протокол viber://)
class ViberRedirect(HttpResponseRedirect):
    allowed_schemes = ['http', 'https', 'viber']


@admin.action(description="💜 Відкрити у Viber (для репосту)")
def share_to_viber(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "⚠️ Для Viber оберіть лише ОДИН товар за раз.", level='ERROR')
        return

    product = queryset.first()

    # Формуємо текст
    product_url = f"https://beddingshop.shop/product/{product.slug}/"
    text = f"{product.name}\n🔥 Ціна: {product.price} грн\n\nЗамовити тут: {product_url}"

    encoded_text = quote(text)

    # Створюємо посилання
    viber_link = f"viber://forward?text={encoded_text}"

    # 👇 2. ВИКОРИСТОВУЄМО НАШ НОВИЙ КЛАС ЗАМІСТЬ ЗВИЧАЙНОГО
    return ViberRedirect(viber_link)


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

    # 👇 ДОДАЄМО НАШІ ДІЇ ТУТ 👇
    actions = [share_to_telegram_user, share_to_viber]

# Можна також зареєструвати моделі окремо, але це не так зручно
# admin.site.register(ProductImage)
# admin.site.register(ProductVariant)
