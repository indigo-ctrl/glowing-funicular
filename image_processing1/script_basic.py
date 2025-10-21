from PIL import Image
import os

def basic_operations():
    """Базовые операции с изображением"""
    
    # Создаем папку output если её нет
    os.makedirs("./output", exist_ok=True)
    
    # 1. Открываем изображение
    try:
        image = Image.open("./input/photo1.jpg")
    except FileNotFoundError:
        print("Файл ./input/photo1.jpg не найден!")
        return
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")
        return

    # 2. Показываем информацию о изображении
    print("=== ИНФОРМАЦИЯ О ИЗОБРАЖЕНИИ ===")
    print(f"Формат: {image.format}")
    print(f"Размер: {image.size}") # (width, height)
    print(f"Режим: {image.mode}") # RGB, L (grayscale), etc.

    # 3. Сохраняем в другом формате
    image.save("./output/photo1_basic.png") # Конвертация в PNG
    print("✓ Конвертация в PNG завершена")

    # 4. Изменяем размер (ширина 400px, высота auto)
    new_width = 400
    new_height = int(image.height * new_width / image.width)
    new_size = (new_width, new_height)
    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
    resized_image.save("./output/photo1_resized.jpg")
    print("✓ Изменение размера завершено")

    # 5. Поворачиваем на 45 градусов
    rotated_image = image.rotate(45, expand=True) # expand=True чтобы не обрезать углы
    rotated_image.save("./output/photo1_rotated.jpg")
    print("✓ Поворот завершен")

    # 6. Конвертируем в черно-белое
    grayscale_image = image.convert("L")
    grayscale_image.save("./output/photo1_bw.jpg")
    print("✓ Конвертация в черно-белое завершена")

    # 7. Обрезаем изображение
    # Определяем центр для обрезки
    width, height = image.size
    crop_size = min(width, height) // 3  # Обрезаем до 1/3 от меньшей стороны
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save("./output/photo1_cropped.jpg")
    print("✓ Обрезка завершена")

    print("\nВсе операции успешно завершены! Результаты в папке ./output")

if __name__ == "__main__":
    basic_operations()
