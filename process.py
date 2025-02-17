import argparse
import json
from lxml import etree
from extract import extract
from card import Card

namespaces = { "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main" }

# TODO: clean up this file
# TODO: strip unicode from runs? need a solution

# parse xml
def parse_xml(filepath):
    # Grab document
    doc = etree.parse(filepath)
    body = doc.getroot().getchildren()[0]

    paragraph_elements = body.xpath(".//w:p", namespaces=namespaces)

    cards = []
    card = Card() # TODO: only grabs the same card

    for paragraph_element in paragraph_elements:
        text_elements = paragraph_element.xpath(".//w:t", namespaces=namespaces)
        paragraph = []

        for text_element in text_elements:
            text, style = parse_element(text_element)

            if style == "Tag":
                if not card.paragraphs:
                    card.tag += text; # add tag
                else:
                    cards.append(card) # add existing card
                    card = Card(tag=text) # new card # TODO: merely changes the tag?
            
            elif style in {"Normal/Card", "Underline", "Emphasis", "Cite"}:
                paragraph.append((text, style)) # add body

        if paragraph:  # avoid empty paragraphs, TODO: fix tag, tag
            card.paragraphs.append(paragraph)

    if card.paragraphs:
        cards.append(card) # add last card
        
    for card in cards:
        print(json.dumps(card.to_dict(), indent=4))

# return the style and text for each text element
def parse_element(text_element):
    parent_element = text_element.getparent()
    style_element = parent_element.xpath(".//w:rStyle", namespaces=namespaces)

    if len(style_element) == 0:
        # grab paragraph style
        parent_element = parent_element.getparent() # Grandparent.
        style_element = parent_element.xpath(".//w:pStyle", namespaces=namespaces)

    text = text_element.text
    style = "Normal/Card"

    if len(style_element) != 0:
        style_dump = parent_element.xpath(".//w:rStyle|.//w:pStyle", namespaces=namespaces)[0].get("{" + namespaces["w"] + "}val")
        # replace with a dictionary of style names, e.g., emphasis v. boxes.
        if style_dump == "StyleUnderline": style = "Underline"
        if style_dump == "Emphasis": style = "Emphasis"
        if style_dump == "Style13ptBold": style = "Cite"
        if style_dump == "Heading4": style = "Tag"
        if style_dump == "Heading3": style = "Block"
        if style_dump == "Heading2": style = "Hat"
        if style_dump == "Heading1": style = "Pocket"

    # print(text, "-", style)
    return text, style

def main():
    # parses output2.xml fine, re: speed for large documents
    # file = './cards/output2.xml'
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", help="file path")
    args = parser.parse_args()
    docxpath = args.docx

    xmlpath = extract(docxpath)
    parse_xml(xmlpath)

if __name__ == "__main__":
    main()