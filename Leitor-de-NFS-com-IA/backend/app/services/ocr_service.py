import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import io
import os
from typing import Literal


# Defina o caminho para o Tesseract se necessário (comum em Docker)
# os.environ['TESSERACT_CMD'] = '/usr/bin/tesseract'

async def extrair_texto_de_arquivo(
        file_path: str,
        mime_type: Literal["application/pdf", "image/png", "image/jpeg"]
) -> str:
    """
    Extrai texto bruto de um arquivo (PDF ou Imagem) usando OCR se necessário.
    """

    if mime_type == "application/pdf":
        try:
            # 1. Tentativa de extração de texto direto (PDF baseado em texto)
            doc = fitz.open(file_path)
            texto_completo = ""
            for page in doc:
                texto_completo += page.get_text()

            # 2. Se o texto for mínimo, provavelmente é um PDF de imagem (escaneado)
            if len(texto_completo.strip()) < 100:
                texto_completo = await _ocr_de_pdf(file_path)

            return texto_completo

        except Exception as e:
            print(f"Erro ao processar PDF, tentando OCR: {e}")
            return await _ocr_de_pdf(file_path)  # Fallback para OCR

    elif mime_type in ["image/png", "image/jpeg"]:
        # 3. Extração direta de OCR de imagem
        return await _ocr_de_imagem(file_path)

    else:
        raise ValueError(f"Tipo de arquivo não suportado: {mime_type}")


async def _ocr_de_imagem(file_path: str) -> str:
    """Função auxiliar para aplicar OCR em um arquivo de imagem."""
    try:
        img = Image.open(file_path)
        # Usar o português como língua para o Tesseract
        texto = pytesseract.image_to_string(img, lang='por')
        return texto
    except Exception as e:
        print(f"Erro no OCR da imagem {file_path}: {e}")
        return ""


async def _ocr_de_pdf(file_path: str) -> str:
    """Função auxiliar para aplicar OCR em um PDF (convertendo para imagens)."""
    try:
        # Requer 'poppler' instalado no sistema/container
        paginas = convert_from_path(file_path, 300)  # 300 DPI
        texto_completo = ""
        for i, pagina_img in enumerate(paginas):
            print(f"Processando OCR da página {i + 1} do PDF...")
            texto_completo += pytesseract.image_to_string(pagina_img, lang='por') + "\n\n"
        return texto_completo
    except Exception as e:
        print(f"Erro na conversão PDF para imagem (Poppler?): {e}")
        return ""