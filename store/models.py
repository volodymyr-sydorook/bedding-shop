from django.db import models
from django.urls import reverse
# Ми імпортуємо нашу кастомну модель User через settings,
# це найкраща практика в Django.
from django.conf import settings

from store.utils import unique_slugify


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=255, unique=True,
                            help_text="URL-адреса (напр. 'dvospalna-postil'). Заповниться автоматично.")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ('name',)  # Сортуємо категорії за алфавітом

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',  # Як звертатися з боку категорії
                                 on_delete=models.SET_NULL,  # Не видаляти товар, якщо видалили категорію
                                 null=True,
                                 verbose_name="Категорія")

    name = models.CharField(max_length=255, verbose_name="Назва товару")
    slug = models.SlugField(max_length=255, unique=True, blank=True,
                            help_text="URL (заповниться автоматично, якщо порожній)")
    description = models.TextField(verbose_name="Опис", blank=True)

    # Використовуємо DecimalField для грошей, ніколи не float!
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")

    # Наш лічильник "+1/-1" буде спиратися на це поле
    stock = models.PositiveIntegerField(default=0, verbose_name="Кількість на складі")

    main_image = models.ImageField(upload_to=unique_slugify, blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Доступний для продажу")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Товар (постіль)"
        verbose_name_plural = "Товари (постіль)"
        ordering = ('-created',)  # Найновіші товари — зверху

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Повертає URL для сторінки цього товару
        return reverse('store:product_detail', args=[self.slug])


# --- Додаткові, але важливі моделі, які я рекомендував ---

class ProductVariant(models.Model):
    """
    Варіації: Розмір (Євро, Полуторний) або Колір (Синій, Бежевий)
    """
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Наприклад: 'Розмір: King Size' або 'Колір: Білий'")
    # Можна додати окрему ціну або зміну ціни (price_adjustment)
    stock = models.PositiveIntegerField(default=0, verbose_name="Залишок цієї варіації")

    class Meta:
        verbose_name = "Варіація товару"
        verbose_name_plural = "Варіації товару"

    def __str__(self):
        return f"{self.product.name} ({self.name})"


class ProductImage(models.Model):
    """
    Додаткові фото для галереї товару
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_slugify)

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Галерея товару"

    def __str__(self):
        return f"Зображення для {self.product.name}"
