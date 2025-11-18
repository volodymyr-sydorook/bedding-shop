# orders/urls.py (новий файл)
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.order_create, name='order_create'),
    # (Ми не робимо окремий URL для "order_created",
    # бо вона рендериться тією ж view 'order_create')
]
