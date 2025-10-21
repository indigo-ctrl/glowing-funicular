from PIL import Image, ImageDraw
import os
import random

def create_collage_from_folder(folder_path, output_path, rows=2, cols=2):
    """Исправленная функция создания коллажа"""
    
    images = []
    for file in os.listdir(folder_path):
        if file.endswith('.jpg'):
            # БАГ 1: Неправильный путь к файлу
            # ИСПРАВЛЕНИЕ: Используем os.path.join для правильного пути
            img_path = os.path.join(folder_path, file)
            try:
                img = Image.open(img_path)
                images.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {file}: {e}")
    
    if len(images) < rows * cols:
        print(f"Недостаточно изображений: {len(images)} из {rows * cols}")
        return False
    
    # БАГ 2: Предполагаем, что все изображения одинакового размера
    # ИСПРАВЛЕНИЕ: Приводим все к одному размеру
    thumbnail_size = (400, 400)  # Фиксированный размер для всех изображений
    
    resized_images = []
    for img in images:
        img_copy = img.copy()
        img_copy.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        resized_images.append(img_copy)
    
    # Используем размер первого изображения после ресайза
    width, height = resized_images[0].size
    
    collage_width = cols * width
    collage_height = rows * height
    collage = Image.new('RGB', (collage_width, collage_height), color='white')
    
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(resized_images):
                # БАГ 3: Неправильные координаты вставки
                # ИСПРАВЛЕНИЕ: Умножаем на правильные размеры
                x = j * width
                y = i * height
                collage.paste(resized_images[index], (x, y))
    
    collage.save(output_path, "JPEG", quality=90)
    print(f"Коллаж сохранен: {output_path}")
    return True

def create_smart_gradient(size=(400, 400), start_color=(255,0,0), end_color=(0,0,255)):
    """Исправленная функция создания градиента"""
    
    img = Image.new('RGB', size, color=start_color)
    pixels = img.load()  # Более эффективный способ работы с пикселями
    
    for x in range(size[0]):
        for y in range(size[1]):
            # БАГ 4: Неправильная интерполяция цветов
            # ИСПРАВЛЕНИЕ: Интерполируем все три канала правильно
            
            # Вычисляем прогрессию от начала к концу (можно использовать разные алгоритмы)
            progress_x = x / (size[0] - 1) if size[0] > 1 else 0
            progress_y = y / (size[1] - 1) if size[1] > 1 else 0
            
            # Комбинируем прогрессию по X и Y для более интересного градиента
            progress = (progress_x + progress_y) / 2
            
            r = start_color[0] + (end_color[0] - start_color[0]) * progress
            g = start_color[1] + (end_color[1] - start_color[1]) * progress
            # БАГ 5: Синий канал не интерполируется
            # ИСПРАВЛЕНИЕ: Добавляем интерполяцию для синего
            b = start_color[2] + (end_color[2] - start_color[2]) * progress
            
            # Ограничиваем значения и конвертируем в int
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            
            pixels[x, y] = (r, g, b)
    
    return img

# Тестируем исправленные функции
if __name__ == "__main__":
    # Создаем тестовые данные если нужно
    test_gradient = create_smart_gradient((300, 300), (255, 255, 0), (0, 255, 255))
    test_gradient.save("./output/test_gradient.jpg")
    
    # Пытаемся создать коллаж
    create_collage_from_folder("./input", "./output/test_collage.jpg", 2, 2)
