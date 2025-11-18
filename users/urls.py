# users/urls.py (новий файл)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Наша реєстрація
    path('register/', views.register, name='register'),

    # Наш профіль
    path('profile/', views.profile, name='profile'),

    # Стандартний вхід (Login)
    # Ми вказуємо template_name, щоб Django знав, де шукати HTML
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Стандартний вихід (Logout)
    # next_page='store:product_list' означає куди перекинути після виходу
    path('logout/', auth_views.LogoutView.as_view(next_page='store:product_list'), name='logout'),
]
