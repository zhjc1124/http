from pytesseract import image_to_string
from PIL import Image


def to_string(filename):
    image = Image.open(filename + '.jpg')
    lang = 'eng'
    if filename == '1':
        lang = 'chi_sim'
    char = image_to_string(image, lang=lang, config='-psm 8')
    print(char)
    return image_to_string(image, lang=lang, config='-psm 8')


