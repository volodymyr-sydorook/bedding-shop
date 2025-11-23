# orders/forms.py
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'delivery_method', 'city', 'warehouse',
            'payment_method', 'comment'
        ]
        widgets = {
            'delivery_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Наприклад: код домофону 35'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо клас form-control до всіх текстових полів
        for field_name, field in self.fields.items():
            if field_name not in ['delivery_method', 'payment_method']:
                field.widget.attrs['class'] = 'form-control'
