from PIL import Image, ImageDraw
import random
import math
import os

def create_generative_art(width=800, height=600, filename="./output/generative_art.png"):
    """Создает генеративное абстрактное изображение"""
    
    # Создаем папку output если её нет
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Создаем новое изображение с градиентным фоном
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Создаем градиентный фон
    for y in range(height):
        # Плавное изменение цвета от синего к фиолетовому
        r = int(50 + 50 * math.sin(y / height * math.pi))
        g = int(50 + 50 * math.sin(y / height * math.pi * 2))
        b = int(150 + 50 * math.cos(y / height * math.pi))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Генерируем случайные круги с разной прозрачностью
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(20, 150)
        
        # Создаем изображение для круга с альфа-каналом
        circle_img = Image.new('RGBA', (radius*2, radius*2), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        
        color = (
            random.randint(100, 255),
            random.randint(100, 255), 
            random.randint(100, 255),
            random.randint(50, 150)  # Альфа-канал
        )
        
        circle_draw.ellipse([0, 0, radius*2, radius*2], fill=color)
        img.paste(circle_img, (x-radius, y-radius), circle_img)
    
    # Добавляем структурные линии
    for _ in range(15):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        
        line_color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255)
        )
        
        draw.line([x1, y1, x2, y2], fill=line_color, width=random.randint(1, 4))
    
    # Добавляем случайные треугольники
    for _ in range(10):
        points = []
        for _ in range(3):
            points.append((random.randint(0, width), random.randint(0, height)))
        
        triangle_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(100, 200)
        )
        
        triangle_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        triangle_draw = ImageDraw.Draw(triangle_img)
        triangle_draw.polygon(points, fill=triangle_color)
        img = Image.alpha_composite(img.convert('RGBA'), triangle_img)
    
    # Сохраняем результат
    img.convert('RGB').save(filename, "PNG")
    print(f"✓ Генеративное искусство сохранено как {filename}")

def create_collage(image_paths, output_path, collage_size=(1200, 800)):
    """Создает коллаж из нескольких изображений"""
    
    collage = Image.new('RGB', collage_size, 'white')
    draw = ImageDraw.Draw(collage)
    
    # Добавляем градиентный фон для коллажа
    for y in range(collage_size[1]):
        color = (240 - int(y / collage_size[1] * 40), 
                240 - int(y / collage_size[1] * 40), 
                255)
        draw.line([(0, y), (collage_size[0], y)], fill=color)
    
    x_offset = 50
    y_offset = 50
    max_height = 0
    
    for i, img_path in enumerate(image_paths):
        try:
            with Image.open(img_path) as img:
                # Ресайзим изображения для коллажа
                img.thumbnail((300, 300))
                
                # Если изображение не помещается в строку, переходим на новую
                if x_offset + img.width > collage_size[0] - 50:
                    x_offset = 50
                    y_offset += max_height + 20
                    max_height = 0
                
                # Добавляем белую рамку вокруг изображения
                frame_size = (img.width + 10, img.height + 10)
                frame = Image.new('RGB', frame_size, 'white')
                frame.paste(img, (5, 5))
                
                collage.paste(frame, (x_offset, y_offset))
                x_offset += frame_size[0] + 20
                max_height = max(max_height, frame_size[1])
                
        except Exception as e:
            print(f"Ошибка при добавлении {img_path} в коллаж: {e}")
    
    collage.save(output_path, "JPEG", quality=90)
    print(f"✓ Коллаж сохранен: {output_path}")

if __name__ == "__main__":
    print("=== ГЕНЕРАТИВНОЕ ИСКУССТВО И КОЛЛАЖИ ===")
    
    # Создаем 3 разных варианта генеративного искусства
    for i in range(3):
        create_generative_art(
            width=random.randint(600, 1000),
            height=random.randint(400, 800),
            filename=f"./output/generative_art_{i+1}.png"
        )
    
    # Создаем коллаж из обработанных изображений
    try:
        # Ищем обработанные изображения
        processed_images = []
        for file in os.listdir("./output"):
            if file.endswith("_processed.jpg"):
                processed_images.append(os.path.join("./output", file))
        
        if processed_images:
            create_collage(processed_images[:4], "./output/collage.jpg")
        else:
            print("Не найдены обработанные изображения для коллажа")
            
    except Exception as e:
        print(f"Ошибка при создании коллажа: {e}")
    
    print("Генерация завершена!")
