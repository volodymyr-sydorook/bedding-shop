# store/utils.py
import os
import uuid


def unique_slugify(instance, filename):
    """
    Генерує унікальне ім'я для файлу, щоб уникнути кирилиці та дублікатів.
    Приклад: my-image.jpg -> products/a1b2c3d4.jpg
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('products/', filename)
