class Embed:
    def __init__(
        self,
        title: str,
        description: str,
        color: int,
    ):
        self.title = title
        self.description = description
        self.color = color
        self.footer = {}
        self.author = {}
        self.fields = []

    def set_footer(self, text: str, icon_url: str = None):
        self.footer = {
            "text": text,
            "icon_url": icon_url,
        }

    def set_author(self, name: str, url: str = None, icon_url: str = None):
        self.author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
        }

    def add_field(self, name: str, value: str, inline: bool = False):
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline,
        })

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "footer": self.footer,
            "author": self.author,
            "fields": self.fields,
        }