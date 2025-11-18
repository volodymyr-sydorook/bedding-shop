from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .filters import ProductFilter
from .models import Category, Product

from django.db.models import Q  # <-- Додайте цей імпорт


def product_list(request):
    products = Product.objects.filter(available=True)

    # --- ЛОГІКА ПОШУКУ ---
    query = request.GET.get('q')
    if query:
        # Шукаємо або в назві, або в описі (icontains - нечутливий до регістру)
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    # ---------------------

    filter_set = ProductFilter(request.GET, queryset=products)
    if filter_set.is_valid():
        products = filter_set.qs

    context = {
        'products': products,
        'filter': filter_set,
        'search_query': query  # передаємо назад у шаблон, щоб залишити в полі
    }
    # --- ПАГІНАЦІЯ ---
    paginator = Paginator(products, 9)  # Показувати по 9 товарів на сторінці
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    # -----------------

    context = {
        'products': products_page,  # Тепер передаємо не весь список, а тільки сторінку
        'filter': filter_set,
        'search_query': query
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    View для сторінки одного товару.
    'slug' приходить сюди з URL-адреси.
    """
    # get_object_or_404 - зручна функція:
    # 1. Намагається знайти товар за slug.
    # 2. Якщо не знаходить - повертає сторінку 404 (Not Found).
    product = get_object_or_404(Product, slug=slug, available=True)

    # (У майбутньому тут буде логіка додавання в кошик)

    context = {
        'product': product,
    }

    return render(request, 'store/product_detail.html', context)


def delivery(request):
    return render(request, 'store/delivery.html')


def contacts(request):
    return render(request, 'store/contacts.html')
