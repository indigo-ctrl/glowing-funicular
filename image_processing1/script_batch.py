from PIL import Image, ImageDraw, ImageFont
import os

def process_image(input_path, output_path, watermark_text="@developer"):
    """Обрабатывает одно изображение: ресайз + водяной знак"""
    
    try:
        with Image.open(input_path) as img:
            # Создаем копию для работы
            working_img = img.copy()
            
            # Ресайз до ширины 800px (только если изображение больше)
            if working_img.width > 800:
                new_height = int((800 / working_img.width) * working_img.height)
                working_img = working_img.resize((800, new_height), Image.Resampling.LANCZOS)
            
            # Добавляем водяной знак
            if watermark_text:
                draw = ImageDraw.Draw(working_img)
                
                try:
                    # Пробуем использовать системный шрифт
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    try:
                        # Альтернативный шрифт для Linux/Mac
                        font = ImageFont.truetype("DejaVuSans.ttf", 20)
                    except:
                        # Если шрифты не найдены, используем стандартный
                        font = ImageFont.load_default()
                
                # Получаем размеры текста
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Позиция в правом нижнем углу с отступом
                margin = 10
                x = working_img.width - text_width - margin
                y = working_img.height - text_height - margin
                
                # Рисуем текст с черной обводкой для читаемости
                draw.text((x-1, y-1), watermark_text, font=font, fill="black")
                draw.text((x+1, y-1), watermark_text, font=font, fill="black")
                draw.text((x-1, y+1), watermark_text, font=font, fill="black")
                draw.text((x+1, y+1), watermark_text, font=font, fill="black")
                draw.text((x, y), watermark_text, font=font, fill="white")
            
            # Сохраняем результат
            working_img.save(output_path, "JPEG", quality=85)
            return True
            
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {e}")
        return False

def process_folder(input_folder, output_folder, watermark_text):
    """Обрабатывает все изображения в папке"""
    
    # Создаем папку output если её нет
    os.makedirs(output_folder, exist_ok=True)
    
    # Поддерживаемые форматы
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    
    # Счетчики
    processed_count = 0
    error_count = 0
    
    # Обрабатываем каждый файл
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            
            # Создаем новое имя файла
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_processed.jpg"
            output_path = os.path.join(output_folder, output_filename)
            
            # Обрабатываем изображение
            if process_image(input_path, output_path, watermark_text):
                print(f"✓ Обработано: {filename}")
                processed_count += 1
            else:
                print(f"✗ Ошибка: {filename}")
                error_count += 1
    
    return processed_count, error_count

if __name__ == "__main__":
    print("=== ПАКЕТНАЯ ОБРАБОТКА ИЗОБРАЖЕНИЙ ===")
    
    input_dir = "./input"
    output_dir = "./output"
    watermark = "© Developer Team 2024"
    
    # Проверяем существование папки input
    if not os.path.exists(input_dir):
        print(f"Папка {input_dir} не существует!")
        exit(1)
    
    processed, errors = process_folder(input_dir, output_dir, watermark)
    
    print(f"\n=== РЕЗУЛЬТАТЫ ===")
    print(f"Успешно обработано: {processed}")
    print(f"С ошибками: {errors}")
    print(f"Всего: {processed + errors}")
