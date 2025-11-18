# core/urls.py

from django.contrib import admin
from django.urls import path, include

# --- ПЕРЕВІРТЕ, ЩО ЦІ ДВА ІМПОРТИ Є ---
from django.conf import settings
from django.conf.urls.static import static

# ---

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # <-- ДОДАЙТЕ ЦЕ
    path('cart/', include('cart.urls')),  # <-- ДОДАЙТЕ ЦЕЙ РЯДОК
    path('orders/', include('orders.urls')),  # <-- ДОДАЙТЕ ЦЕЙ РЯДОК
    path('', include('store.urls')),

]

# --- ПЕРЕВІРТЕ, ЩО ЦЕЙ БЛОК Є В КІНЦІ ФАЙЛУ ---
# Цей блок "вмикає" роздачу файлів з MEDIA_URL
# ТІЛЬКИ в режимі розробки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
