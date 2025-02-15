# need to reliably extract the xml from word
# TODO: add error handling to everything
import zipfile

def extract(docxpath):
    with zipfile.ZipFile(docxpath, 'r') as doc: 
        print(doc.namelist())
        with doc.open('word/document.xml') as xml_file:
            xml_content = xml_file.read()

    xmlpath = docxpath[:-5] + ".xml"
    with open(xmlpath, 'wb') as output:
        output.write(xml_content)

    return xmlpath

def main():
    # Test
    docxpath = "./da---kant.docx"
    extract(docxpath)

if __name__ == "__main__":
    main()