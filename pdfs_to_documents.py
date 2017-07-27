import nltk
import os
from optparse import OptionParser
from tqdm import tqdm
import PyPDF2
#import slate

def pdf_to_text_PyPDF2(path):
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        document = ''
        for i in range(0, pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            document += page.extractText()
        return document
    

#def pdf_to_text(path):
#    with open(path, 'rb') as pdf_file:
#        pdf_doc = slate.PDF(pdf_file)
#        document = ''
#        for page in pdf_doc:
#            document += page
#        return document

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="specify input folder")
    parser.add_option("-o", "--output", dest="output", help="specify output folder")
  
    (options, args) = parser.parse_args()
    
    print("PDFs 2 Documents")
    
    if not options.input:
        parser.error("Specify an input folder.")
    
    if not options.output:
        parser.error("Specify an output folder.")
    
    if not os.path.exists(options.input):
        parser.error("Specify an existing input folder.")
        
    os.makedirs(options.output, exist_ok=True)
    
    for (dirpath, dirnames, filenames) in os.walk(options.input):
        for filename in tqdm(filenames):
            os.system("pdftotext -enc UTF-8 '" + os.path.join(dirpath, filename) + "' '" + os.path.join(options.output, os.path.basename(dirpath)+filename)+".txt'")
            