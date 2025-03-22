import json
from lxml import etree

from card import Card

ns = {'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def parse_xml(file_path):
    # Grab xml
    document = etree.parse(file_path)
    xml_body = document.getroot().getchildren()[0]

    paragraph_elements = xml_body.xpath('.//w:p', namespaces=ns)

    card = Card()

    for paragraph_element in paragraph_elements:
        text_elements = paragraph_element.xpath('.//w:t', namespaces=ns)
        paragraph = []

        for text_element in text_elements:
            text, style = parse_element(text_element)
        
            if style == "Tag":
                if not card.paragraphs:
                    card.tag += text; # Add tag
                else:
                    add_card(card)
                    card = Card(tag=text)
            
            elif style in {"Normal/Card", "Underline", "Emphasis", "Cite"}:
                paragraph.append((text, style)) # Add body

        if paragraph: # Avoid empty paragraphs?
            card.paragraphs.append(paragraph)
    
    if card.paragraphs:
        add_card(card)


def add_card(card):
    with open('cards.jsonl', 'w', encoding='utf-8') as f:
        json.dump(card, f, indent=4, ensure_ascii=False)


def parse_element(text_element):
    parent_element = text.getparent()
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