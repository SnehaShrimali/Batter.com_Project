import os
import django
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_project.settings')
django.setup()

from django.core.files.base import ContentFile
from properties.models import Property
from PIL import Image, ImageDraw, ImageFont

PROPERTY_COLORS = {
    'house': (52, 152, 219),
    'apartment': (46, 204, 113),
    'condo': (155, 89, 182),
    'townhouse': (230, 126, 34),
    'land': (39, 174, 96),
    'commercial': (231, 76, 60),
}

def generate_property_image(property_type, title, size=(800, 500)):
    color = PROPERTY_COLORS.get(property_type, (52, 152, 219))
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)

    for i in range(0, size[0], 40):
        for j in range(0, size[1], 40):
            draw.rectangle([i, j, i+20, j+20], fill=(color[0]+20, color[1]+20, color[2]+20))

    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_type = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_type = ImageFont.load_default()

    cx, cy = size[0] // 2, size[1] // 2 - 40
    draw.polygon([(cx-60, cy+20), (cx, cy-50), (cx+60, cy+20)], fill='white', outline='white')
    draw.rectangle([cx-30, cy+20, cx+30, cy+60], fill='white')

    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((size[0]-tw)//2, cy+80), title, fill='white', font=font_title)

    type_text = property_type.upper()
    bbox = draw.textbbox((0, 0), type_text, font=font_type)
    tw = bbox[2] - bbox[0]
    draw.text(((size[0]-tw)//2, cy+120), type_text, fill=(255,255,255,180), font=font_type)

    brand = "Barter.com"
    bbox = draw.textbbox((0, 0), brand, font=font_type)
    tw = bbox[2] - bbox[0]
    draw.text(((size[0]-tw)//2, cy+160), brand, fill=(255,255,255,100), font=font_type)

    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue())

def main():
    properties = Property.objects.all()
    if not properties:
        print("No properties found.")
        return

    for prop in properties:
        filename = f"{prop.slug or 'property'}.jpg"
        image_content = generate_property_image(prop.property_type, prop.title)

        if prop.main_image:
            prop.main_image.delete(save=False)

        prop.main_image.save(filename, image_content, save=True)
        print(f"OK - {prop.title}")

    print(f"\nDone! Generated {properties.count()} images.")

if __name__ == '__main__':
    main()
