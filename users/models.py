from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Розширена модель користувача.
    Поля username, email, first_name, last_name вже є у AbstractUser.
    Ми додаємо лише те, що нам потрібно додатково.
    """
    phone_number = models.CharField(
        max_length=20,
        blank=True,  # Поле не обов'язкове (наприклад, для адміна)
        null=True,  # Дозволяємо базі даних зберігати NULL
        verbose_name="Номер телефону"  # Гарна назва для адмінки
    )

    # verbose_name = "Користувач" # (Опціонально)
    # verbose_name_plural = "Користувачі" # (Опціонально)

    def __str__(self):
        # Цей метод визначає, як користувач буде відображатися
        # в адмінці (наприклад, у списку замовлень)
        return self.username
