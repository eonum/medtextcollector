## script to extract texts from PDFs
## based on https://gist.github.com/tiarno/8a2995e70cee42f01e79

import os
from tqdm import tqdm
from optparse import OptionParser
from PyPDF2 import PdfFileReader
import math
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine



def pdf_to_text_PyPDF2(path):
    """
    Takes the source path of a PDF and extracts its text.
    :param path: PDF src
    :return: string containing the text
    """
    with open(path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        document = ''
        for i in range(0, pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            document += page.extractText()
        return document


def pdf_to_text_pdfminer(file_src):
    """
    Takes a PDF and extracts its text.
    :param file_src: source path of PDF
    :return: string containing the text

    from https://stackoverflow.com/questions/44024697/
        how-to-read-pdf-file-using-pdfminer3k
    """
    fp = open(file_src, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()

    return extracted_text


def walk(obj, fnt, emb):
    """
    If there is a key called 'BaseFont', that is a font that is used in the
    document.
    If there is a key called 'FontName' and another key in the same dictionary
    object
    that is called 'FontFilex' (where x is null, 2, or 3), then that fontname is
    embedded.

    We create and add to two sets, fnt = fonts used and emb = fonts embedded.
    """
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        # test to see if there is FontFile
        if [x for x in fontkeys if x in obj]:
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb  # return the sets for each page


def hasFonts(file_src):
    """
    Check if any fonts can be detected in PDF.
    :param file_src: source path
    :return: True, if a font could be detected; False otw.
    """
    pdf = PdfFileReader(file_src)
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

def outFolderName(prefix, nFiles, filesPerFolder):
    """
    Constructs a folder name (eg. "files1", "files2") based on the
    :param prefix:
    :param nFiles:
    :param filesPerFolder:
    :return:
    """
    if (not filesPerFolder > 0):
        print("invalid number of files per folder")
        return

    suffix = str(math.floor(nFiles / filesPerFolder))
    return str(prefix) + suffix


if __name__ == '__main__':
    # Parse input.
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="specify input folder")
    parser.add_option("-o", "--output", dest="output",
                      help="specify output folder")
    (options, args) = parser.parse_args()

    options.input = str(options.input)
    options.output = str(options.output)

    # Check if directories are available.
    if not options.input:
        parser.error("Specify an input folder.")
    if not options.output:
        parser.error("Specify an output folder.")
    if not os.path.exists(options.input):
        parser.error("Specify an existing input folder.")
    os.makedirs(options.output, exist_ok=True)


    # We try to distinguish the following 4 PDF categories:
    # 1. machine_pdfs   (plain text, produced by a machine)
    # 2. ocr_pdfs       (scanned PDFs with an OCR layer containing text, all
    #                    samples had used english OCR on german text, resulting
    #                    in an 'Umlaut'-problem)
    # 3. scanned_pdfs   (PDFs containing no text, checked by function
    #                    hasFonts)
    # 4. faulty_pdfs    (could not be opened properly)

    machine_pdfs_count = 0
    ocr_pdfs_count = 0
    ocr_pdfs_names = ''
    scanned_pdfs_count = 0
    scanned_pdfs_names = ''
    faulty_pdfs_count = 0
    faulty_pdfs_names = ''
    saved_files_count = 0

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
                    faulty_pdfs_count += 1
                    faulty_pdfs_names += file_src + "\n"
                    continue

                # Files which have fonts might be plain text or preprocessed by
                # OCR
                if foundFonts:

                    try:
                        text = pdf_to_text_PyPDF2(file_src)
                        # text = pdf_to_text_pdfminer(file_src)
                    except:
                        faulty_pdfs_count += 1
                        faulty_pdfs_names += file_src + "\n"
                        continue

                    # If 'Umlaut' contained in text, it's most likely not
                    # processed by a standard english ocr
                    if any(c in text for c in ['ä', 'Ä', 'ü', 'Ü', 'ö', 'Ö']):
                        machine_pdfs_count += 1

                        # create folders with maximal 1000 files
                        out_dir = outFolderName("txtFiles", saved_files_count,
                                                1000)
                        out_path = os.path.join(options.output, out_dir)
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)

                        output_src = os.path.join(out_path, fn + '.txt')

                        # command line tool seems to work best for extracting
                        # text from PDF
                        os.system("pdftotext -enc UTF-8 '" + file_src + "' '"
                                  + output_src + "'")

                        # with open(output_src, "w") as text_file:
                        #      print(text, file=text_file)

                        saved_files_count += 1

                    # If no 'Umlaut' contained in text, it's most likely
                    # processed by a standard english ocr
                    else:
                        ocr_pdfs_count += 1
                        ocr_pdfs_names += file_src + "\n"
                        # TODO process them


                # Files without fonts are most likely unprocessed scans
                else:
                    scanned_pdfs_count += 1
                    scanned_pdfs_names += file_src + "\n"
                    # TODO process them

    with open(os.path.join(options.output, "ocr_pdfs.txt"), "w") \
            as text_file:
        print(ocr_pdfs_names, file=text_file)

    with open(os.path.join(options.output, "scanned_pdfs.txt"), "w") \
            as text_file:
        print(scanned_pdfs_names, file=text_file)

    with open(os.path.join(options.output, "faulty_pdfs.txt"), "w") \
            as text_file:
        print(faulty_pdfs_names, file=text_file)


    print("\nPlain-Text PDFs:", machine_pdfs_count,
          "\t\tPDFs with OCR:", ocr_pdfs_count)
    print("Faulty PDFs: ", faulty_pdfs_count,
          "\t\tScanned PDFs:", scanned_pdfs_count)





