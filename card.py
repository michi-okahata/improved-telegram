class Card:
    def __init__(self, tag: str = "", paragraphs: list = None):
        self.tag = tag
        self.paragraphs = paragraphs if paragraphs is not None else []

    def to_dict(self):
        return {
            "Tag": self.tag,
            "Body": self.paragraphs
        }

if __name__ == "__main__":
    print("test")