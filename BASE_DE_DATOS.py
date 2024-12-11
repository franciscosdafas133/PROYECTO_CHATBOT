import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd

# Configuración para Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extraer_texto_pdfs(carpeta_pdfs):
    datos = []

    for archivo in os.listdir(carpeta_pdfs):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_pdfs, archivo)
            print(f"Procesando: {archivo}")
            texto_completo = ""

            try:
                # Intentar extraer texto directamente con PyMuPDF
                with fitz.open(ruta_pdf) as documento:
                    for pagina in documento:
                        texto_pagina = pagina.get_text()
                        if texto_pagina.strip():  # Verificar si hay texto
                            texto_completo += texto_pagina
                        else:
                            # Si no hay texto, usar OCR
                            pixmap = pagina.get_pixmap()
                            imagen = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
                            texto_completo += pytesseract.image_to_string(imagen)
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")

            datos.append({"archivo": archivo, "texto": texto_completo})

    return pd.DataFrame(datos)

if __name__ == "__main__":
    carpeta_pdfs = r"C:\Users\Kenneth Garcia\Desktop\env\DATOS\PDFS"
    df_pdfs = extraer_texto_pdfs(carpeta_pdfs)
    df_pdfs.to_csv("base_datos_texto.csv", index=False)
    print("Texto extraído y guardado en base_datos_texto.csv")
