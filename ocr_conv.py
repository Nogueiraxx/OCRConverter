import pytesseract
import cv2

imagem = cv2.imread("images\recorte_jornal3.png")

texto = pytesseract.image_to_string(imagem)

print(texto)