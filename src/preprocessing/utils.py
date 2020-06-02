import re
from parsing.symbols import Bold, Italic, ItalicAndBold, Heading3, Heading4, Heading


def clean(text):
    tags = [
        Bold,
        ItalicAndBold,
        Italic,
        Heading3,
        Heading4,
        Heading,
    ]

    for i in tags:
        text = re.sub(i.start.regex, "", text)

    text = re.sub(r'<ref[\s\S]*?\/\>(!?<\/ref\>)*|<ref[\s\S]*?\>*?[<]?\/ref\>', "", text)
    text = re.sub(r'\*', "", text)

    return text
