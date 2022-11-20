import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image

def check_invalid_type_generator(file: object):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # читать изображение с помощью OpenCV
    image = cv2.imread(file)
    # или вы можете использовать подушку
    # image = Image.open("test.png")

    # получаем строку
    string = pytesseract.image_to_string(image, lang='rus')
    # печатаем
    print(string)

    # чтобы нарисовать сделаем копию изображения
    image_copy = image.copy()
    # слово для поиска
    target_words = {"дизельный", "бензиновый"}
    # получить все данные из изображения
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='rus')

    # получить все вхождения нужного слова
    word_occurences = [ i for i, word in enumerate(data["text"]) if word.lower() in target_words ]

    for occ in word_occurences:
        # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
        w = data["width"][occ]
        h = data["height"][occ]
        l = data["left"][occ]
        t = data["top"][occ]
        # определяем все точки окружающей рамки
        p1 = (l, t)
        p2 = (l + w, t)
        p3 = (l + w, t + h)
        p4 = (l, t + h)
        # рисуем 4 линии (прямоугольник)
        image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)

    plt.imsave("disel.png", image_copy)
    plt.imshow(image_copy)
    plt.show()

    if len(word_occurences) > 0:
        return True

print(check_invalid_type_generator('test.jpg'))

    