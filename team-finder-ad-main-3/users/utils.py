import io
import os
import random
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

# Константы для аватаров
AVATAR_COLORS = [
    (173, 216, 230), (144, 238, 144), (255, 182, 193),
    (255, 218, 185), (221, 160, 221), (240, 230, 140), (200, 200, 200),
]
AVATAR_SIZE = (200, 200)
AVATAR_TEXT_COLOR = (50, 50, 50)

# Шрифт со своим файлом кладём прямо в проект: у Pillow нет встроенного
# шрифта с кириллицей, а системный Arial есть только на Windows —
# на сервере (Linux) его нет, и буквы вроде "А" не отображались бы.
AVATAR_FONT_PATH = settings.BASE_DIR / "static" / "fonts" / "DejaVuSans-Bold.ttf"


def generate_avatar(name):
    """Генерирует аватар с первой буквой имени на цветном фоне"""
    initial = name[0].upper() if name else 'U'
    
    bg_color = random.choice(AVATAR_COLORS)
    
    img = Image.new('RGB', AVATAR_SIZE, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(str(AVATAR_FONT_PATH), 80)
    except OSError:
        font = ImageFont.load_default()
    
    # Центрирование текста
    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (AVATAR_SIZE[0] - text_width) // 2
    y = (AVATAR_SIZE[1] - text_height) // 2
    
    draw.text((x, y), initial, fill=AVATAR_TEXT_COLOR, font=font)
    
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return InMemoryUploadedFile(
        img_io, 'ImageField', f'avatar_{initial}.png', 'image/png', img_io.getbuffer().nbytes, None
    )