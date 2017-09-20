## script to check the amount of scanned PDFs, which need OCR
## based on https://gist.github.com/tiarno/8a2995e70cee42f01e79

import os
from tqdm import tqdm
from optparse import OptionParser
from PyPDF2 import PdfFileReader


def pdf_to_text_PyPDF2(path):
    with open(path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        document = ''
        for i in range(0, pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            document += page.extractText()
        return document


def walk(obj, fnt, emb):
    '''
    If there is a key called 'BaseFont', that is a font that is used in the document.
    If there is a key called 'FontName' and another key in the same dictionary object
    that is called 'FontFilex' (where x is null, 2, or 3), then that fontname is
    embedded.

    We create and add to two sets, fnt = fonts used and emb = fonts embedded.
    '''
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        if [x for x in fontkeys if x in obj]:  # test to see if there is FontFile
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb  # return the sets for each page


def hasFonts(fname):
    pdf = PdfFileReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        obj = page.getObject()
        f, e = walk(obj['/Resources'], fonts, embedded)
        fonts = fonts.union(f)
        embedded = embedded.union(e)

        if len(fonts) > 0:
            return True

    return False




if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="specify input folder")
    parser.add_option("-o", "--output", dest="output", help="specify output folder")
    (options, args) = parser.parse_args()

    # Check directories
    if not options.input:
        parser.error("Specify an input folder.")
    if not options.output:
        parser.error("Specify an output folder.")
    if not os.path.exists(options.input):
        parser.error("Specify an existing input folder.")
    os.makedirs(options.output, exist_ok=True)

    # count how many pdfs are scanned
    machine_pdfs = 0
    ocr_pdfs = 0
    scanned_pdfs = 0
    faulty_pdfs = 0

    print("Start walking through directory.")
    for (dirpath, dirnames, filenames) in os.walk(options.input):

        for filename in tqdm(filenames):
            file_src = os.path.join(dirpath, filename)
            fn, ext = os.path.splitext(filename)
            if (file_src and ext in (".PDF", ".pdf")):

                # some files might be faulty (e.g. empty, corrupted..)
                try:
                    foundFonts = hasFonts(file_src)
                except:
                    faulty_pdfs += 1
                    continue

                # Files which have fonts might be plain text or preprocessed by OCR
                if foundFonts:
                    text = pdf_to_text_PyPDF2(file_src)
                    if any(c in text for c in ['ä', 'Ä', 'ü', 'Ü', 'ö', 'Ö']):
                        machine_pdfs += 1

                        output_src = os.path.join(dirpath, fn + '.txt')
                        with open(output_src, "w") as text_file:
                             print(text, file=text_file)

                    else:
                        ocr_pdfs += 1
                        # TODO process them


                # Files without fonts are most likely unprocessed scans
                else:
                    scanned_pdfs += 1
                    # TODO process them


    print("\nPlain-Text PDFs:", machine_pdfs, "\t\tPDFs with OCR:", ocr_pdfs)
    print("Faulty PDFs: ", faulty_pdfs, "\t\tScanned PDFs:", scanned_pdfs)





