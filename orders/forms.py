# orders/forms.py (новий файл)
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма, що базується на моделі Order.
    Django автоматично створить поля, які ми вказали.
    """

    class Meta:
        model = Order
        # Вказуємо, які поля з моделі Order показувати у формі
        fields = ['first_name', 'last_name', 'email', 'phone_number']

        # (Ми не включаємо 'user', бо ми його встановимо автоматично у view)
