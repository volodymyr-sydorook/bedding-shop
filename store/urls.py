# store/urls.py (новий файл)
from django.urls import path
from . import views  # Імпортуємо наші майбутні 'views'

app_name = 'store'  # Це важливо для іменування посилань

urlpatterns = [
    # Головна сторінка (каталог)
    path('', views.product_list, name='product_list'),

    # Сторінка конкретного товару
    # <slug:slug>/ - це динамічна частина URL.
    # Django візьме 'moy-komplekt' з URL і передасть у view
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    # --- Нові сторінки ---
    path('info/delivery/', views.delivery, name='delivery'),
    path('info/contacts/', views.contacts, name='contacts'),
]
