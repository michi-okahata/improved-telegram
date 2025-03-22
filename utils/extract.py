import os
import zipfile

def extract(docx_path: str) -> str:
    """
    Extracts xml from docx.

    Args: docx_path (str): docx file path.
    Returns: xml_path (str): xml file path.
    """
    with zipfile.ZipFile(docx_path, 'r') as doc:
        # print(doc.namelist())
        with doc.open('word/document.xml') as xml_file:
            xml_content = xml_file.read()

    xml_path = os.path.splitext(docx_path)[0] + ".xml"
    with open(xml_path, 'wb') as output:
        output.write(xml_content)

    return xml_path