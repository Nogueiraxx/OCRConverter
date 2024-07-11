from reportlab.lib.pagesizes import letter
from customtkinter import filedialog 
from reportlab.pdfgen import canvas
from customtkinter import *
from reportlab.lib.units import inch
# from PIL import Image
import numpy as np
import pytesseract 
import cv2 as cv
import glob
import PIL
import os

def imgToString(imgPath):

    img = cv.imread(imgPath)

    try:
        text = pytesseract.image_to_string(img, lang='por')
        return text
    except  FileNotFoundError:
        error = "404"
        return error
    

def pdfCreator(text, path, imgName):

    # Configuração do PDF
    full_path = os.path.join(path, imgName)
    doc = canvas.Canvas(full_path + '.pdf', pagesize=letter)
    width, height = letter
    margin = inch
    text_object = doc.beginText(margin, height - margin)
    text_object.setFont("Helvetica", 12)

    #Texto com quebra de linha
    linhas = text.split('\n')
    for linha in linhas:
        text_object.textLine(linha)

    doc.drawText(text_object)
    doc.showPage()

    doc.save()

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

imgPath = r"C:\Users\Jaime Nogueira\Desktop\Bagunca\teste\recorte_jornal.png"
imgPthDst = r"C:\Users\Jaime Nogueira\Desktop\Bagunca\arquivosConvertidosEstagio"
imgName = "recorte_jornal.png"
texto = imgToString(imgPath)
pdfCreator(texto, imgPthDst, imgName)