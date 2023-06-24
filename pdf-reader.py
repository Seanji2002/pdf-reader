import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

import sys

class PDFReader:
    def __init__(self, out_path: str):
        if platform.system() == "Windows":
            # For this to work, please go and download the OCR engine from https://github.com/UB-Mannheim/tesseract/wiki/
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            
            # Follow this link to download the poppler for windows:https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
            self.path_to_poppler_exe = r"C:\Program Files\poppler-0.68.0_x86\bin"
        
        out_directory = Path(out_path).expanduser()

        # Store all the pages of the PDF in a variable
        self.image_file_list = []
        
        # Store all the pages of the PDF in a variable
        self.text_file = out_directory / Path("out_text.txt")

    def read_pdf(self, PDF_file: str, begin_page: int, end_page: int):
        with TemporaryDirectory() as tempdir:
            # converting pdf into images and saving them in a temporary directory
            if platform.system() == "Windows":
                pdf_pages = convert_from_path(
                    PDF_file, 500, poppler_path=self.path_to_poppler_exe, first_page=begin_page, last_page=end_page
                )
            # else:
            #     pdf_pages = convert_from_path(PDF_file, 500)
            # Iterate through all the pages stored
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                # Create a file name to store the image
                filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                # Declaring filename for each page of PDF as JPG: aka PDF page n -> page_00n.jpg
                # Save the image of the page in system
                page.save(filename, "JPEG")
                self.image_file_list.append(filename)

            with open(self.text_file, "w") as output_file:
                # for each page, recognize the text in the image and write the text into the file
                for image_file in self.image_file_list:
                    text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                    text = text.replace("-\n", "")
                    output_file.write(text)
     
if __name__ == "__main__":
    if len(sys.argv) == 5:
        print("Arguments provided: ")
        print("out path: ", sys.argv[1])
        print("pdf path: ", sys.argv[2])
        print("begin page #: ", sys.argv[3])
        print("end page #: ", sys.argv[4])
        print("Running PDF Reader...")
        out_path, pdf_path, begin_page, end_page = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        pdf_reader = PDFReader(out_path)
        pdf_reader.read_pdf(pdf_path, int(begin_page), int(end_page))
        print("out_text.txt file created successfully")
    else:
        print("Please provide valid arguments in the following order:")
        print("out path, pdf path, begin page #, end page #")