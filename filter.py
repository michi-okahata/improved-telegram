import os
import jsonlines
import argparse

def filter(jsonpath):
    json_out = os.path.splitext(jsonpath)[0] + '_out.jsonl'

    with jsonlines.open(jsonpath, 'r') as reader, jsonlines.open(json_out, 'w') as writer:
        for card in reader:
            new_body = []
            for paragraph in card['body']:
                blank = True
                for run in paragraph: 
                    if run[1] != "Normal/Card": 
                        blank = False
                if not blank:
                    new_body.append(paragraph)
            card['body'] = new_body
            writer.write(card)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('json', help='file path')
    args = parser.parse_args()
    jsonpath = args.json

    filter(jsonpath)