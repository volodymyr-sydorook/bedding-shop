from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- 1. Стилізація (Bootstrap) ---
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # --- 2. Переклад назв полів (Labels) ---
        self.fields['username'].label = "Логін (Нікнейм)"
        self.fields['first_name'].label = "Ім'я"
        self.fields['last_name'].label = "Прізвище"
        self.fields['phone_number'].label = "Номер телефону"

        # Переклад полів пароля
        if 'password1' in self.fields:
            self.fields['password1'].label = "Пароль"
        if 'password2' in self.fields:
            self.fields['password2'].label = "Підтвердження пароля"

        # --- 3. Переклад підказок (Help Text) ---

        # Підказка для логіна
        self.fields['username'].help_text = (
            "Обов'язкове поле. Не більше 150 символів. "
            "Тільки літери, цифри та символи @/./+/-/_."
        )

        # Підказка для пароля
        # Ми замінюємо стандартний список вимог на зрозумілий текст
        if 'password1' in self.fields:
            self.fields['password1'].help_text = (
                "Пароль має містити щонайменше 8 символів. "
                "Він не може бути занадто простим або складатися лише з цифр."
            )


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
