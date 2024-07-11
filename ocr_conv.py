from reportlab.lib.pagesizes import letter
from customtkinter import filedialog 
from reportlab.pdfgen import canvas
import customtkinter 
from reportlab.lib.units import inch
import logging as log
import numpy as np
import pytesseract 
import webbrowser
import cv2 as cv
from PIL import Image
import glob
import os

log.basicConfig(filename='LOGGING.log', level=log.DEBUG, format=" %(levelname)d - %(filename)s - %(lineno)d - %(message)s - %(asctime)s")


def controller():
    formatos = ['*.jpg', '*.jpeg', '*.png']
    counter = 0
    images = []
    
    for formato in formatos:
        images.extend(glob.glob(originDirectory + '/' + formato))
    
    for image in images:
        name = os.path.basename(image)
        if counter == 0:
            enhancedImagesFilePath = subfolderCreator(destinyDirectory, 'Imagem_Melhorada')
        editedImage = color2GrayImage(image, enhancedImagesFilePath)
        convertedText = imgToString(editedImage)
        print(convertedText)
        if convertedText != "404":
            pdfCreator(convertedText, destinyDirectory, name)            
        counter+= 1

    #No final da execução abre a pasta destino 
    webbrowser.open(os.path.realpath(destinyDirectory))

#-----------------------------------------------------------------

def subfolderCreator(base_path, folder_name):
    """
    Cria uma pasta com um nome específico em um caminho determinado.

    Parâmetros:
    - base_path: str - O caminho base onde a nova pasta será criada.
    - folder_name: str - O nome da nova pasta.

    Retorna:
    - str - Caminho completo da pasta criada, ou mensagem se houver erro.
    """
    # Combinar o caminho base com o nome da nova pasta
    full_path = os.path.join(base_path, folder_name)

    # Verificar se a pasta já existe
    if os.path.exists(full_path):
        log.info(f"Pasta '{folder_name}' já existe em: {full_path}")
        return full_path
    else:
        try:
            # Criar a pasta
            os.makedirs(full_path, exist_ok=True)
            return full_path
        except Exception as e:
            log.error(f"Erro ao criar a pasta: {e}")
            return None

#-----------------------------------------------------------------

def selectFile(opc):
    global originDirectory
    global destinyDirectory

    if opc == "1":
        originDirectory = filedialog.askdirectory()
    elif opc == "2":
        destinyDirectory = filedialog.askdirectory()
    return
#-----------------------------------------------------------------

def color2GrayImage(image_path, output_path):
    # Carregar a imagem
    image = cv.imread(image_path)

    #Imagem Preto e Branco
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #Juntando diretório e nome da imagem
    image_name = output_path + r'/' + os.path.basename(image_path)
   
    # Verificar se a imagem foi carregada corretamente
    if gray_image is None:
        log.critical(f"Erro ao carregar a imagem {image_path}")
        return


    cv.imwrite(image_name, gray_image)

    
    log.info(f"Imagem processada e salva em {output_path}")

    return image_name

# ----------------------------------------------------------------

def imgToString(imgPath):

    img = cv.imread(imgPath)

    try:
        text = pytesseract.image_to_string(img, lang='por')
        return text
    except  FileNotFoundError:
        log.error(f"Erro ao converter a imagem: {imgPath} - em texto")
        error = "404"
        return error

# ----------------------------------------------------------------

def updateName(OldImgName):

    formatos = ['.png', '.jpg', '.jpeg']

    if formatos[0] in OldImgName:
        newImageName = OldImgName.replace('.png', '')
    elif formatos[1] in OldImgName:
        newImageName = OldImgName.replace('.jpg', '')
    elif formatos[2] in OldImgName:
        newImageName = OldImgName.replace('.jpeg', '')

    return newImageName

#---------------------------------------------------

def pdfCreator(text, path, imgName):

    #Tira a extensão do nome do arquivo
    name = updateName(imgName)

    # Configuração do PDF
    full_path = os.path.join(path, name)
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

#-----------------------------------------------------------------



# #Troca do caminho de instalação nas variáveis de ambiente.
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


program = customtkinter.CTk()
program.geometry("414x560")
program.title("OCR-Converter")

customtkinter.set_appearance_mode("dark")

background_image = customtkinter.CTkImage(light_image=Image.open('resources/background.png'), 
                                          dark_image=Image.open('resources/background.png'), 
                                          size=(414, 560))

background_label = customtkinter.CTkLabel(program, 
                                          text="", 
                                          image=background_image)
background_label.pack()

origin_directory_button = customtkinter.CTkButton(master=program, 
                                                  width=341, 
                                                  height=55, 
                                                  text="INSIRA A PASTA DE ORIGEM...", 
                                                  fg_color="#FFFFFF", 
                                                  text_color="#052232",
                                                  command=lambda: selectFile("1"))

origin_directory_button.place(relx=0.5,
                              rely=0.3, 
                              anchor="center")

destiny_directory_button = customtkinter.CTkButton(master=program, 
                                                   width=341, 
                                                   height=55, 
                                                   text="INSIRA A PASTA DE DESTINO...", 
                                                   fg_color="#FFFFFF", 
                                                   text_color="#052232",
                                                   command=lambda: selectFile("2"))

destiny_directory_button.place(relx=0.5, 
                               rely=0.45, 
                               anchor="center")

process_button = customtkinter.CTkButton(master=program, 
                                         width=236,
                                         height=38 ,
                                         text="PROCESSAR",
                                         fg_color="#051D4A", 
                                         command=controller)

process_button.place(relx=0.5, 
                     rely=0.65, 
                     anchor="center")


program.mainloop()