from optparse import OptionParser
import os
import shutil

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="specify url")
    parser.add_option("-o", "--out", dest="output", help="specify output directory")
    parser.add_option("-i", "--in", dest="input", help="specify input directory")

    (options, args) = parser.parse_args()
    if not options.url:
        parser.error('Please specifiy an url!')
        
    if not options.output:
        parser.error('Please specifiy an output directory!')
        
    if not options.input:
        parser.error('Please specifiy an input directory!')
        
    if not os.path.exists(options.output):
        os.makedirs(options.output)
        
    if not os.path.exists(options.input):
        parser.error('Please specify an existing input directory!')
    
    print("URL Based Extractor")
    print("In: %s" % options.input)
    print("Out: %s" % options.output)
    print("URL: %s" % options.url)
    print("Extracting:")
    for filename in os.listdir(options.input):
        if filename.endswith(".txt"): 
            fabsolute = os.path.join(options.input, filename)
            with open(fabsolute, 'r') as f:
                l = f.readline()
                p = l.split(';')
                url = p[0].replace('"','')
                if url.startswith(options.url):
                    print(url)
                    shutil.copy2(fabsolute, options.output)                   
        else:
            continue

    