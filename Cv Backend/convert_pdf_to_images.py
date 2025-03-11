import os
import fitz  # PyMuPDF
from PIL import Image
import base64

import io


def convert_pdf_to_images(pdf_path, output_dir, dpi=300):
    
    pdf_document = fitz.open(pdf_path)
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    images_base64 = []
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        zoom_factor = dpi / 72
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        
         # here converting image to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        images_base64.append(img_str)


        
        # if output_dir:
        #     image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        #     img.save(image_path, "PNG")
           
        #     print(f"Saved {image_path}")
    
    pdf_document.close()
    return images_base64