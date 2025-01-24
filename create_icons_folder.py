import os
import base64
import json

def create_icons():
    # دیکشنری شامل آیکون‌های base64 encoded
    icons_data = {
        "clear.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "cloudy.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "rain.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "drizzle.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "thunderstorm.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "snow.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "mist.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0...",
        "default.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0..."
    }

    # ایجاد پوشه icons اگر وجود نداشته باشد
    if not os.path.exists('icons'):
        os.makedirs('icons')

    # ذخیره هر آیکون در فایل جداگانه
    for filename, base64_data in icons_data.items():
        icon_path = os.path.join('icons', filename)
        with open(icon_path, 'wb') as f:
            f.write(base64.b64decode(base64_data))

if __name__ == "__main__":
    create_icons() 