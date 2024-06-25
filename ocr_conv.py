import pytesseract 
import cv2 as cv
path = 'images/recorte_jornal2.png'
imagem = cv.imread(path)

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

if imagem is None:
    print("Não foi possivel ler a imagem")
else:
    pdf = pytesseract.image_to_pdf_or_hocr(imagem, extension='pdf')
    with open('imagem.pdf', 'w+b') as f:
        f.write(pdf)
    # texto = pytesseract.image_to_string(imagem)
    # pytesseract.image_to_pdf_or_hocr(imagem)
    # print(texto)
