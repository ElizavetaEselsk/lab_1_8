import numpy as np
import skimage.io
from PIL import Image
from PIL import Image

import config
import metrix


# сокрытие сообщения
def hide_message(message_bits, picture):
    # Проверка вместимости стегоконтейнера (по длине сообщения )
    if len(message_bits) > picture.shape[0] * picture.shape[1] * picture.shape[2]:
        print("Не получится")
        return picture
    # Получение размерности массива
    picture_shape = picture.shape
    # Зануление последних двух битов каждого байта изображения и преобразование в одномерный массив
    picture = ((picture >> 1) << 1).reshape(-1)
    message_bits = np.asarray(message_bits)
    # получение размерности массива битов сообщения
    bits_length = message_bits.shape[0]
    # Битовое сложение каждого байта изображения с битом сообщения
    picture[:bits_length] = picture[:bits_length] | message_bits
    # Преобразование массива в исходную размерность
    return picture.reshape(picture_shape)


# сообщение из картинки
def get_message_from_image(picture):
    # картинка -> одномерный массив и битовое умножение с 0x01
    picture = picture.reshape(-1) & 0x01
    # Отсечение лишних битов и преобразование в массив [количествобайт х 8]
    message = picture[:(picture.shape[0] // 8) * 8].reshape(-1, 8)
    # Получение байтов сообщения до первого нулевого байта и преобразования в одномерный массив
    return message[~np.all(message == 0, axis=1)].reshape(-1)


# чтение картинки
def read_image(path):
    image = skimage.io.imread(path)
    return image


# строка -> массив битов
def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


# массив бит -> строку
def from_bits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)




if __name__ == "__main__":
    # Чтение картинки
    image = read_image(config.IMG_PATH)

    # Чтение сообщения
    lines = []
    with open(config.MESSAGE_PATH) as f:
        for line in f:
            lines.append(line)
    text = ''.join(lines)
    # изображение -> массив битов
    bites = to_bits(text)
    # Получение заполненного стегоконтейнера
    encoded_image = hide_message(bites, image)
    im = Image.fromarray(encoded_image)
    im.save(config.ENCODE_PATH)
    # Получение соолбщения из заполненного стегокнтейнера
    decoded_bits_message = get_message_from_image(encoded_image)
    # строка полученного массива битов сообщения
    print(from_bits(decoded_bits_message))
    # подсчет метрик на основе незаполненного и заполненного контейнеров

    img = Image.open(config.IMG_PATH)
    enc = Image.open(config.ENCODE_PATH)
    w = img.size[0]
    h = img.size[1]
    img = img.load()
    enc = enc.load()

    print(f'NMSE = {metrix.NMSE(w, h, img, enc)}')

    print(f'MSE = {metrix.MSE(w, h, img, enc)}')
    print(f'LMSE = {metrix.LMSE(w, h, img, enc)}')

