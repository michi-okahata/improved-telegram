import argparse

from utils import extract
from utils import parse_xml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('docx', help='file path')
    args = parser.parse_args()
    docx_path = args.docx

    xml_path = extract(docx_path)
    parse_xml(xml_path)

if __name__ == "__main__":
    main()