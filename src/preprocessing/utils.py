import re
from parsing.symbols import Bold, Italic, ItalicAndBold, \
    Heading3, Heading4, Heading, Table

from parsing.utils import recursive, MalformedTag


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

    is_there = Table.start.re.search(text)
    while is_there is not None:
        try:
            match = recursive(text, Table.start, Table.end, is_there.start())
            text = text[:match.start()] + ' ' + text[match.end():]
            is_there = Table.start.re.search(text)
        except MalformedTag as e:
            print(e.message)
            break

    text = re.sub(r'<ref[\s\S]*?\/\>(!?<\/ref\>)*|<ref[\s\S]*?\>*?[<]?\/ref\>', "", text)
    text = re.sub(r'\*', "", text)

    return text
