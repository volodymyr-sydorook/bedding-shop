# cart/urls.py (новий файл)
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Сторінка самого кошика
    path('', views.cart_detail, name='cart_detail'),
    # URL для додавання (ми використовуємо product_id)
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # URL для видалення
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
