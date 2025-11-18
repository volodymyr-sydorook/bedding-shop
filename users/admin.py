from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Імпортуємо нашу модель


# Ми хочемо додати поле 'phone_number' прямо у список
# та у форму редагування в адмінці.

# Створюємо клас, який наслідує стандартний UserAdmin
class CustomUserAdmin(UserAdmin):
    # Додаємо 'phone_number' до полів, які відображаються при редагуванні
    # fieldsets - це ті блоки, які ви бачите на сторінці редагування
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    # add_fieldsets - це поля, які видно при створенні нового юзера
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    # list_display - це колонки, які видно у списку всіх користувачів
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']


# Реєструємо нашу модель User з нашим кастомним класом
admin.site.register(User, CustomUserAdmin)
