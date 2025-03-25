import os
import json
import zipfile

from lxml import etree

class Card:
    def __init__(self, tag: str = "", cite: list = None, body: list = None):
        self.tag = tag
        self.cite = cite if cite is not None else []
        self.body = body if body is not None else []

    def to_dict(self):
        return {
            "tag": self.tag,
            "cite": self.cite, 
            "body": self.body
        }


def extract(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as doc:
        with doc.open('word/document.xml') as xml_file:
            xml_content = xml_file.read()

    xml_path = os.path.splitext(docx_path)[0] + '.xml'
    with open(xml_path, 'wb') as output:
        output.write(xml_content)


ns = {'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def parse_xml(file_path):
    # Grab xml
    document = etree.parse(file_path)
    xml_body = document.getroot().getchildren()[0]
    jsonpath = os.path.splitext(file_path)[0] + '.jsonl'

    paragraph_elements = xml_body.xpath('.//w:p', namespaces=ns)

    card = Card()

    for paragraph_element in paragraph_elements:
        text_elements = paragraph_element.xpath('.//w:t', namespaces=ns)
        paragraph = []

        for text_element in text_elements:
            text, style = parse_element(text_element)
        
            if style == "Tag":
                if not card.body:
                    card.tag += text; # Add tag
                else:
                    add_card(card, jsonpath)
                    card = Card(tag=text)
            
            elif style in {"Normal/Card", "Underline", "Emphasis", "Cite"}:
                paragraph.append((text, style)) # Add body

        if not card.cite:
            for t in paragraph:
                if t[1] == "Cite":
                    card.cite.append(paragraph)
                    break
        elif paragraph: # Avoid empty paragraphs?
            card.body.append(paragraph)
    
    if card.body:
        add_card(card, jsonpath)


def add_card(card, jsonpath):
    with open(jsonpath, 'a', encoding='utf-8') as f:
        json_str = json.dumps(card.to_dict())
        f.write(json_str + '\n')


def parse_element(text_element):
    parent_element = text_element.getparent()
    style_element = parent_element.xpath(".//w:rStyle", namespaces=ns)

    if len(style_element) == 0:
        # Grab paragraph style
        parent_element = parent_element.getparent() # Grandparent.
        style_element = parent_element.xpath(".//w:pStyle", namespaces=ns)

    text = text_element.text
    style = "Normal/Card"

    if len(style_element) != 0:
        style_dump = parent_element.xpath(".//w:rStyle|.//w:pStyle", namespaces=ns)[0].get("{" + ns['w'] + "}val")
        if style_dump == "StyleUnderline": style = "Underline"
        if style_dump == "Emphasis": style = "Emphasis"
        if style_dump == "Style13ptBold": style = "Cite"
        if style_dump == "Heading4": style = "Tag"
        if style_dump == "Heading3": style = "Block"
        if style_dump == "Heading2": style = "Hat"
        if style_dump == "Heading1": style = "Pocket"
    
    return text, style