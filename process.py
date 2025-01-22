from lxml import etree
import re
import json

# import zipfile

from card import Card, Card_Paragraph, Card_Run

run1 = Card_Run("Economic decline", "Bold")
run2 = Card_Run("doesn't cause war.", "Italic")

# Create Card_Paragraph with a list of Card_Run objects
paragraph = Card_Paragraph([run1, run2])

# Create Card with a list of Card_Paragraph
walt20 = Card("Economic decline doesn't cause war.", [paragraph])

# Print the result of to_dict
card_dict = walt20.to_dict()
print(json.dumps(card_dict, indent=4))

def parse_2(filepath):
    # Parse document
    doc = etree.parse(filepath)

    # Document body
    body = doc.getroot().getchildren()[0]

    # Get tags
    tags = {element.tag for element in body.iter()}
    stripped_tags = {etree.QName(tag).localname for tag in tags}
    print(stripped_tags)

    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # rStyle v. pStyle AND only searches the first rStyle
    # 'x' in title instead!

    # pstyle_elements = body.iterfind('.//w:pStyle', namespaces)
    # rstyle_elements = body.iterfind('.//w:rStyle', namespaces)

    # Not matching blank/none

    # Find the text -> search for parent value rStyle OR pStyle (would this work), if null then Normal/Card

    '''

    style_elements = body.xpath('.//w:rStyle|.//w:pStyle', namespaces=namespaces)

    text_elements = body.xpath('.//w:t', namespaces=namespaces) # DOES grab ALL text.

    for text in text_elements:
        print(text.text)

    for style in style_elements:
        attribute = style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        print(attribute)

    '''

    # Clear spaces ' '? How to deal with that.
    text_elements = body.iterfind('.//w:t', namespaces=namespaces)

    for text_element in text_elements:
        parent_element = text_element.getparent()
        style_element = parent_element.xpath('.//w:rStyle|.//w:pStyle', namespaces=namespaces)
        style = 'Normal/Card' if len(style_element) is 0 else parent_element.xpath('.//w:rStyle|.//w:pStyle', namespaces=namespaces)[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        text = text_element.text
        print(style, ':', text)

def main():
    # Parses output2.xml fine, re: speed for large documents
    file = './cards/output2.xml'
    parse_2(file)

main()