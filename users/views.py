# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages  # <-- Додайте цей імпорт!


def register(request):
    """
    View для реєстрації нового користувача.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Одразу логінимо користувача після реєстрації (зручно!)
            login(request, user)
            return redirect('store:product_list')  # Перекидаємо на головну
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # Якщо прийшли дані з форми оновлення
        # instance=request.user означає, що ми редагуємо поточного юзера, а не створюємо нового
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            # Додаємо "флеш-повідомлення" (воно покажеться в base.html)
            messages.success(request, 'Ваш профіль успішно оновлено!')
            return redirect('users:profile')

    else:
        # Якщо це GET-запит, просто показуємо форму, заповнену даними юзера
        form = UserUpdateForm(instance=request.user)

    # Отримуємо замовлення
    orders = request.user.orders.all()

    context = {
        'form': form,
        'orders': orders
    }

    return render(request, 'users/profile.html', context)
