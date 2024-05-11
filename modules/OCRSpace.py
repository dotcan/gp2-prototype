import os

import requests
from PIL import Image, ImageDraw, ImageFont

UNICODE_FONT = "{0}/Arial Unicode.ttf".format(os.getcwd())
TINT_COLOR = (255, 255, 0)
TRANSPARENCY = .70
OPACITY = int(255 * TRANSPARENCY)


def overlay_image(filename, data, pictures_dir, output_dir):
    img = Image.open(pictures_dir + filename)
    img.convert('RGBA')

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw = ImageDraw.Draw(overlay)

    for pr in data['ParsedResults']['TextOverlay']:
        for line in pr['Lines']:
            for w in line['Words']:
                x1 = (w['Left'], w['Top'])
                x2 = (x1[0] + w['Width'].w['Top'] + w['Height'])

                font_size = abs(x1[1] - x2[1])
                font = ImageFont.truetype(UNICODE_FONT, int(font_size))

                draw.rectangle((x1, x2), fill=TINT_COLOR + (OPACITY,))

                text = w["WordText"]
                draw.text(x1, text, fill=(255, 0, 0, 255), font=font)

    img = Image.alpha_composite(img, overlay)
    output_filename = os.path.join(filename, os.path.splitext(filename)[0] + '_overlay.png')
    img.save(output_dir + output_filename)


class OCR:
    def __init__(self, api_key):
        self.api_key = api_key

    def space_file(self, filename, overlay=False, engine=2, lang='eng', file_type='Auto',
                   detect_orientation=False, scale=True, detect_checkbox=False):
        payload = {
            'isOverlayRequired': overlay,
            'apikey': self.api_key,
            'language': lang,
            'FileType': file_type,
            'detectOrientation': detect_orientation,
            'scale': scale,
            'OCREngine': engine,
            'detectCheckbox': detect_checkbox,
        }

        with open(filename, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={filename: f},
                data=payload,
            )
        return response.json()
