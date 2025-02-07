from lxml import etree
import json
from card import Card, Card_Paragraph, Card_Run

# Steal Kansas cards 

run1 = Card_Run("Economic decline", "Bold")
run2 = Card_Run("doesn't cause war.", "Italic")

# Create Card_Paragraph with a list of Card_Run objects
paragraph = Card_Paragraph([run1, run2])

# Create Card with a list of Card_Paragraph
walt20 = Card("Economic decline doesn't cause war.", [paragraph])

# Print the result of to_dict
card_dict = walt20.to_dict()
print(json.dumps(card_dict, indent=4))

def parse(filepath):
    # Parse document
    doc = etree.parse(filepath)

    # Document body
    body = doc.getroot().getchildren()[0]

    # Get tags
    tags = {element.tag for element in body.iter()}
    stripped_tags = {etree.QName(tag).localname for tag in tags}
    print(stripped_tags)

    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    w_val = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'

    # Figure out Heading4 (Tag) and so on.
    # Figure out card objects, new cards, jsonl.

    # Grab text
    text_elements = body.xpath('.//w:t', namespaces=namespaces)

    '''
    Grab text
    Grab run style, text parent
    Grab paragraph style, text parent parent OR 
    '''

    # This works!
    for text_element in text_elements:
        parent_element = text_element.getparent()
        style_element = parent_element.xpath('.//w:rStyle', namespaces=namespaces)

        if len(style_element) == 0:
            parent_element = parent_element.getparent()
            style_element = parent_element.xpath('.//w:pStyle', namespaces=namespaces)

        style = 'Normal/Card' if len(style_element) is 0 else parent_element.xpath('.//w:rStyle|.//w:pStyle', namespaces=namespaces)[0].get(w_val)
        text = text_element.text
        print(style + ": " + text)

def main():
    # Parses output2.xml fine, re: speed for large documents
    # file = './cards/output2.xml'
    file = './cards/output2.xml'
    parse(file)

main()