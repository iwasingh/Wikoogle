"""
Extracting just raw text from the Wikipedia dumps is pretty hellish. Apparently the official Wikipedia parser itself is something like one 5000 line PHP function. There are about 30 or so alternate parsers that attempt to do this with limited success. I tried a lot of those options, but eventually had to hack together some terrible scripts of my own to do the job.
https://www.mediawiki.org/wiki/Alternative_parsers
"""
class Wikimarkup:
    def text(self, dump):
        pass
