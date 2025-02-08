import json

class Card:
    def __init__(self, tag: str = None, paragraph_list: list = None):
        self.tag = tag
        self.paragraphs = paragraph_list

    def to_dict(self):
        return {
            "Tag": self.tag,
            "Paragraphs": [para.to_dict() for para in self.paragraphs]
        }

class Card_Paragraph:
    def __init__(self, card_runs: list):
        self.runs = card_runs
    
    def to_dict(self):
        return {
            "Runs": [run.to_dict() for run in self.runs]
        }

class Card_Run:
    def __init__(self, run_style: str, run_text: str):
        self.style = run_style
        self.text = run_text
    
    def to_dict(self):
        return {
            "Style": self.style,
            "Text": self.text
        }

if __name__ == "__main__":
    run1 = Card_Run("Economic decline", "Bold")
    run2 = Card_Run("doesn't cause war.", "Italic")

    paragraph = Card_Paragraph([run1, run2])

    walt20 = Card("Economic decline doesn't cause war.", [paragraph])

    card_dict = walt20.to_dict()
    print(json.dumps(card_dict, indent=4))