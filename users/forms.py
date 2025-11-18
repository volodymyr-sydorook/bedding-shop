# users/forms.py (новий файл)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")  # Робимо email обов'язковим

    class Meta:
        model = User
        # Вказуємо, які поля будуть при реєстрації
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']


class UserUpdateForm(forms.ModelForm):
    """Форма для оновлення даних профілю"""
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    # Додамо трохи краси для полів через віджети (опціонально, але корисно)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
