# -*- coding: utf8-*-
from pytesseract import image_to_string
from PIL import Image


def to_string(filename):
    image = Image.open(filename + '.jpg')
    lang = 'eng'
    config = '-psm 10 -c tessedit_char_whitelist="ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"'
    if filename == '1':
        lang = 'chi_sim'
        config = '-psm 10 -c tessedit_char_whitelist="辽吉黑冀晋陕鲁皖苏浙豫鄂湘赣台闽滇琼川黔粤甘青渝沪津京宁蒙藏新贵港澳"'
    char = image_to_string(image, lang=lang, config=config)
    print filename + '.jpg', char
    return char


