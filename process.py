import argparse

from utils.extract import extract
from utils.parse import parse_xml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", help="file path")
    args = parser.parse_args()
    docxpath = args.docx

    xmlpath = extract(docxpath)
    parse_xml(xmlpath)

if __name__ == "__main__":
    main()