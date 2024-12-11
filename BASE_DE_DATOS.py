import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import pandas as pd

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extraer_texto_pdfs(carpeta_pdfs):
    datos = []  # Aquí almacenaremos texto extraído de cada PDF

    # Iterar sobre cada archivo en la carpeta
    for archivo in os.listdir(carpeta_pdfs):
        if archivo.endswith(".pdf"):  # Procesar solo archivos PDF
            ruta_pdf = os.path.join(carpeta_pdfs, archivo)
            print(f"Procesando: {archivo}")
            texto_completo = ""

            # Intentar leer texto directamente con PyPDF2
            try:
                lector = PdfReader(ruta_pdf)
                for pagina in lector.pages:
                    texto_completo += pagina.extract_text()
            except Exception as e:
                print(f"Error al leer {archivo} con PyPDF2, intentando OCR...")

            # Si no se extrajo texto, usar OCR
            if not texto_completo.strip():
                imagenes = convert_from_path(ruta_pdf)  # Convertir cada página a imagen
                for img in imagenes:
                    texto_completo += pytesseract.image_to_string(img)  # Usar OCR

            # Guardar el texto y el nombre del archivo
            datos.append({"archivo": archivo, "texto": texto_completo})

    # Convertir los datos a un DataFrame de pandas
    return pd.DataFrame(datos)

if __name__ == "__main__":
    carpeta_pdfs = r"C:\Users\Kenneth Garcia\Desktop\env\DATOS\PDFS"  # Ruta a la carpeta con los PDFs
    df_pdfs = extraer_texto_pdfs(carpeta_pdfs)

    # Guardar los datos en un archivo CSV
    df_pdfs.to_csv("base_datos_texto.csv", index=False)
    print("Texto extraído y guardado en base_datos_texto.csv")
"hplita
"