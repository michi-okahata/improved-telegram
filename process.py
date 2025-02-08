from lxml import etree
import json
from card import Card, Card_Paragraph, Card_Run

# Next step is to generate cards + text dumps
# Maintain paragraph integrity

namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def parse(filepath):
    # Grab document
    doc = etree.parse(filepath)
    body = doc.getroot().getchildren()[0]

    # Get tags
    '''
    tags = {element.tag for element in body.iter()}
    stripped_tags = {etree.QName(tag).localname for tag in tags}
    print(stripped_tags)
    '''

    text_elements = body.xpath(".//w:t", namespaces=namespaces)

    # Card might be useless, just make a dict
    # Need to figure out how to parse paragraphs

    for text_element in text_elements:
        style, text = parse_element(text_element)
        '''
        Iterate through each text element
        if tag -> new card, add tag
        if paragraph -> add paragraph
        if run -> add run and style 

        if tag -> add a new card, new card is what is accessed
        if paragraph -> add new paragraph to card
        if run -> add run and style to paragraph   
        '''


# Return the style and text for each text element.
def parse_element(text_element):
    parent_element = text_element.getparent()
    style_element = parent_element.xpath(".//w:rStyle", namespaces=namespaces)

    if len(style_element) == 0:
        # Grab paragraph style
        parent_element = parent_element.getparent() # Grandparent.
        style_element = parent_element.xpath(".//w:pStyle", namespaces=namespaces)

    style = "Normal/Card"
    text = text_element.text

    if len(style_element) != 0:
        style_dump = parent_element.xpath(".//w:rStyle|.//w:pStyle", namespaces=namespaces)[0].get("{" + namespaces["w"] + "}val")
        # Replace with a hash set of style names, e.g., emphasis v. boxes.
        if style_dump == "Heading4": style = "Tag"
        if style_dump == "Style13ptBold": style = "Cite"
        if style_dump == "StyleUnderline": style = "Underline"
        if style_dump == "Emphasis": style = "Emphasis"

    print(style + ":" + text)
    return style, text

def main():
    # Parses output2.xml fine, re: speed for large documents
    # file = './cards/output2.xml'
    file = "./cards/output.xml"
    parse(file)

main()