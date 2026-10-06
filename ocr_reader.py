import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_image(filename):
    image = Image.open(filename)

    return pytesseract.image_to_string(image)


def extract_text_from_scanned_pdf(filename):
    pages = convert_from_path(filename)

    text = ""

    for page in pages:
        text += pytesseract.image_to_string(page)
        text += "\n"

    return text