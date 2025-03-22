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
    
# TODO: style dictionary?