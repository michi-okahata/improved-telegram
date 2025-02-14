# need to reliably extract the xml from word
# TODO: add error handling to everything
import zipfile

def extract(docxpath):
    with zipfile.ZipFile(docxpath, 'r') as doc: 
        print(doc.namelist())
        with doc.open('word/document.xml') as xml_file:
            xml_content = xml_file.read()

    with open(docxpath[:-5] + ".xml", 'wb') as output:
        output.write(xml_content)

docxpath = "./1AC---UT Semis---mini.docx"

extract(docxpath)