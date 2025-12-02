from PIL import Image, ImageOps


def fix_image_size(input_path, output_path, target_size=(1500, 1000)):
    img = Image.open(input_path)

    # Створюємо нове зображення з потрібним розміром та білим фоном (або чорним)
    new_img = Image.new("RGB", target_size, (255, 255, 255))

    # Зберігаємо пропорції оригіналу
    img.thumbnail(target_size, Image.Resampling.LANCZOS)

    # Вираховуємо позицію для центрування
    x_offset = (target_size[0] - img.width) // 2
    y_offset = (target_size[1] - img.height) // 2

    # Вставляємо оригінал на нове полотно
    new_img.paste(img, (x_offset, y_offset))
    new_img.save(output_path, quality=95)
    print(f"Готово! Збережено як {output_path}")


# Використання
fix_image_size(r"C:\Users\sidor\Desktop\photo_2025-11-29_17-24-36.jpg", "fixed_photo.jpg")